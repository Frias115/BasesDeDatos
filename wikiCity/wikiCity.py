
import json
import pymongo

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

        self.nameFlag = False
        self.kindFlag = False
        self.addressFlag = False
        self.geolocationFlag = False


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
        self.nameFlag = True

    @kind.setter
    def kind(self, kind):
        self._kind = kind
        self.kindFlag = True

    @address.setter
    def address(self, address):
        self._address = address
        self.addressFlag = True

    @geolocation.setter
    def geolocation(self, geolocation):
        self._geolocation = geolocation
        self.geolocationFlag = True


# name
# province
# autonomous_community
# geolocation
# area
# elevation
# population

class City:

    def __init__(self, name, province=None, autonomous_community=None, area=None, elevation=None, population=None):
        self._name = name
        self._province = province
        self._autonomous_community = autonomous_community
        self._area = area
        self._elevation = elevation
        self._population = population
        self._geolocation = []
        self._POIs = []

        self.nameFlag = False
        self.provinceFlag = False
        self.autonomous_communityFlag = False
        self.geolocationFlag = False
        self.areaFlag = False
        self.elevationFlag = False
        self.populationFlag = False
        self.POIsFlag = False

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
        self.nameFlag = True

    @province.setter
    def province(self, province):
        self._province = province
        self.provinceFlag = True

    @autonomous_community.setter
    def autonomous_community(self, autonomous_community):
        self._autonomous_community = autonomous_community
        self.autonomous_communityFlag = True

    @geolocation.setter
    def geolocation(self, geolocation):
        self._geolocation = geolocation
        self.geolocationFlag = True

    @area.setter
    def area(self, area):
        self._area = area
        self.areaFlag = True

    @elevation.setter
    def elevation(self, elevation):
        self._elevation = elevation
        self.elevationFlag = True

    @population.setter
    def population(self, population):
        self._population = population
        self.populationFlag = True

    @POIs.setter
    def POIs(self, POIs):
        self._POIs = POIs
        self.POIsFlag = True




Cities = []

with open('wikicity.json','r') as file:
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
    file.close()



#def parser(self):


#Compuebo si existe una City con esos mismo datos
#def save(self):

one = [ {'$match' : {'borough' : 'Bronx'}} , {'$project' : {'address.street' : 1}} ]


# http://api.mongodb.com/python/current/tutorial.html#documents
def query(self, *listOfInstruccions):

    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    db = client.test.restaurants
    result = db.aggregate(listOfInstruccions)

    for document in result:
        print(document)


query(one)





