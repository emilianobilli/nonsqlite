from nonsqlite import nonSQLiteClient

#
# Inicia la base de Datos
db = nonSQLiteClient(':memory:')

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
print pepe.insert( '{ "edad": 30 }' )


print "Busqueda Edad: 21"
# 
# Busqueda por edad == 21
print pepe.find( { 'edad': 21 })

#
# Busqueda por name == "Jeronimo"
print "Busqueda name: Jeronimo"
print pepe.find( { 'name': 'Jeronimo' })

#
# Muestra las colecciones
print db.showCollections()