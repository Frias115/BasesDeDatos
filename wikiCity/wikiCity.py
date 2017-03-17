import pymongo
from pymongo import errors
from pymongo import MongoClient

class DBConecction:

    client = None

    @staticmethod
    def db_connect():
        DBConecction.client = MongoClient('localhost', 27017)
        collection = DBConecction.client.wikicity.wikicity

        collection.create_index([('location.coordinates',pymongo.GEOSPHERE)])

        return collection

    @staticmethod
    def db_close():
        DBConecction.client.close()


# name
# kind
# score
# avg_price

class POI(object):

    def __init__(self, initial_data):
        essential = ['name', 'kind', 'score', 'avg_price']

        self.__dict__.update(initial_data)

        [setattr(self, key, None) for key in essential if key not in self.__dict__]

    def update_attribute(self, key, value):
        self.__dict__[key] = value
        self.modifieds.add(str(key))

# name
# province
# autonomous_community
# location
# area
# elevation
# population
# POI

class City(object):

    def __init__(self, initial_data):
        essential = ['name', 'province', 'autonomous_community', 'location', 'area', 'elevation', 'population', 'POI']

        self.__dict__.update(initial_data)

        self.modifieds=set()

        [setattr(self, key, None) for key in essential if key not in self.__dict__]

        if self.__dict__.get('location') is None:
            setattr(self, 'location', {"type": "Point", "coordinates": [0,0]})



        if self.__dict__.get('POI') is not None:

            POI_list = None

            if isinstance(self.__dict__.get('POI'), list):
                POI_list = self.__dict__.get('POI')
            else:
                POI_list = []
                POI_list.append(self.__dict__.get('POI'))

            newPOI = []
            for x in POI_list:
                if type(x) is not dict:
                    newPOI.append(x.__dict__)
                else:
                    newPOI.append(x)

            setattr(self, 'POI', newPOI)


    def update_attribute(self, key, value):
        self.__dict__[key] = value
        self.modifieds.add(str(key))

    def save_in_database(self):
        collection = DBConecction.db_connect()
        try:
            if self.__dict__.has_key('_id') and self.modifieds.__len__() is not 0:
                changes = {} # comprensive dict
                for x in self.modifieds:
                    changes[x] = self.__dict__.get(x)
                id = {}
                id['_id'] = self.__dict__.get('_id')
                collection.update_one( id, { '$set' : changes})
                self.modifieds.clear()

            elif not self.__dict__.has_key('_id'):
                dict = self.__dict__
                dict.pop('modifieds')
                collection.insert_one(dict)
            print "Succesful"
        except errors.ConnectionFailure as e:
            print "Something went wrong: " % e

        DBConecction.db_close()

 # TAREAS
 # hacer las querys

    @staticmethod
    def query(list_of_instructions):
        collection = DBConecction.db_connect()
        result = collection.aggregate(list_of_instructions)
        DBConecction.db_close()
        return result

    @staticmethod
    def next_result(result):
        if result.alive:
            try:
                city_dict = result.next()
                res = City(city_dict)
                return res
            except StopIteration:
                return None
        else:
            return None

# WEB DE REFERENCIA: http://api.mongodb.com/python/current/api/pymongo/command_cursor.html

if __name__ == "__main__":

    one = [{'$match': {'location.type': 'Point'}}, {'$project': {'name': 1, 'location' : 1, 'POI' : 1}}]
    two = [{'$match': {'province': 'Zamora'}}, {'$project': {'autonomous_community': 1}}]
    three = [{'$match': {'name': 'Madrid'}}, {'$project': {'name': 1}}]
    four = [{'$match': {'location.coordinates': [0,0]}}, {'$project': {'location': 1}}]


    cities = City.query(one)

    city = City.next_result(cities)

    poiprueba = POI({'name' : 'prueba1'})

    poiprueba2 = POI({'name' : 'prueba2'})

    prueba2 = City({'name' : 'probando', 'POI' : poiprueba})

    print prueba2.__dict__


# Crear una ciudad
# Guardar
# modificar ciudad
# guardar
# query