import sqlite3
import json
import os


COLLECTION = '''CREATE TABLE collection (
	        id INTEGER PRIMARY KEY AUTOINCREMENT,
	        name TEXT)'''

DOCUMENT   = '''CREATE TABLE document (
	        id INTEGER PRIMARY KEY AUTOINCREMENT,
	        jobject TEXT,
	        collection_id INTEGER,
	        FOREIGN KEY(collection_id) REFERENCES collection(id))'''

DOCUMENT_FIELD = '''CREATE TABLE document_field (
		    id INTEGER PRIMARY KEY AUTOINCREMENT,
	            document_id   INTEGER,
		    collection_id INTEGER,
	            field  TEXT,
	            value  TEXT,
	            type   TEXT,
	            FOREIGN KEY(document_id) REFERENCES document(id))'''



debug_select_all_collections		   = 'SELECT * FROM collection'
debug_select_all_documents		   = 'SELECT * FROM document'
debug_select_all_document_fields	   = 'SELECT * FROM document_field'


get_collections	           		   = 'SELECT name FROM collection'
get_collection_query       		   = 'SELECT id,name FROM collection where name=:name'
set_collection_query       		   = 'INSERT into collection     (name)                            VALUES (:name)'
set_document_query	   		   = 'INSERT into document       (jobject, collection_id)          VALUES (:jobject, :collection_id)'
set_document_fields_query  		   = 'INSERT into document_field (document_id, collection_id, field, value, type) VALUES (:document_id, :collection_id, :field, :value, :type)'
get_document_fields_query  		   = 'SELECT document_id FROM document_field where collection_id=:collection_id and field=:field and value=:value'
get_document_value_query		   = 'SELECT document_id FROM document_field where collection_id=:collection_id and value=:value'
get_document_fields_query_like		   = 'SELECT document_id FROM document_field where collection_id=:collection_id and field=:field and value LIKE :value'
get_document_value_query_like		   = 'SELECT document_id FROM document_field where collection_id=:collection_id and value LIKE :value'
count_document_fields_query		   = 'SELECT count(*) FROM document_field where collection_id=:collection_id and field=:field and value=:value'

get_document_object        		   = 'SELECT jobject FROM document where id=:id and collection_id=:collection_id'

get_all_id_documents_by_collection_id	   = 'SELECT id FROM document    WHERE collection_id=:id'
get_all_documents_by_collection_id	   = 'SELECT id, jobject FROM document WHERE collection_id=:id'
delete_all_documents	   		   = 'DELETE FROM document       WHERE collection_id=:id'
delete_all_document_fields 		   = 'DELETE FROM document_field WHERE document_id=:id'
delete_document				   = 'DELETE FROM document	 WHERE id=:id'
delete_collection	   		   = 'DELETE FROM collection     WHERE id=:id' 
update_document				   = 'UPDATE document SET jobject=:jobject WHERE id=:id and collection_id=:collection_id'

def __create_tables(conn):
    cursor = conn.cursor()
    cursor.execute(COLLECTION)
    conn.commit()
    cursor.execute(DOCUMENT)
    conn.commit()
    cursor.execute(DOCUMENT_FIELD)
    conn.commit()


class Stack(object):
    def __init__(self):
	self.content = []
    def empty(self):
	if len(self.content) > 0:
	    return False
	return True
    def push(self, obj):
	self.content.append(obj)
    def pop(self):
	if not self.empty():
	    return self.content.pop()
	return None
	    


def toupletify (value, field_string, touple_list):
    s = Stack()
    if type(value).__name__ == 'dict':
	for key in value.keys():
	    s.push(key)
    
	key = s.pop()
	while key is not None:
	    if field_string == '':
		toupletify(value[key], key, touple_list)
	    else:
		toupletify(value[key], field_string + '.' + key, touple_list)
	    key = s.pop()

    elif type(value).__name__ == 'list':
	for element in value:
	    touple_list.append((field_string, element))
    else:
	touple_list.append((field_string,value))

    return

    	

