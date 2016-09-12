# nonsqlite
Non SQL Database over SQLite3

## Getting Started
```
$ pip install nonsqlite
```

This package install nonsqlite and Object modules

## Object Module
Micro ORM Framework
### Create a new Object collection
```
from nonsqlite.Object import Object


class Person(Object):
  def __init__(self):
    self.name = ''
    self.age  = 0
```  
### Specify the database to save the collection
```
Person._db_name = 'db.db'
```
If the _db_name is omitted, Object use the default database: Object.db in the current directory


### Save a new Object in collection
```
a = Person()
a.name = 'Piter'
a.age  = 21
a.save()
```

### Load the object from a json
```
a = Person.loads(json)
a.save()
```


### Query Objects in collection
- Get one object
```
a = Person.get({'name': 'Piter'})
print a.name
```
- Get list of coincidences: ```filter({}, limit=, sort=), filterAND([{}]), filterOR([{}])```
```
a = Person.filter({'name': 'Piter'}, sort='-age') # Order by age desc
for i in a:
  print i.name
```
```
a = Person.filterAND([{'name': 'Piter'}, {'age': 21}])
for i in a:
  print i.name
```
- Wildcard $
```
a = Person.filter({'$': 'Piter'})
```
### Delete an Object in collection
```
a = Person.get({'name': 'Piter'})
a.delete()
```

### Drop all Objects in collection
```
Person.drop()
```

### Count Objects with Occurrences
```
n = Person.count({'name': 'Piter'})
```

### Count all Objects in Collection
```
n = Person.len()
```
