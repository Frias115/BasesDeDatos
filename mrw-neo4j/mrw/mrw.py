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


def new_package(path_info, user_id):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "bleh"))
    with driver.session() as session:
        posicion_actual = path_info.get('route')[0]
        destino = path_info.get('route')[-1]
        tipo = path_info.get('type')
        aux = []

        for office in session.run('MATCH (p:Oficina {name: $name})-[:Esta]-(s:Vehiculo) '
                             'RETURN s as nodes', name=posicion_actual):
            aux.append(office['nodes'])

        session.sync()
        if aux is []:
            print 'No hay vehiculos disponibles!'
            return
        else:
            disponible = False
            id_auxiliar = -1
            for vehiculo in aux:
                if str(vehiculo['destino']) is '':
                    disponible = True
                    vehicle_ID = str(vehiculo['ID'])
                elif str(vehiculo['destino']) == destino and vehiculo['tipo'] == tipo:
                    disponible = True
                    id_auxiliar = str(vehiculo['ID'])
            if disponible is False:
                print 'No hay vehiculos disponibles!'
                return
            else:
                print 'Hay vehiculos!'
            if id_auxiliar is not -1:
                vehicle_ID = id_auxiliar

        for office in session.run(
                'match (ID:ID) '
                'set ID.PID = ID.PID + 1 '
                'return ID.PID'):
            ID = office['ID.PID']
        session.sync()


        coste_total = path_info.get('total_cost')
        tiempo_total = path_info.get('total_time')
        ruta = path_info.get('route')
        relaciones = path_info.get('relationships')

        session.run(
            'MERGE (package:Paquete {ID: $ID, tipo: $tipo, coste_total: $coste_total, '
            'tiempo_restante: $tiempo_total, ruta: $ruta, relaciones: $relaciones, '
            'posicion_actual: $posicion_actual, id_vehiculo:$id_vehiculo, pagado:False}) ',
            ID=ID, tipo=tipo, coste_total=coste_total,
            tiempo_total=tiempo_total, ruta=ruta,
            relaciones=relaciones, posicion_actual=posicion_actual, id_vehiculo=vehicle_ID)
        session.sync()

        session.run('MATCH (s:Vehiculo {ID:$ID_vehiculo}), (p:Paquete {ID:$ID}), (u:Cliente {ID:$user_id}) '
               'CREATE (p)-[:Transporta]->(s), (p)-[:Pertenece]->(u) '
               'SET s.ruta = $ruta, s.destino = $destino, s.tipo = $tipo',
               ID_vehiculo=vehicle_ID, destino=destino, ruta=ruta, ID=ID, user_id=user_id, tipo=tipo)
        session.sync()
        print 'Se ha cargado tu paquete al vehiculo'
        session.close()
    return vehicle_ID


def deliver_packages(vehicle_id):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "bleh"))
    with driver.session() as session:
        session.run('MATCH (oficinaDestino:Oficina {name:vehicle.destino}), '
                    '(vehicle:Vehiculo {ID:$ID})-[c:Esta]-(:Oficina), (vehicle)-[f:Transporta]-(paquete:Paquete) '
                    'CREATE (paquete)-[:Almacenado]->(oficinaDestino) '
                    'SET paquete.posicion_actual = oficinaDestino.name, paquete.tiempo_restante = 0, '
                    'vehicle.destino = "", vehicle.ruta = "", vehicle.posicionActual = vehicle.origen, vehicle.tipo = "" '
                    'DELETE f', ID=vehicle_id)
        session.run('MATCH (vehicle:Vehiculo {ID:$ID})-[c:Esta]-(:Oficina), (oficinaOrigen:Oficina {name:vehicle.origen}) '
                    'CREATE (vehicle)-[:Esta]->(oficinaOrigen) '
                    'DELETE c', ID=vehicle_id)
        session.sync()


def charge_package(package_id):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "bleh"))
    with driver.session() as session:
        session.run('MATCH (p:Paquete {ID:$package_id}) '
                    'SET p.pagado = True', package_id=package_id)
        session.sync()


def hand_package(package_id):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "bleh"))
    with driver.session() as session:
        session.run('MATCH (p:Paquete {ID:$package_id, pagado:True})-[u:Almacenado]-() '
                    'DELETE u', package_id=package_id)
        session.sync()