class nsql_collection(object):
    def __init__(self, id, name, conn):
	self.id   = id
	self.name = name
    	self.conn = conn
    	
    
    def update(self, did, jobject):
	native_json = json.loads(jobject)
	self.__delete_all_document_fields(did)
	cursor = self.conn.cursor()
	cursor.execute(update_document, {'jobject': jobject, 'id': did, 'collection_id': self.id})
	self.conn.commit()

	touple_list = []
	toupletify(native_json, '', touple_list)

	for touple in touple_list:
	    field, value = touple
	    t = type(value).__name__	
	    cursor.execute(set_document_fields_query, {'document_id': did, 'collection_id': self.id, 'field': field, 'value': value, 'type': t})
	    self.conn.commit()


    def insert(self, jobject):
	native_json = json.loads(jobject)
	# Primero se crea el document	

	cursor = self.conn.cursor()
	cursor.execute(set_document_query, { 'jobject': jobject, 'collection_id': self.id })
	document_id = cursor.lastrowid
	self.conn.commit()


	touple_list = []
	toupletify(native_json, '', touple_list)

	for touple in touple_list:
	    field, value = touple
	    t = type(value).__name__	
	    cursor.execute(set_document_fields_query, {'document_id': document_id, 'collection_id': self.id, 'field': field, 'value': value, 'type': t})
	    self.conn.commit()
    	
    	return { 'object_id': document_id }

    def findOne(self, query):
	return self.find(query, 1)

    def findAll(self, query):
	return self.find(query, -1)

    def findLikeOne(self, query):
	return self.find(query, 1, True)

    def findLikeAll(self, query):
	return self.find(query, -1, True)
	
    def count(self, query):
	keys = query.keys()
	if len(keys) > 1:
	    return None
	
	field = keys[0]
	if type(query[field]).__name__ == 'int' or type(query[field]).__name__ == 'float' or type(query[field]).__name__ == 'bool':
	    value = str(query[field])	
	else:
	    value = query[field]

	cursor = self.conn.cursor()
	cursor.execute(count_document_fields_query, {'field': field, 'value': value, 'collection_id': self.id})
	c, = cursor.fetchone() 
	return c

    def get(self, oid):
	cursor = self.conn.cursor()
	cursor.execute(get_document_object, { 'id': oid, 'collection_id': self.id })
	try:
	    document, = cursor.fetchone()
	    return {'_id': oid, 'document': document}
	except:
	    return None

    def all(self):
	cursor = self.conn.cursor()

	cursor.execute(get_all_documents_by_collection_id, {'id': self.id})
	_all = cursor.fetchall()

	jobjects_documents = []
	for i in _all:
	    _id, document = i
	    jobjects_documents.append({'_id': _id, 'document': document})
	
	return jobjects_documents

    def find(self, query, limit = 1, like=False):
	keys = query.keys()
	if len(keys) > 1:
	    return None
	
	field = keys[0]
	if type(query[field]).__name__ == 'int' or type(query[field]).__name__ == 'float':
	    value = str(query[field])	
	else:
	    value = query[field]
	        	

	cursor = self.conn.cursor()
	if field == '$':
	    if like:
		cursor.execute(get_document_value_query_like, {'value' : value, 'collection_id': self.id})
	    else:
		cursor.execute(get_document_value_query, {'value' : value, 'collection_id': self.id})
    	else:
	    if like:
    		cursor.execute(get_document_fields_query_like, {'field': field, 'value': value, 'collection_id': self.id})
	    else:
		cursor.execute(get_document_fields_query, {'field': field, 'value': value, 'collection_id': self.id})

	if limit == 1:
	    document_id_list = [cursor.fetchone()]
	else:    
	    document_id_list = cursor.fetchall()

	temp = []
	for d in document_id_list:
	    if d not in temp and d != None:
		temp.append(d)

	document_id_list = temp

	jobjects_documents = []
	if len(document_id_list) == 0:
	    return jobjects_documents
	else:
	    i = 0
	    if limit == -1:
		while i < len(document_id_list): 
		    _id, = document_id_list[i]
		    i    = i + 1
    		    cursor.execute(get_document_object, { 'id': _id, 'collection_id': self.id })
    		    document,  = cursor.fetchone()
    		    jobjects_documents.append({'_id': _id, 'document': document})
    		return jobjects_documents
	    else:
		while i < limit and i < len(document_id_list): 
		    _id, = document_id_list[i]
		    i    = i + 1
    		    cursor.execute(get_document_object, { 'id': _id, 'collection_id': self.id })
    		    document,  = cursor.fetchone()
    		    jobjects_documents.append({'_id': _id, 'document': document})
    		return jobjects_documents


    def __delete_all_document_fields(self, did):
	cursor = self.conn.cursor()
	cursor.execute(delete_all_document_fields, {'id': did} )
	self.conn.commit()

    def getDocument(self, did):
	cursor = self.conn.cursor()
	cursor.execute(get_document_object, { 'id' : did })
	document,  = cursor.fetchone()
    	jobjects_documents.append({'_id': _id, 'document': document})
    	return jobjects_documents

    def deleteDocument(self, did):
	cursor = self.conn.cursor()
	self.__delete_all_document_fields(did)
	cursor.execute(delete_document, {'id': did})	
	self.conn.commit()

    def delete (self, filter):
	pass


    	    	
