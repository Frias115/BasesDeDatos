
from pymongo import MongoClient

# name
# kind
# direction
# geolocation

class POI:

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

class City:

    def __init__(self, name, province=None, autonomous_community=None, area=None, elevation=None, population=None, **args ):
        self._name = name
        self._province = province
        self._autonomous_community = autonomous_community
        self._area = area
        self._elevation = elevation
        self._population = population
        self._geolocation = []
        self._POIs = []
        self.modfieds=set()

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
    def name(self, name):
        self._name = name
        self.modfieds.add("name")

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


"""with open('wikicity.json','r') as file:
    for i in file:
        data = json.loads(i)
    for i in data:
        city = City(i["name"], i["province"], i["autonomous_community"], i["area"], i["elevation"], i["population"])
        for j in i["location"]["coordinates"]:
            city.geolocation.append(j)
        for j in i["POI"]:
            punto = POI(j["name"], j["kind"])
            city.POIs.append(POI)

        Cities.append(city)
    file.close()"""





def parser(datos):
    for i in datos:
        city = City(i["address"]["street"])
        #print(city.name)
        Cities.append(city)


#Compuebo si existe una City con esos mismo datos
def save(datos):
    update = [] #esto ahora es el modifieds de city y de poi
    for tupla in datos:
        print(tupla.nameFlag)
        if(tupla.nameFlag == True):
            print(tupla.nameFlag)
            update.append({'name' : tupla.name})

    print(update)

    #dentro del for vamos a iterar sobre id no sobre los atributos de la id
    #recorrer toda la lista de ciudades, comprobar booleanos de city y actualizar la base de datos mirando los ids que si se han cambiado



# http://api.mongodb.com/python/current/tutorial.html#documents
def query(listOfInstruccions):

    client = MongoClient('localhost', 27017)
    db = client.test.wikicity
    result = db.find()

    for document in result:
        print(document)
        datosQuery.append(document)





#PREGUNTA: como manejar los datos que no conocemos en el parser

#PREGUNTA: No cambia los flags en los setters, no se sabe por que, solucionado en ciudad

#PREGUNTA: Como cargar el wikicity.json, quitar los corchetes y las comas

#PREGUNTA: Tienen buena pinta las estrucutas iniciales, si, pero query y save son de ciudad y el parser va directamente dentro de la funcion query

#PREGUNNTA: podemos utilizar librerias como bson para cambiar los tipos de datos



if __name__ == "__main__":
    Cities = []

    one = [{'$match': {'borough': 'Bronx'}}, {'$project': {'address.street': 1}}]

    datosQuery = []

    query(one)

    #parser(datosQuery)

    #Cities[0].name = 'prueba'

    #save(Cities)