from nonsqlite import nonSQLiteClient
from json      import dumps
from json      import loads

class Object(object):
    def __init__(self):
	self._collection = nonSQLiteClient('orm.db').getCollection(self.__class__.__name__)
	self._id 	 = None

    def save(self):
	fields = vars(self)
	keys   = fields.keys()
	
	doc = {}

	
	for key in keys:
	    if key != '_id' and key != '_collection':
		doc[key] = fields[key]

	if self._id is None:
	    ret = self._collection.insert(dumps(doc))
	    self._id = ret['object_id']
	else:
	    self._collection.update(self._id, dumps(doc))

    def delete(self):
	self._collection.deleteDocument(self._id)

    def filter(self, query):
	ret = []
	element_list = self._collection.find(query, -1)
	for element in element_list:
	    doc  = loads(element['document'])
	    keys = doc.keys()
	    obj  = self.__class__()
	    for key in keys:
		obj.__setattr__(key, doc[key])
	    ret.append(obj)
	
	return ret

    def get(self, query):
	ret = self._collection.findOne(query)
	if ret is not None:
	    document = ret[0]
	    doc = loads(document['document'])
	    keys = doc.keys()
	    obj  = self.__class__()
	    for key in keys:
		obj.__setattr__(key, doc[key])
	    return obj
	else:
	    return None

