
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

    def __init__(self, name, province=None, autonomous_community=None, area=None,
                 elevation=None, population=None, **args):
        self._name = name
        self._province = province
        self._autonomous_community = autonomous_community
        self._area = area
        self._elevation = elevation
        self._population = population
        self._geolocation = []
        self._POIs = []
        self.modfieds=set()

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
                res = City(*city_dict)
                return res
            except StopIteration:
                return None
        else:
            return None


    @property
    def name(self):
        return self._name

    @property
    def province(self):
        return self._province

    @property
    def autonomous_community(self):
        return self._autonomous_community

    @property
    def geolocation(self):
        return self._geolocation

    @property
    def area(self):
        return self._area

    @property
    def elevation(self):
        return self._elevation

    @property
    def population(self):
        return self._population

    @property
    def POIs(self):
        return self._POIs

    @name.setter
    def name(self, val):
        self.modfieds.add('name')
        self._name = val

    @province.setter
    def province(self, province):
        self._province = province
        self.modfieds.add("province") #hay que tener cuiadado, ya que eso es el dato como esta en base de datos, no como en ciudad, en ciudad seria _province, hay que controlarlo

    @autonomous_community.setter
    def autonomous_community(self, autonomous_community):
        self._autonomous_community = autonomous_community
        self.modfieds.add("autonomous_community")

    @geolocation.setter
    def geolocation(self, geolocation):
        self._geolocation = geolocation
        self.modfieds.add("geolocation")

    @area.setter
    def area(self, area):
        self._area = area
        self.modfieds.add("area")

    @elevation.setter
    def elevation(self, elevation):
        self._elevation = elevation
        self.modfieds.add("elevation")

    @population.setter
    def population(self, population):
        self._population = population
        self.modfieds.add("population")

    @POIs.setter
    def POIs(self, POIs):
        self._POIs = POIs
        self.modfieds.add("POIs")

# PREGUNTA: como manejar los datos que no conocemos en el parser,
# con el **args y el update dinamico

# PREGUNTA: No cambia los flags en los setters, no se sabe por
# que, solucionado en ciudad

# PREGUNTA: Tienen buena pinta las estrucutas iniciales, si, pero query y save son
# de ciudad y el parser va directamente dentro de la funcion query

# WEB DE REFERENCIA: http://api.mongodb.com/python/current/api/pymongo/command_cursor.html

if __name__ == "__main__":

    # prueba = City('prueba')

    one = [{'$match': {'location.type': 'Point'}}, {'$project': {'name': 1}}]
    two = [{'$match': {'province': 'Zamora'}}, {'$project': {'autonomous_community': 1}}]

    cities = City.query(one)
    cities_result = []
    while City.next_result(cities) is not None:
        cities_result.append(cities)

    for x in cities_result:
        print x.name


