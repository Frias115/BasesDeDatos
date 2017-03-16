import pymongo
from pymongo import errors
from pymongo import MongoClient

# name
# kind
# direction
# geolocation


class POI(object):

    def __init__(self, initial_data):
        essential = ['name', 'kind', 'direction', 'geolocation']

        for key in initial_data:
            setattr(self, key, initial_data[key])

        self.modifieds = set()

        [setattr(self, key, None) for key in essential if key not in self.__dict__]

    def update_attribute(self, key, value):
        self.__dict__[key] = value
        self.modifieds.add(str(key))

# name
# province
# autonomous_community
# geolocation
# area
# elevation
# population

class City(object):

    def __init__(self, initial_data):
        essential = ['name', 'province', 'autonomous_community', 'geolocation', 'area', 'elevation', 'population']

        for key in initial_data:
            setattr(self, key, initial_data[key])

        self.modifieds=set()

        [setattr(self, key, None) for key in essential if key not in self.__dict__]

        # for key in essential:
        #   if key not in self.__dict__:
        #      setattr(self, key, None)

    def update_attribute(self, key, value):
        self.__dict__[key] = value
        self.modifieds.add(str(key))

    def save_in_database(self):
        client = MongoClient('localhost', 27017)
        collection = client.test.wikicity
        try:
            if self.__dict__.has_key('_id') and self.modifieds.__len__() is not 0:
                print (self.modifieds.__len__())
                changes = {}
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


 # PREGUNTAS
 # Preguntar si POI deberia tener modifieds
 # Como hacer que la funcion update_attribute se pueda llamar por las dos clases.
 # como aplicar lo del formato geojson y indexado 2dsphere

 # TAREAS
 # Usar la clase poi
 # tener en cuenta que save no guarde algo no modificado
 # hacer las querys
 # Simplificar el codigo que se ha repetido varias veces


    @staticmethod
    def query(list_of_instructions):
        client = MongoClient('localhost', 27017)
        collection = client.test.wikicity
        result = collection.aggregate(list_of_instructions)
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

    one = [{'$match': {'location.type': 'Point'}}, {'$project': {'name': 1}}]
    two = [{'$match': {'province': 'Zamora'}}, {'$project': {'autonomous_community': 1}}]
    three = [{'$match': {'name': 'Madrid'}}, {'$project': {'name': 1}}]

    cities = City.query(one)

    city = City.next_result(cities)

    print (city.__dict__.get('_id'))

    city.update_attribute('name', 'prueba')

    city.save_in_database()

    cities = City.query(one)

    city2 = City.next_result(cities)

    print city2.__dict__

    nuevo_poi = POI({'name': 'kind'})

    for x in nuevo_poi.__dict__:
        print x