class nsql_database(object):
    def __init__(self, conn):
	self.conn = conn


    def _debug_dump(self):
	cursor = self.conn.cursor()
	
	cursor.execute(debug_select_all_collections)
	coll = cursor.fetchall()
	
	print '\n----------- COLLECTIONS -------------\n'
	for c in coll:
	    print c
	    
	cursor.execute(debug_select_all_documents)
	docs = cursor.fetchall()
	
	print '\n----------- DOCUMENTS ---------------\n'
	for d in docs:
	    print d

	cursor.execute(debug_select_all_document_fields)
	dfields = cursor.fetchall()
	
	print '\n----------- DOCUMENTS FIELDS --------\n'
	for d in dfields:
	    print d

    def getCollection(self, collection_name):
	cursor = self.conn.cursor()
	cursor.execute(get_collection_query, { 'name': collection_name })
	coll =  cursor.fetchone()
	
	if coll is None:
	    # Se debe crear la collection
	    cursor.execute(set_collection_query, { 'name': collection_name })
	    id   = cursor.lastrowid
	    name = collection_name
	    self.conn.commit()
	else:
	    id, name = coll
	return nsql_collection(id,name,self.conn)

    def showCollections(self):
	cursor = self.conn.cursor()
	cursor.execute(get_collections)
	collections = []
	for name_tuple in cursor.fetchall():
	    name, = name_tuple
	    collections.append(name)
	
	return collections


    def dropCollection(self, collection_name):
	cursor = self.conn.cursor()
	cursor.execute(get_collection_query, { 'name': collection_name })
	coll = cursor.fetchone()
	
	if coll is None:
	    return

	_id, __none = coll

	cursor.execute(get_all_id_documents_by_collection_id, { 'id': _id })
	document_list = cursor.fetchall()

	for document in document_list:
	    _document_id, = document
	    cursor.execute(delete_all_document_fields, { 'id' : _document_id })
	
	cursor.execute(delete_all_documents, { 'id': _id })
	cursor.execute(delete_collection,    { 'id': _id })
	self.conn.commit()

def nonSQLiteClient(database):
    create_tables = False
    if database == ':memory:' or not os.path.isfile(database):
	create_tables = True
	
    conn = sqlite3.connect(database)

    if create_tables:
	__create_tables(conn)
	
    return nsql_database(conn)
    
