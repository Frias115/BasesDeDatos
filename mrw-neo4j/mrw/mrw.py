# coding=utf-8
from neo4j.v1 import GraphDatabase



def add_friends(tx, name, friend_name):
    tx.run("MERGE (a:Person {name: $name}) "
           "MERGE (a)-[:KNOWS]->(friend:Person {name: $friend_name})",
           name=name, friend_name=friend_name)


def print_friends(tx, name):
    for record in tx.run("MATCH (a:Person)-[:KNOWS]->(friend) WHERE a.name = $name "
                         "RETURN friend.name ORDER BY friend.name", name=name):
        print(record["friend.name"])

#flush                   match (n)-[r]-(m) delete n,r,m
#flush nodo sin relacion match (n) delete n


def show_services(postal_office=None):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "bleh"))
    with driver.session() as session:
        session.read_transaction(_show_services, postal_office)


def _show_services(tx, postal_office):
    if postal_office is None:
        for office in tx.run('MATCH (a:Oficina) RETURN a.urgente4h, a.name, a.urgente6h, a.urgente8h, a.normal12h, a.economico'):
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
            for office in tx.run('MATCH (a:Oficina {name: $name}) RETURN a.urgente4h, a.name, a.urgente6h, a.urgente8h, a.normal12h, a.economico', name=postal_office[p_o]):
                print('Oficina: ' + str(office['a.name']) +
                      ' \n\tEnvio urgente 4h: ' + str(office["a.urgente4h"]) +
                      ' \n\tEnvio urgente 6h: ' + str(office["a.urgente6h"]) +
                      ' \n\tEnvio urgente 8h: ' + str(office["a.urgente8h"]) +
                      ' \n\tEnvio normal 12h: ' + str(office["a.normal12h"]) +
                      ' \n\tEnvio economico:  ' + str(office["a.economico"]))


def find_shortest_path(departure, arrival):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "bleh"))
    with driver.session() as session:
        session.read_transaction(_find_shortest_path, departure, arrival)


def _find_shortest_path(tx, departure, arrival):
    for office in tx.run(
        'MATCH a = (departure:Oficina {name: $departure})-[*1..6]-(arrival:Oficina {name: $arrival})'
        ' RETURN a as shortestPath,'
        ' REDUCE(tiempo=0, r in relationships(a) | tiempo + r.tiempo) as totalTime order by totalTime ASC limit 3', departure=departure, arrival=arrival):
        print office


"""
Preguntas:

 - ¿Las rutas son todos son puntos por los que pasa un paquete, no? ¿Como lo podriamos hacer?, solo tenemos hecho que calcule el mejor tiempo pero no nos da los puntos



 - ¿Como organizamos la flota? ¿Como variables de la oficina o como nodos conectados a las oficinas?
  
  
  
 - ¿Como organizamos los paquetes? ¿Como variables del vehiculo o como nodos conectados a un vehiculo?
 
 
 
 - ¿Tenemos que tener una query para pedir informacion del paquete?
 
 
 
 - ¿Diferencia entre gestionar y consultar? en el punto de los clientes
 
 
 
 
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

if __name__ == "__main__":

    find_shortest_path('Oporto', 'Mallorca')