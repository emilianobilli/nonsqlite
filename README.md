# nonsqlite
Non SQL Database over SQLite3

## Getting Started
> $ pip install nonsqlite

This package install nonsqlite and Object modules

## Object Module
Micro ORM Framework
### Create a new Object collecion
```
from nonsqlite.Object import Object


class Person(Object):
  def __init__(self):
    self.name = ''
    self.age  = 0
```  
### Save a new Object in collection
```
a = Person()
a.name = 'Piter'
a.age  = 21
a.save()
```
### Query Objects in collection
- Get one object
```
a = Person.get({'name': 'Piter'})
print a.name
```
- Get list of coincidences: ```filter({}), filterAND([{}]), filterOR([{}])```
```
a = Person.filter({'name': 'Piter'})
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
