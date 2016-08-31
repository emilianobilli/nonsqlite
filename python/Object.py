from nonsqlite import nonSQLiteClient
from json      import dumps
from json      import loads


class Object(object):
    def __init__(self):
	self._collection = nonSQLiteClient('orm.db').getCollection(self.__class__.__name__)
	self._id 	 = None

    def checktype(self, obj):
	if (type(obj).__name__ != 'int'   and 
	    type(obj).__name__ != 'str'   and 
	    type(obj).__name__ != 'list'  and 
	    type(obj).__name__ != 'dict'  and 
	    type(obj).__name__ != 'float' and 
	    type(obj).__name__ != 'bool'):
	    return True
	else:
	    return False

    def getid(self):
	return self._id

    def save(self):
	fields = vars(self)
	keys   = fields.keys()
	
	doc = {}
	
	for key in keys:
	    if key != '_id' and key != '_collection':
		if self.checktype(fields[key]):
		    o, = fields[key].__class__.__bases__
		    if o.__name__ == 'Object':
			doc[key] = fields[key].getid()
		else:
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
	    obj = self.__load_document(element)
	    ret.append(obj)
	
	return ret

    def all(self):
	ret = []
	element_list = self._collection.all()
	for element in element_list:
	    obj = self.__load_document(element)
	    ret.append(obj)
	
	return ret

    def getbyid(self, oid):
	ret = self._collection.get(oid)
	if ret is not None:
	    return self.__load_document(ret)

    def get(self, query):
	ret = self._collection.findOne(query)
	if ret != []:
	    return self.__load_document(ret[0])

    def __load_document(self, document):
	    doc     = loads(document['document'])
	    keys    = doc.keys()
	    obj     = self.__class__()
	    obj._id = document['_id']
	    
	    # Si el objecto tiene atributos por definicion
	    # Estos son los objectos "fuertemente tipados"
	    objkeys  = vars(obj)
	    for key in keys:
		if key in objkeys:
		    if self.checktype(obj.__dict__[key]):
			o, = obj.__dict__[key].__class__.__bases__
			if o.__name__ == 'Object':
			    obj.__dict__[key].getbyid(doc[key])
		    else:
			obj.__setattr__(key, doc[key])
		else:
		    obj.__setattr__(key, doc[key])
	    return obj


