import redis
import random

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)

def getVariable(variable_name):
    my_server = redis.Redis(connection_pool=pool)
    response = my_server.get(variable_name)

    return response

def setVariable(variable_name, variable_value = None):
    my_server = redis.Redis(connection_pool=pool)
    my_server.set(variable_name, variable_value)



"""

DONE
El sistema debera ser capaz de gestionar la informacion relativa a la conexion de los
usuarios (nombre de usuario, identificador del usuario y contrasena). La contrasena se
podra guardar en formato plano.

DONE
El identificador del usuario se generara de forma automatica en la base de datos. Los
identificadores seran numeros enteros que se asignaran de forma incremental siguiendo el
orden en el que los usuarios se registran.

DONE
Se debera gestionar asi mismo los identificadores de las cookies que permiten entrar a los
usuarios sin necesidad de realizar la identificacion de nuevo. Estos identificadores deberan
expirar a los 7 dias de su creacion.

DONE
Se debera almacenar la informacion relativa a los seguidores que tiene un usuario

DONE
Asi mismo se debera almacenar la informacion relativa a las cuentas que sigue un usuario.

DONE
Los usuarios que esten siguiendo a otros usuarios deberan ser notificados cada
vez que alguno de los usuarios que siguen realicen una retransmision.


Se debera almacenar la informacion relativa a las retrasmisiones que realiza el usuario de
modo que se pueda acceder a las retransmisiones activas y tambien las retransmisiones ya
finalizadas


Las retrasmisiones podran ser accedidas a traves del identificador del usuario que
lo retrasmite.


Asi mismo, las retransmisiones contaran con una serie de hashtags que lo
identifican y que permitiran realizar busquedas sobre las retransmisiones en
funcion de sus hashtags.


Ademas de poder consultar las retransmisiones por identificador y/o hashtags,
tambien se debe permitir especificar si estan activas o no.

"""

def setUser(username = None, password = None):

    my_server = redis.Redis(connection_pool=pool)
    if not my_server.exists('ID'):
        setVariable('ID', 0)

    ID = getVariable('ID');

    setVariable(ID, ID)
    setVariable(str(ID) + '.username' , username)
    setVariable(str(ID) + '.password' , password)
    #Cookie
    setVariable(str(ID) + '.cookie' , random.randint(0, 99999))
    my_server.expire(str(ID) + '.cookie', 604800)


    my_server.incr('ID')

def addFollower(ID, *list_of_follower_IDs):
    my_server = redis.Redis(connection_pool=pool)

    my_server.sadd(str(ID) + '.followers', list_of_follower_IDs)

    my_server.pubsub(list_of_follower_IDs)

def addToFollowing(ID, *list_of_IDs_to_follow):
    my_server = redis.Redis(connection_pool=pool)

    my_server.sadd(str(ID) + '.following', list_of_IDs_to_follow)

def notifyStreaming(ID):
    my_server = redis.Redis(connection_pool=pool)

    my_server.publish(ID, 'I started streaming, join me!')



if __name__ == "__main__":

    setUser('rober', 'bleh')






