def check_packages_type(client_id=None):
    type = raw_input('¿Que tipo de paquete quieres ver? \n0: Todos\n1: Urgente4h\n2: Urgente6h\n3: Urgente8h\n4: Normal12h\n5: Economico')
    type = int(type)
    if type == 0:
        type=None
    elif type == 1:
        type = 'urgente4h'
    elif type == 2:
        type = 'urgente6h'
    elif type == 3:
        type = 'urgente8h'
    elif type == 4:
        type = 'normal12h'
    elif type == 5:
        type = 'economico'
    else:
        print 'No valido'
        return
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "bleh"))
    with driver.session() as session:
        packages = []
        if type is None:
            if client_id is None:
                for package in session.run('MATCH (p:Paquete) return p'):
                    packages.append(package)
            else:
                print 'Los paquetes del usuario ' + str(client_id) + ' son:'
                for package in session.run('MATCH (p:Paquete)-[:Pertenece]-(:Cliente {ID:$client_id}) return p', client_id=client_id):
                    packages.append(package)
        else:
            if client_id is None:
                for package in session.run('MATCH (p:Paquete {tipo:$type}) return p', type=type):
                    packages.append(package)
            else:
                print 'Los paquetes del usuario ' + str(client_id) + ' son:'
                for package in session.run('MATCH (p:Paquete {tipo:$type})-[:Pertenece]-(:Cliente {ID:$client_id}) return p', client_id=client_id, type=type):
                    packages.append(package)
        for package in packages:
            print 'ID: ' + str(package['p']['ID']) + ' Tipo: ' + str(package['p']['tipo']) + ' Coste: ' \
                  + str(package['p']['coste_total']) + ' Tiempo restante: ' + str(package['p']['tiempo_restante']) \
                  + ' Ruta: ' + str(package['p']['ruta']) + ' Relaciones: ' + str(package['p']['relaciones']) \
                  + ' Posicion actual: ' + str(package['p']['posicion_actual']) + ' ID vehiculo: ' + str(
                package['p']['id_vehiculo']) \
                  + ' Pagado: ' + str(package['p']['pagado'])


def check_packages_charged(client_id=None):
    charged = raw_input('¿Que tipo de paquete quieres ver? \n0: Todos\n1: Pagados\n2: No pagados')
    charged = int(charged)
    if charged == 0:
        charged=None
    elif charged == 1:
        charged = True
    elif charged == 2:
        charged = False
    else:
        print 'No valido'
        return
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "bleh"))
    with driver.session() as session:
        packages = []
        if charged is None:
            if client_id is None:
                for package in session.run('MATCH (p:Paquete) return p'):
                    packages.append(package)
            else:
                print 'Los paquetes del usuario ' + str(client_id) + ' son:'
                for package in session.run('MATCH (p:Paquete)-[:Pertenece]-(:Cliente {ID:$client_id}) return p', client_id=client_id):
                    packages.append(package)
        else:
            if client_id is None:
                for package in session.run('MATCH (p:Paquete {pagado:$charged}) return p', charged=charged):
                    packages.append(package)
            else:
                print 'Los paquetes del usuario ' + str(client_id) + ' son:'
                for package in session.run('MATCH (p:Paquete {pagado:$charged})-[:Pertenece]-(:Cliente {ID:$client_id}) return p', client_id=client_id, charged=charged):
                    packages.append(package)
        total_import = 0
        for package in packages:
            if not bool(package['p']['pagado']):
                total_import = total_import + float(package['p']['coste_total'])
            print 'ID: ' + str(package['p']['ID']) + ' Tipo: ' + str(package['p']['tipo']) + ' Coste: ' \
                  + str(package['p']['coste_total']) + ' Tiempo restante: ' + str(package['p']['tiempo_restante']) \
                  + ' Ruta: ' + str(package['p']['ruta']) + ' Relaciones: ' + str(package['p']['relaciones']) \
                  + ' Posicion actual: ' + str(package['p']['posicion_actual']) + ' ID vehiculo: ' + str(
                package['p']['id_vehiculo']) \
                  + ' Pagado: ' + str(package['p']['pagado'])
        print 'Importe total debido: ' + str(total_import)

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


 - ¿Hay que hacer index? De que?
 
 Si, de algo a lo que hagamos muchas consultas, hay que mirarlo
 
 - ¿Un vehiculo solo cubre una ruta al final?
 
 SI de punta a punta y nos olvidamos
 
 Cuando un vehiculo acaba su ruta lo 'reinciamos'
 
 Y no es necesario hacerse la funcioon de que avance, pero lo podemos hacer si queremos
 
 ¿Eliminamos los booleamos de la oficina que no usamos?
 
 
"""

if __name__ == "__main__":

    path_info = find_shortest_path('Oporto', 'Sevilla', 'economico')
    new_package(path_info, 1)

    path_info = find_shortest_path('Oporto', 'Sevilla', 'economico')
    new_package(path_info, 2)

    path_info = find_shortest_path('Oporto', 'Barcelona', 'economico')
    new_package(path_info, 3)

    path_info = find_shortest_path('Oporto', 'Barcelona', 'normal12h')
    new_package(path_info, 4)

    path_info = find_shortest_path('Oporto', 'Mallorca', 'economico')
    new_package(path_info, 1)

    path_info = find_shortest_path('Oporto', 'Barcelona', 'economico')
    new_package(path_info, 2)

    vehiculo = new_package(find_shortest_path('Oporto', 'Sevilla', 'economico'), 3)

    deliver_packages(vehiculo)

    path_info = find_shortest_path('Oporto', 'Mallorca', 'normal12h')
    new_package(path_info, 4)

    charge_package(1)
    charge_package(4)
    hand_package(1)
    hand_package(2)

    check_packages_charged(2)