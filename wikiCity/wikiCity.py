
import json

class puntoInteres:

    def __init__(self, nombre, tipo=None, direccion=None, geolocalizacion=None):
        self._nombre = nombre
        self._tipo = tipo
        self._direccion = direccion
        self._geolocalizacion = geolocalizacion

        self.nombreFlag = False
        self.tipoFlag = False
        self.direccionFlag = False
        self.geolocalizacionFlag = False


    @property
    def nombre(self):
        return self._nombre

    @property
    def tipo(self):
        return self._tipo

    @property
    def direccion(self):
        return self._direccion

    @property
    def geolocalizacion(self):
        return self._geolocalizacion



    @nombre.setter
    def nombre(self, nombre):
        self._nombre = nombre
        self.nombreFlag = True

    @tipo.setter
    def tipo(self, tipo):
        self._tipo = tipo
        self.tipoFlag = True

    @direccion.setter
    def direccion(self, direccion):
        self._direccion = direccion
        self.direccionFlag = True

    @geolocalizacion.setter
    def geolocalizacion(self, geolocalizacion):
        self._geolocalizacion = geolocalizacion
        self.geolocalizacionFlag = True


class Ciudad:

    def __init__(self, nombre, provincia=None, comunidadAutonoma=None, superficie=None, altitud=None, poblacion=None):
        self._nombre = nombre
        self._provincia = provincia
        self._comunidadAutonoma = comunidadAutonoma
        self._superficie = superficie
        self._altitud = altitud
        self._poblacion = poblacion
        self._geolocalizacion = []
        self._puntosInteres = []

        self.nombreFlag = False
        self.provinciaFlag = False
        self.comunidadAutonomaFlag = False
        self.geolocalizacionFlag = False
        self.superficieFlag = False
        self.altitudFlag = False
        self.poblacionFlag = False
        self.puntosInteresFlag = False

    @property
    def nombre(self):
        return self._nombre

    @property
    def provincia(self):
        return self._provincia

    @property
    def comunidadAutonoma(self):
        return self._comunidadAutonoma

    @property
    def geolocalizacion(self):
        return self._geolocalizacion

    @property
    def superficie(self):
        return self._superficie

    @property
    def altitud(self):
        return self._altitud

    @property
    def poblacion(self):
        return self._poblacion

    @property
    def puntosInteres(self):
        return self._puntosInteres



    @nombre.setter
    def nombre(self, nombre):
        self._nombre = nombre
        self.nombreFlag = True

    @provincia.setter
    def provincia(self, provincia):
        self._provincia = provincia
        self.provinciaFlag = True

    @comunidadAutonoma.setter
    def comunidadAutonoma(self, comunidadAutonoma):
        self._comunidadAutonoma = comunidadAutonoma
        self.comunidadAutonomaFlag = True

    @geolocalizacion.setter
    def geolocalizacion(self, geolocalizacion):
        self._geolocalizacion = geolocalizacion
        self.geolocalizacionFlag = True

    @superficie.setter
    def superficie(self, superficie):
        self._superficie = superficie
        self.superficieFlag = True

    @altitud.setter
    def altitud(self, altitud):
        self._altitud = altitud
        self.altitudFlag = True

    @poblacion.setter
    def poblacion(self, poblacion):
        self._poblacion = poblacion
        self.poblacionFlag = True

    @puntosInteres.setter
    def puntosInteres(self, puntosInteres):
        self._puntosInteres = puntosInteres
        self.puntosInteresFlag = True


ciudades = []

with open('wikicity.json','r') as file:
    for i in file:
        data = json.loads(i)
    for i in data:
        ciudad = Ciudad(i["name"], i["province"], i["autonomous_community"], i["area"], i["elevation"], i["population"])
        for j in i["location"]["coordinates"]:
            ciudad.geolocalizacion.append(j)
        for j in i["POI"]:
            punto = puntoInteres(j["name"], j["kind"])
            ciudad.puntosInteres.append(puntoInteres)

        ciudades.append(ciudad)
    file.close()

for i in ciudades:
    print(i.nombre)


