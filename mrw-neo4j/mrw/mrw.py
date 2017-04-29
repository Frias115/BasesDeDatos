# coding=utf-8
from neo4j.v1 import GraphDatabase


def show_services(postal_office=None):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "bleh"))
    with driver.session() as session:
        resultado = []
        if postal_office is None:
            for office in session.run('MATCH (a:Oficina) RETURN a'):
                resultado.append(office)
        else:
            # So that code remains the same even if we don't receive a list of offices
            aux_list = []
            if type(postal_office) is not list:
                aux_list.append(postal_office)
                postal_office = aux_list
            for p_o in range(0, len(postal_office)):
                for office in session.run('MATCH (a:Oficina {name: $name}) RETURN a', name=postal_office[p_o]):
                    resultado.append(office)

        for office in resultado:
            print('Oficina: ' + str(office['a']['name']) +
                  ' \n\tEnvio urgente 4h: ' + str(office["a"]['urgente4h']) +
                  ' \n\tEnvio urgente 6h: ' + str(office["a"]['urgente6h']) +
                  ' \n\tEnvio urgente 8h: ' + str(office["a"]['urgente8h']) +
                  ' \n\tEnvio normal 12h: ' + str(office["a"]['normal12h']) +
                  ' \n\tEnvio economico:  ' + str(office["a"]['economico']))
        session.sync()


def find_shortest_path(departure, arrival, type):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "bleh"))
    with driver.session() as session:

        # Checking shipping types available in a office
        for office in session.run(
                'Match (a:Oficina {name: $departure}) RETURN a', departure=departure):
            if not office['a'][str(type)]:
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
        offices = []
        if time is 0:
            # Finding the cheapest path between two offices
            for office in session.run(
                    'MATCH a = (departure:Oficina {name: $departure})-[:Carretera | Ferroviario | Maritimo | Aereo*1..6]-(arrival:Oficina {name: $arrival}) '
                    'RETURN relationships(a) as relationships, nodes(a) as nodes, '
                    'REDUCE(cost=0, r in relationships(a) | cost + r.costeAsociado) as totalCost '
                    'order by totalCost ASC limit 1', departure = departure, arrival = arrival):
                print 'coste estimado: ' + str(office['totalCost'])
                total_cost = float(office['totalCost'])
                offices.append(office)

        else:
            # Finding the fastest path between two offices
            # (the shipment must be faster that the time available for the type of shipment chosen)
            for office in session.run(
                    'MATCH a = (departure:Oficina {name: $departure})-[:Carretera | Ferroviario | Maritimo | Aereo*1..6]-(arrival:Oficina {name: $arrival}) '
                    'RETURN relationships(a) as relationships, nodes(a) as nodes, '
                    'REDUCE(tiempo=0, r in relationships(a) | tiempo + r.tiempo) as totalTime '
                    'order by totalTime ASC limit 1', departure = departure, arrival = arrival):

                if office["totalTime"] > time:
                    print 'No existe una ruta valida que cumpla ese tipo de envio.'
                    return
                else:
                    print 'Tiempo estimado: ' + str(office['totalTime'])
                    total_time = float(office['totalTime'])
                offices.append(office)

        # Printing route information
        for office in offices:
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
        session.sync()
        return dict({'type': type, 'total_cost': total_cost, 'total_time': total_time, 'relationships': relationships, 'route': route})


def new_package(path_info, user_id):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "bleh"))
    with driver.session() as session:
        posicion_actual = path_info.get('route')[0]
        destino = path_info.get('route')[-1]
        tipo = path_info.get('type')
        aux = []
        # Checking for relationships between office and vehicles
        for office in session.run('MATCH (p:Oficina {name: $name})-[:Esta]-(s:Vehiculo) '
                             'RETURN s as nodes', name=posicion_actual):
            aux.append(office['nodes'])

        session.sync()
        if aux is []:
            print 'No hay vehiculos disponibles!'
            return
        else:
            # Check if a vehicle is free or has the same route and type of shipping
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

        # retrieving the package id
        for office in session.run(
                'MATCH (ID:ID) '
                'SET ID.PID = ID.PID + 1 '
                'RETURN ID.PID'):
            ID = office['ID.PID']
        session.sync()

        coste_total = path_info.get('total_cost')
        tiempo_total = path_info.get('total_time')
        ruta = path_info.get('route')
        relaciones = path_info.get('relationships')

        # Creating the package
        session.run(
            'MERGE (package:Paquete {ID: $ID, tipo: $tipo, coste_total: $coste_total, '
                    'tiempo_restante: $tiempo_total, ruta: $ruta, relaciones: $relaciones, '
                    'posicion_actual: $posicion_actual, id_vehiculo:$id_vehiculo, pagado:False}) ',
            ID=ID, tipo=tipo, coste_total=coste_total,
            tiempo_total=tiempo_total, ruta=ruta,
            relaciones=relaciones, posicion_actual=posicion_actual, id_vehiculo=vehicle_ID)
        session.sync()
        # Creating indexes for package-related queries
        session.run('CREATE INDEX ON :Paquete(ID)')
        session.run('CREATE INDEX ON :Paquete(tipo)')
        session.run('CREATE INDEX ON :Paquete(coste_total)')
        session.run('CREATE INDEX ON :Paquete(pagado)')
        session.sync()
        # Creating relationships between package, vehicle and client
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
        # Moving package to destination office
        # Removing relationship between package and vehicle
        # Resetting vehicle and moving it to origin office
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
        # Setting paid attribute from package to True
        session.run('MATCH (p:Paquete {ID:$package_id}) '
                    'SET p.pagado = True', package_id=package_id)
        session.sync()


