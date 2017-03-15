import pymongo
from pymongo import errors
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

    # Compuebo si existe una City con esos mismo datos
    def save(self, datos):
        prueba = self.modifieds.pop()
        print (prueba)
        for i in self.modifieds:
            print('a')

        self.modifieds.clear()

        # PREGUNTA: Con que comando subo las cosas a la base de datos y hay diferentes comandos
        # cuando ya existe el objeto en base de datos o no
        # si el insert para nuevos, update para existentes, chequeo la id para saber cual utilizar

        # dentro del for vamos a iterar sobre id no sobre los atributos de la id
        # recorrer toda la lista de ciudades, comprobar booleanos de city y actualizar la base de
        # datos mirando los ids que si se han cambiado


    # En la version dinamica seria necesario un metodo update que
    # permita modificar los atributos una vez se haya creado el objeto y anada un flag de modificado.
    #
    # Viendo vuestro codigo he visto que utilizais un metodo get_attribute para obtener los parametros.
    # Tened en cuenta que si habeis utilizado el metodo update de __dict__ en el constructor, las variables
    # pertenecen al objeto y podeis acceder directamente (res.name). Si utilizamos el update es porque queremos
    # poder realizar comprobaciones y activar el flag de modificacion.

    # - Realizarlo de forma estatica definiendo en el constructor cada atributo y realizar la mismas comprobaciones que antes.
    # En este caso no seria necesario metodo update pero si definir los getters y setters para cada atributo


    def save_in_database(self):
        client = MongoClient('localhost', 27017)
        collection = client.test.wikicity
        try:
            if self.__dict__.has_key('_id'):
                changes = {}
                for x in self.modifieds:
                    changes[x] = self.__dict__.get(x)
                    print x
                    print self.__dict__.get(x)
                id = {}
                id['_id'] = self.__dict__.get('_id')
                print id
                collection.update_one( id, { '$set' : changes})
           # else:
                # collection.insert(self._id, self.changes)
            print "Succesful"
        except errors.ConnectionFailure as e:
            print "Something went wrong: " % e




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

    cities = City.query(one)

    city = City.next_result(cities)

    print (city.__dict__.get('_id'))

    city.update_attribute('name', 'prueba')

    city.save_in_database()

    cities = City.query(one)

    city2 = City.next_result(cities)

    print city2.name
