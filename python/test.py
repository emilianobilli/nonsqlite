from nonsqlite import nonSQLiteClient

#
# Inicia la base de Datos
db = nonSQLiteClient('pepe.db')

#
# Crea la coleccion
pepe = db.getCollection('pepe')

print pepe.id
print pepe.name    	

#
# Inserta valores en la conexion
print pepe.insert( '{ "name": "Laura",    "edad": 21 }' )
print pepe.insert( '{ "name": "Gaston",   "edad": 21 }' )
print pepe.insert( '{ "name": "Jeronimo", "edad": 32 }')
print pepe.insert( '{ "edad": {"algo": 1}, "otra": [1,2,3,4]  }' )


print "Busqueda Edad: 21"
# 
# Busqueda por edad == 21
print pepe.find( { 'edad': 21 })


#
# pepe.find_gt
# pepe.find_lt
#


#
# Busqueda por name == "Jeronimo"
print "Busqueda name: Jeronimo"
print pepe.find( { 'name': 'Jeronimo' })
print "Busqueda compuesta"
print pepe.find( { 'edad.algo': 1 })
print "Busqueda en array"
print pepe.find( { 'otra' : 4 } )

print "Busqueda por cualquier valor"
x =  pepe.find( { 'name': '%nimo%' }, 10, True)
for i in x:
    print i
#db._debug_dump()

#
# Muestra las colecciones
print db.showCollections()
print db.dropCollection('pepe')
print db.showCollections()

#db._debug_dump()
#db.getCollection('felipe')
#db._debug_dump()