def hand_package(package_id):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "bleh"))
    with driver.session() as session:
        # Deleting relationship between package and destination office
        session.run('MATCH (p:Paquete {ID:$package_id, pagado:True})-[u:Almacenado]-() '
                    'DELETE u', package_id=package_id)
        session.sync()


def check_packages_type(client_id=None):
    # Asking user what type of shipment it wants to check
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
                # Getting every package
                for package in session.run('MATCH (p:Paquete) return p'):
                    packages.append(package)
            else:
                # Getting every package belonging to a certain client
                print 'Los paquetes del usuario ' + str(client_id) + ' son:'
                for package in session.run('MATCH (p:Paquete)-[:Pertenece]-(:Cliente {ID:$client_id}) return p', client_id=client_id):
                    packages.append(package)
        else:
            if client_id is None:
                # Getting every package of a certain shipment type
                for package in session.run('MATCH (p:Paquete {tipo:$type}) return p', type=type):
                    packages.append(package)
            else:
                # Getting every package of a certain shipment type belonging to a certain client
                print 'Los paquetes del usuario ' + str(client_id) + ' son:'
                for package in session.run('MATCH (p:Paquete {tipo:$type})-[:Pertenece]-(:Cliente {ID:$client_id}) return p', client_id=client_id, type=type):
                    packages.append(package)
        # Printing package information
        for package in packages:
            print 'ID: ' + str(package['p']['ID']) + ' Tipo: ' + str(package['p']['tipo']) + ' Coste: ' \
                  + str(package['p']['coste_total']) + ' Tiempo restante: ' + str(package['p']['tiempo_restante']) \
                  + ' Ruta: ' + str(package['p']['ruta']) + ' Relaciones: ' + str(package['p']['relaciones']) \
                  + ' Posicion actual: ' + str(package['p']['posicion_actual']) + ' ID vehiculo: ' + str(
                package['p']['id_vehiculo']) \
                  + ' Pagado: ' + str(package['p']['pagado'])


def check_packages_charged(client_id=None):
    # Asking user what type of package it wants to check
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
                # Getting every package
                for package in session.run('MATCH (p:Paquete) return p'):
                    packages.append(package)
            else:
                # Getting every package belonging to a certain client
                print 'Los paquetes del usuario ' + str(client_id) + ' son:'
                for package in session.run('MATCH (p:Paquete)-[:Pertenece]-(:Cliente {ID:$client_id}) return p', client_id=client_id):
                    packages.append(package)
        else:
            if client_id is None:
                # Getting every package of a certain charged type
                for package in session.run('MATCH (p:Paquete {pagado:$charged}) return p', charged=charged):
                    packages.append(package)
            else:
                # Getting every package of a certain charged type belonging to a certain client
                print 'Los paquetes del usuario ' + str(client_id) + ' son:'
                for package in session.run('MATCH (p:Paquete {pagado:$charged})-[:Pertenece]-(:Cliente {ID:$client_id}) return p', client_id=client_id, charged=charged):
                    packages.append(package)
        total_import = 0
        # Printing package information
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


def create_indexes():
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "bleh"))
    # Creating indexes because neo4j doesn't allow to create them in *.cypher database generation file
    # Has to be called at the beginning of main
    with driver.session() as session:
        session.run('CREATE INDEX ON :Oficina(name);')
        session.run('CREATE INDEX ON :puntoIntermedio(name);')
        session.run('CREATE INDEX ON :Vehiculo(ID);')
        session.run('CREATE INDEX ON :Vehiculo(origen);')
        session.run('CREATE INDEX ON :Cliente(ID);')
        session.run('CREATE INDEX ON :Carretera(tiempo);')
        session.run('CREATE INDEX ON :Carretera(costeAsociado);')
        session.run('CREATE INDEX ON :Aereo(tiempo);')
        session.run('CREATE INDEX ON :Aereo(costeAsociado);')
        session.run('CREATE INDEX ON :Ferroviario(tiempo);')
        session.run('CREATE INDEX ON :Ferroviario(costeAsociado);')
        session.run('CREATE INDEX ON :Maritimo(tiempo);')
        session.run('CREATE INDEX ON :Maritimo(costeAsociado);')
        session.sync()


if __name__ == "__main__":

    create_indexes()
    show_services('Oporto')
    info = find_shortest_path('Oporto', 'Barcelona', 'normal12h')
    vehicle_id = new_package(info, 1)
    deliver_packages(vehicle_id)
    charge_package(1)
    hand_package(1)
    check_packages_type(1)
    check_packages_charged(1)