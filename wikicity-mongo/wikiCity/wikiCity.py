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

        #default por si no hay un location con la estructura de un punto 2dSphere
        if self.__dict__.get('location') is None:
            setattr(self, 'location', {"type": "Point", "coordinates": [0,0]})

        #convierte listas de POI en diccionarios para poder guardarlos correctamente
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

        DBConecction.db_close()

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

if __name__ == "__main__":

    find = [{'$match': {'name': 'Madrid'}}, {'$project': {'name': 1}}]

    # Crear una ciudad
    u_tad = POI({"name": "u-tad", "kind": "University", "score": 5, "avg_price": 10000})
    madrid = City({"name": "Madrid", "province": "Madrid", "autonomous_community": "Madrid", "area": 605770000, "elevation": 657, "population": 3165541, "POI": u_tad})

    # Guardar
    madrid.save_in_database()

    # modificar ciudad
    query_result = City.query(find)
    new_city = City.next_result(query_result)
    new_city.update_attribute("name", "Madriz")

    # guardar
    new_city.save_in_database()

    # query
    primera = [{'$match': {'autonomous_community': 'Castilla y Leon'}}, {'$project': {'name': 1}}]
    segunda = [{'$match': {'autonomous_community': 'Castilla y Leon'}}, {'$group': {"_id": '$_id', 'media_elevation': {"$avg": '$elevation'}}}]
    tercera = [{'$match': {'autonomous_community': 'Castilla y Leon'}}, {'$group': {"_id": '$_id', 'media_elevation': {"$avg": '$population'}}}]
    cuarta = [{'$match': {'name': 'Leon'}}, {'$group': {"_id": '$POI.kind', 'count': {'$sum': 1}}}, {'$unwind': '$_id'}, {'$group': {"_id": '$_id', 'count': {"$sum": 1}}}]
    quinta = [{'$unwind': '$POI'}, {'$group': {"_id": {"name": '$name', "kind": '$POI.kind'}}}]
    sexta = [{'$match': {'name': 'Leon'}}, {'$unwind': '$POI'}, {'$match': {'POI.kind': 'Restaurant'}}, {'$group': {"_id": {"name": '$name', "kind": '$POI.kind'}, "minimumPrice": {"$min": '$POI.avg_price'}, "averagePrice": {'$avg': '$POI.avg_price'}, "maxPrice": {"$max": '$POI.avg_price'}}}]
    septima = [{'$geoNear': {'near': {'type': "Point", 'coordinates': [40,-5]}, 'distanceField': "dist.calculated", 'spherical': True}}, {'$unwind': '$POI'}, {'$match': {'POI.kind': 'Restaurant'}}, {'$sort': {"dist.calculated": -1}}, {'$group': {"_id": {"name": '$name', "kind": '$POI.kind', "distance": '$dist.calculated'}}}]
    octava = [{'$geoNear': {'near': {'type': "Point", 'coordinates': [40,-5]}, 'distanceField': "dist.calculated", 'maxDistance': 10000000, 'num': 5, 'spherical': 'true'}}, { '$unwind': '$POI'}, {'$match': {'POI.kind': 'Restaurant'}}, {'$sort': {"dist.calculated" : -1}}, {'$group': {"_id": {"name": '$name', "kind": '$POI.kind', "distance": '$dist.calculated'}}}]
    novena = [{'$match': {"name": {'$in':['Leon', 'Burgos']}}}, {'$unwind': '$POI'}, {'$match': {'POI.kind': 'Restaurant'}}, {'$match': {"POI.kind": 'Restaurant'}}, {'$group': {"_id": {"name": "$name", "POI.kind": '$POI.kind', "POI.name" : "$POI.name"}}}]
    decima = [{'$unwind': '$POI'}, {'$group': {"_id": {"name": '$name', "score": '$POI.score'}}}, {'$sort': {"_id.score": -1}}]
    onceava = [{'$unwind': '$POI'}, {'$match': {'POI.kind': 'Restaurant'}}, {'$group': {"_id": { "kind": '$POI.kind', 'name': '$POI.name'}, 'count': {"$sum": 1}}}, {'$sort': {"count" : -1}}, {'$limit' : 5}]


    query = City.query(primera)