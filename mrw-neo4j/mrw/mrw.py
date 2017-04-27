# coding=utf-8
from neo4j.v1 import GraphDatabase

def show_services(postal_office=None):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "bleh"))
    with driver.session() as session:

        if postal_office is None:
            for office in session.run('MATCH (a:Oficina) RETURN a.urgente4h, a.name, a.urgente6h, a.urgente8h, a.normal12h, a.economico'):
                print('Oficina: ' + str(office['a.name']) +
                      ' \n\tEnvio urgente 4h: ' + str(office["a.urgente4h"]) +
                      ' \n\tEnvio urgente 6h: ' + str(office["a.urgente6h"]) +
                      ' \n\tEnvio urgente 8h: ' + str(office["a.urgente8h"]) +
                      ' \n\tEnvio normal 12h: ' + str(office["a.normal12h"]) +
                      ' \n\tEnvio economico:  ' + str(office["a.economico"]))
        else:
            aux_list = []
            if type(postal_office) is not list:
                aux_list.append(postal_office)
                postal_office = aux_list
            for p_o in range(0, len(postal_office)):
                for office in session.run('MATCH (a:Oficina {name: $name}) RETURN a.urgente4h, a.name, a.urgente6h, a.urgente8h, a.normal12h, a.economico', name=postal_office[p_o]):
                    print('Oficina: ' + str(office['a.name']) +
                          ' \n\tEnvio urgente 4h: ' + str(office["a.urgente4h"]) +
                          ' \n\tEnvio urgente 6h: ' + str(office["a.urgente6h"]) +
                          ' \n\tEnvio urgente 8h: ' + str(office["a.urgente8h"]) +
                          ' \n\tEnvio normal 12h: ' + str(office["a.normal12h"]) +
                          ' \n\tEnvio economico:  ' + str(office["a.economico"]))
        session.close()


def find_shortest_path(departure, arrival, type):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "bleh"))
    with driver.session() as session:

        for office in session.run(
                'Match (a:Oficina {name: $departure}) RETURN a.urgente4h, a.urgente6h, a.urgente8h, a.normal12h, a.economico', departure=departure):
            if office['a.' + str(type)] is False:
                print 'El tipo de envio solicitado no esta disponible.'
                return None
        if type is 'urgente4h':
            time = 4*60
        elif type is 'urgente6h':
            time = 6*60
        elif type is 'urgente8h':
            time = 8*60
        elif type is 'normal12h':
            time = 12*60
        else:
            time = 0

        total_cost = 0
        total_time = 0
        relationships = []
        route = []
        if time is 0:
            for office in session.run(
                    'MATCH a = (departure:Oficina {name: $departure})-[:Carretera | Ferroviario | Maritimo | Aereo*1..6]-(arrival:Oficina {name: $arrival}) '
                    'RETURN relationships(a) as relationships, nodes(a) as nodes, '
                    'REDUCE(cost=0, r in relationships(a) | cost + r.costeAsociado) as totalCost '
                    'order by totalCost ASC limit 1', departure = departure, arrival = arrival):
                print 'coste estimado: ' + str(office['totalCost'])
                total_cost = float(office['totalCost'])
                print 'Caminos entre las ciudades: '
                for relationship in range(0, len(office['relationships'])):
                    print '\t' + str(office['relationships'][relationship]['name'])
                    total_time = + float(office['relationships'][relationship]['tiempo'])
                    relationships.append(str(office['relationships'][relationship]['name']))
                print 'Nodos por los que pasa: '
                for nodo in range(0, len(office['nodes'])):
                    print '\t' + str(office['nodes'][nodo]['name'])
                    route.append(str(office['nodes'][nodo]['name']))

                for nodo in range(0, len(office['nodes'])):
                    if nodo >= len(office['nodes']) - 1:
                        print str(office['nodes'][nodo]['name'])
                    else:
                        print str(office['nodes'][nodo]['name']) + ' --[' + str(
                            office['relationships'][nodo]['name']) + ']->',

        else:
            for office in session.run(
                    'MATCH a = (departure:Oficina {name: $departure})-[:Carretera | Ferroviario | Maritimo | Aereo*1..6]-(arrival:Oficina {name: $arrival}) '
                    'RETURN relationships(a) as relationships, nodes(a) as nodes, '
                    'REDUCE(tiempo=0, r in relationships(a) | tiempo + r.tiempo) as totalTime '
                    'order by totalTime ASC limit 1', departure = departure, arrival = arrival):

                if office["totalTime"] > time:
                    print 'No existe una ruta valida que cumpla ese tipo de envio.'
                else:
                    print 'Tiempo estimado: ' + str(office['totalTime'])
                    total_time = float(office['totalTime'])
                    print 'Caminos entre las ciudades: '
                    for relationship in range(0, len(office['relationships'])):
                        print '\t' + str(office['relationships'][relationship]['name'])
                        total_cost = + float(office['relationships'][relationship]['costeAsociado'])
                        relationships.append(str(office['relationships'][relationship]['name']))
                    print 'Nodos por los que pasa: '
                    for nodo in range(0, len(office['nodes'])):
                        print '\t' + str(office['nodes'][nodo]['name'])
                        route.append(str(office['nodes'][nodo]['name']))
                    for nodo in range(0, len(office['nodes'])):
                        if nodo >= len(office['nodes'])-1:
                            print str(office['nodes'][nodo]['name'])
                        else:
                            print str(office['nodes'][nodo]['name']) + ' --[' + str(office['relationships'][nodo]['name']) + ']->',
        session.close()
        return dict({'type': type, 'total_cost': total_cost, 'total_time': total_time, 'relationships': relationships, 'route': route})


