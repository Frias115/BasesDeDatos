
from pymongo import MongoClient

# name
# kind
# direction
# geolocation


class POI(object):

    def __init__(self, name, kind=None, address=None, geolocation=None, **args):
        self._name = name
        self._kind = kind
        self._address = address
        self._geolocation = geolocation
        self.modfieds = set()

    @property
    def name(self):
        return self._name

    @property
    def kind(self):
        return self._kind

    @property
    def address(self):
        return self._address

    @property
    def geolocation(self):
        return self._geolocation



    @name.setter
    def name(self, name):
        self._name = name
        self.modfieds.add("name")

    @kind.setter
    def kind(self, kind):
        self._kind = kind
        self.modfieds.add("kind")

    @address.setter
    def address(self, address):
        self._address = address
        self.modfieds.add("address")

    @geolocation.setter
    def geolocation(self, geolocation):
        self._geolocation = geolocation
        self.modfieds.add("geolocation")


# name
# province
# autonomous_community
# geolocation
# area
# elevation
# population

class City(object):

    def __init__(self, initial_data):
        for key in initial_data:
            setattr(self, key, initial_data[key])
        self.modfieds=set()

    def set_attribute(self, key, value):
        self.__dict__[key] = value
        self.modfieds.add(str(key))

    def get_attribute(self, key):
        return self.__dict__[key]

    # Compuebo si existe una City con esos mismo datos
    def save(self, datos):
        prueba = self.modfieds.pop()
        print (prueba)
        for i in self.modfieds:
            print('a')

        self.modfieds.clear()

        # PREGUNTA: Con que comando subo las cosas a la base de datos y hay diferentes comandos
        # cuando ya existe el objeto en base de datos o no
        # si el insert para nuevos, update para existentes, chequeo la id para saber cual utilizar

        # dentro del for vamos a iterar sobre id no sobre los atributos de la id
        # recorrer toda la lista de ciudades, comprobar booleanos de city y actualizar la base de
        # datos mirando los ids que si se han cambiado

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
                print res.get_attribute('name')
                return res
            except StopIteration:
                return None
        else:
            return None

# WEB DE REFERENCIA: http://api.mongodb.com/python/current/api/pymongo/command_cursor.html

if __name__ == "__main__":

    one = [{'$match': {'location.type': 'Point'}}, {'$project': {'name': 1}}]
    two = [{'$match': {'province': 'Zamora'}}, {'$project': {'autonomous_community': 1}}]

    cities = City.query(one)

    city = City.next_result(cities)

    city.set_attribute('name', 'prueba')

    print city.modfieds