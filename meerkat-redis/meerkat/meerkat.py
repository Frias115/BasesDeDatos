import redis
import random
import time
from threading import Thread
my_server = redis.StrictRedis(host='localhost', port=6379, db=0)


def get_variable(variable_name):
    response = my_server.get(variable_name)
    return response


def set_variable(variable_name, variable_value=None):
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


def set_user(username=None, password=None):

    if not my_server.exists('ID'):
        set_variable('ID', 0)

    ID = get_variable('ID')

    set_variable(ID, ID)
    set_variable(str(ID) + '.username', username)
    set_variable(str(ID) + '.password', password)
    #Cookie
    set_variable(str(ID) + '.cookie', random.randint(0, 99999))
    my_server.expire(str(ID) + '.cookie', 604800)

    my_server.incr('ID')


def add_follower(ID, *list_of_follower_IDs):

    my_server.sadd(str(ID) + '.followers', list_of_follower_IDs)


def add_to_following(ID, *list_of_IDs_to_follow):

    my_server.sadd(str(ID) + '.following', list_of_IDs_to_follow)


def notify_streaming(ID):
    time.sleep(2)
    print "Hola?"
    subscription = my_server.pubsub()

    # subscription.subscribe(0)

    my_server.publish(str(ID), 'I started streaming, join me!')

    # subscription.close()


def get_messages_for_id(ID):
    print "Me estoy ejecutando"
    subscription = my_server.pubsub()
    subscription.subscribe(str(ID))

    while True:
        message = subscription.get_message()
        if message:
            if message['data'] == "KILL":
                print 'i\'m closing'
                break
            print message


def generate_following(ID):
    list_of_following = my_server.sscan(str(ID) + '.following')
    for followingID in list_of_following:
        print followingID
        print type(list_of_following)
        thread = Thread(target=get_messages_for_id, args=(followingID, ))
        thread.start()


def kill_following(ID):
    list_of_following = my_server.sscan(str(ID) + '.following')
    for followingID in list_of_following:
        print str(followingID)
        my_server.publish(str(followingID),'KILL')

if __name__ == "__main__":

    set_user('Rober', 'bleh')
    set_user('Sergio', 'calvo')
    add_follower(0, 1)
    add_to_following(1, 0)
    generate_following(1)
    notify_streaming(0)
    time.sleep(3)
    print 'Vamos a matarlos...'
    kill_following(1)
