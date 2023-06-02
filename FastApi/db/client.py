from pymongo import MongoClient


# db_client = MongoClient().local #BASE DE DATOS LOCAL 

db_client = MongoClient(
    'mongodb+srv://zuntrixit_fastapi:glblK1nzdLbD6jZp@cluster0.nqcohk6.mongodb.net/?retryWrites=true&w=majority').test




# Modulo de conexion MongoDB: pip install pymongo
#Ejecucion: sudo mongod --dbpath "/Users/luisangel/Documents/LuisAngel/MongoDB/data"
#Conexion: mongodb://localhost

#zuntrixit_fastapi
#glblK1nzdLbD6jZp