def new_package(path_info):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "bleh"))
    with driver.session() as session:

        aux = -1
        for office in session.run('MATCH (p:Oficina {name: $name})-[:Esta]-(s:Vehiculo) '
                             'RETURN s.ID limit 1', name=path_info.get('route')[0]):
            aux = office['s.ID']

        session.sync()
        if aux is -1:
            print 'No hay vehiculos disponibles!'
            return
        else:
            print 'Hay vehiculos!'
        for office in session.run(
                'match (ID:ID) '
                'set ID.PID = ID.PID + 1 '
                'return ID.PID'):
            ID = office['ID.PID']
            print 'se ha acabado ID'
            print ID
        session.sync()
        tipo = path_info.get('type')
        print tipo
        coste_total = path_info.get('total_cost')
        print coste_total
        tiempo_total = path_info.get('total_time')
        print tiempo_total
        ruta = path_info.get('route')
        print ruta
        relaciones = path_info.get('relationships')
        print relaciones

        session.run(
            'MERGE (package:Paquete {ID: $ID, tipo: $tipo, coste_total: $coste_total, '
            'tiempo_total: $tiempo_total, ruta: $ruta, relaciones: $relaciones}) ',
            ID=ID, tipo=tipo, coste_total=coste_total,
            tiempo_total=tiempo_total, ruta=ruta,
            relaciones=relaciones)
        session.sync()
        print 'Paso merge'
        destino = path_info.get('route')[-1]
        print destino
        session.run('MATCH (s:Vehiculo {ID:$ID_vehiculo}), (p:Paquete {ID:$ID}) '
               'CREATE (p)-[:Transporta]->(s) '
               'SET s.ruta = $ruta, s.destino = $destino',
               ID_vehiculo=aux, destino=destino, ruta=ruta, ID=ID)
        session.sync()
        print 'se ha acabado CREATE'
        session.close()

"""
Preguntas:

 - ¿Las rutas son todos los puntos por los que pasa un paquete, no? ¿Como lo podriamos hacer?, solo tenemos hecho que calcule el mejor tiempo pero no nos da los puntos
    
si, hay que cambiar la funcion que tenemos con algun WHEN/WITH hay que ver como sacar la informacion. Hay que delimitar bien las consultas para que sea optimo.

 - ¿Como organizamos la flota? ¿Como variables de la oficina o como nodos conectados a las oficinas?
  
Nodos generalistas (un coche es un barco, avion y tren) y estan conectado mediante una relacion con la oficina,
punto intermedio o lo que toque y asi sabemos como avanza en el camino.
  
 - ¿Como organizamos los paquetes? ¿Como variables del vehiculo o como nodos conectados a un vehiculo?
 
Son nodos unidos a los vehiculos que los transportan y al cliente que los ha enviado. Una vez se ha realizado el envio,
la relacion con la oficina se dehace y solo queda la del usuario.
 
 - ¿Tenemos que tener una query para pedir informacion del paquete?
 
si, tiene que tener informacion de la ruta. (por donde ha pasado y por donde va a pasar)
 
 - ¿Diferencia entre gestionar y consultar? en el punto de los clientes
 
Gestionar -> guardar datos en la base de datos
consultar -> queries en la base de datos
 
 
"""


# Cosas que vamos a necesitar:
# 1. Puntos de entrega (+ info servicios disponibles)
# 2. Puntos de recogida (+ info servicios disponibles)
# 3. Clientes
# 4. Transportes (Carretera, Aereo, Maritimo, Ferrocarril) (+ info tiempos y costes)
# 5. Plataformas intermedias
# 6. Tipos de envio (Urgente, Urgente madrugadores, Urgente primera hora, Envio normal, Envio economico)

# https://neo4j.com/docs/cypher-refcard/current/

# Ruta mas corta
# http://stackoverflow.com/questions/26458589/shortest-path-through-weighted-graph
# http://stackoverflow.com/questions/28032830/cypher-query-to-return-nodes-in-path-order

if __name__ == "__main__":

    path_info = find_shortest_path('Oporto', 'Barcelona', 'economico')
    new_package(path_info)