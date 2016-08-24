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
	            document_id INTEGER,
	            field  TEXT,
	            value  TEXT,
	            type   TEXT,
	            FOREIGN KEY(document_id) REFERENCES document(id))'''


get_collections	          = 'SELECT name FROM collection'
get_collection_query      = 'SELECT id,name FROM collection where name=:name'
set_collection_query      = 'INSERT into collection     (name)                            VALUES (:name)'
set_document_query	  = 'INSERT into document       (jobject, collection_id)          VALUES (:jobject, :collection_id)'
set_document_fields_query = 'INSERT into document_field (document_id, field, value, type) VALUES (:document_id,  :field, :value, :type)'
get_document_fields_query = 'SELECT document_id FROM document_field where field=:field and value=:value'
get_document_object       = 'SELECT jobject FROM document where id=:id'



def __create_tables(conn):
    cursor = conn.cursor()
    cursor.execute(COLLECTION)
    conn.commit()
    cursor.execute(DOCUMENT)
    conn.commit()
    cursor.execute(DOCUMENT_FIELD)
    conn.commit()
    	

class nsql_collection(object):
    def __init__(self, id, name, conn):
	self.id   = id
	self.name = name
    	self.conn = conn
    	
    
    def insert(self, jobject):
	native_json = json.loads(jobject)
	# Primero se crea el document	

	cursor = self.conn.cursor()
	cursor.execute(set_document_query, { 'jobject': jobject, 'collection_id': self.id })
	document_id = cursor.lastrowid
	self.conn.commit()
    	
    	for key in native_json.keys():
    	    field = key
    	    value = str(native_json[key])
    	    t     = type(native_json[key]).__name__
	    cursor.execute(set_document_fields_query, {'document_id': document_id, 'field': field, 'value': value, 'type': t})
	    self.conn.commit()
    	
    	return '{ object_id: %d }' % document_id
    	
    def find(self, query, limit = 1):
	keys = query.keys()
	if len(keys) > 1:
	    return None
	
	field = keys[0]
	if type(query[field]).__name__ == 'int':
	    value = str(query[field])	
	else:
	    value = query[field]
	        	
    	cursor = self.conn.cursor()
    	cursor.execute(get_document_fields_query, {'field': field, 'value': value})
    	document_id_list = cursor.fetchall()

	jobjects_documents = []
	if len(document_id_list) == 0:
	    return jobjects_documents
	else:
	    i = 0
	    while i < limit and i < len(document_id_list): 
		_id, = document_id_list[i]
		i    = i + 1
    		cursor.execute(get_document_object, { 'id': _id })
    		document,  = cursor.fetchone()
    		jobjects_documents.append({'_id': _id, 'document': document})
    	    return jobjects_documents

    def update (self, objectid, jobject):
	pass
    
    def delete (self, filter):
	pass
    	    	
class nsql_database(object):
    def __init__(self, conn):
	self.conn = conn

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
	pass

def nonSQLiteClient(database):
    create_tables = False
    if database == ':memory:' or not os.path.isfile(database):
	create_tables = True
	
    conn = sqlite3.connect(database)

    if create_tables:
	__create_tables(conn)
	
    return nsql_database(conn)
    
