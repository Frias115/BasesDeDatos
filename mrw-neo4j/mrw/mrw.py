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


# Cosas que vamos a necesitar:
# 1. Puntos de entrega (+ info servicios disponibles)
# 2. Puntos de recogida (+ info servicios disponibles)
# 3. Clientes
# 4. Transportes (Carretera, Aereo, Maritimo, Ferrocarril) (+ info tiempos y costes)
# 5. Plataformas intermedias
# 6. Tipos de envio (Urgente, Urgente madrugadores, Urgente primera hora, Envio normal, Envio economico)

if __name__ == "__main__":
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "bleh"))

    with driver.session() as session:
        session.write_transaction(add_friends, "Arthur", "Guinevere")
        session.write_transaction(add_friends, "Arthur", "Lancelot")
        session.write_transaction(add_friends, "Arthur", "Merlin")
        session.read_transaction(print_friends, "Arthur")

