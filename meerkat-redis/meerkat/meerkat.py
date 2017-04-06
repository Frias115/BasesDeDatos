import redis
import random
import time
from threading import Thread
from operator import itemgetter

my_server = redis.StrictRedis(host='localhost', port=6379, db=0)
iteracion = 0
index = []

def get_variable(variable_name):
    response = my_server.get(variable_name)
    return response


def set_variable(variable_name, variable_value=None):
    my_server.set(variable_name, variable_value)


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


def add_follower(ID, list_of_follower_IDs):

    my_server.sadd(str(ID) + '.followers', list_of_follower_IDs)


def add_to_following(ID, list_of_IDs_to_follow):

    my_server.sadd(str(ID) + '.following', list_of_IDs_to_follow)


def notify_streaming(ID):
    time.sleep(2)
    subscription = my_server.pubsub()
    # subscription.subscribe(0)
    my_server.publish(str(ID), 'I started streaming, join me!')
    # subscription.close()

def get_messages_for_id(ID):
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
    list_of_following = my_server.smembers(str(ID) + '.following')
    for followingID in list_of_following:
        thread = Thread(target=get_messages_for_id, args=(followingID, ))
        thread.start()


def kill_following(ID):
    print 'Killing threads'
    list_of_following = my_server.smembers(str(ID) + '.following')
    for followingID in list_of_following:
        my_server.publish(str(followingID),'KILL')


"""
- Retransmisiones activas
- Retransmisiones finalizadas
    - Hashtags ID
Sistema de busqueda teniendo en cuenta id o hashtag y que te diga si esta activa o no la retransmision

id.retransmision.name       =   ['video1'    ,   'video2']
id.retransmission.status    =   [   0        ,       1   ]
id.retransmision.date       =   ['01.01.17'  , '02.02.17']
id.retransmission.likes     =   [  '4'       ,      '3'  ]
id.retransmissions.id_likes =   [[1, 2, 3, 4],  [2, 3, 4]]

hashtag.retransmission.id =     [2, 3, 4, 5]

Busqueda segun ID
si le das un ID, te tiene que sacar todos sus videos ordenados por fecha. 

"""



"""
PREGUNTAS:

- Esta bien lo de los threads en los avisos? Sip, es valido si funciona


- Fecha que tipo de dato es? da lo mismo


- Se podria hacer una carga de datos de las retranmisiones en una lista y luego utilizarla o hay que hacerlo sobre bd? mejor sobre bd


- Los datos en retransmision son listas, valen? hay que aplicar lo que nos ha dicho


- Preguntas sobre los likes en las retransmisiones, meterlo dento de la estructura
"""


def add_retransmission(ID, name, date, id_likes=[], hashtags = [], status=1):
    retransmission_index = my_server.zadd(str(ID) + '.retransmission.index', date, name)
    if retransmission_index is 0:
        print 'El nombre ya existe! Elige otro.'
    else:
        dictionary = {'date': date, 'status': status, 'id_likes': id_likes, 'hashtags': hashtags}
        my_server.hmset(str(ID) + '.retransmission.info.' + name, dictionary)
        for i in hashtags:
            my_server.sadd('hashtag.' + str(i), str(ID) + '.retransmission.index.' + name)


def get_retransmissions_by_id(id, max_date = 99999999, min_date = 0):
    iteracion = 0
    video_list = []
    list_index = str(id) + '.retransmission.index'
    index = my_server.zrevrangebyscore(list_index,max=max_date, min=min_date)
    for i in range(0, 3):
        var = index[i]
        video = []
        video.append(var)
        info = my_server.hvals(str(id) + '.retransmission.info.' + str(var))
        for j in info:
            video.append(j)

        video_list.append(video)
    print video_list


def get_more_retransmissions(id):
    video_list = []
    for i in range(0, 3):
        var = index.pop()
        video = []
        video.append(var)
        info = my_server.hvals(str(id) + '.retransmission.info.' + str(var))
        for j in info:
            video.append(j)

        video_list.append(video)
    sorted_list = sorted(video_list, key=itemgetter(1))
    iteracion += 1
    print sorted_list

if __name__ == "__main__":

    set_user('Rober', 'bleh')
    set_user('Sergio', 'calvo')
    set_user('Ramon', 'pesado')
    set_user('Diego', 'onice')
    """
    add_follower(0, [1, 2, 3])
    add_to_following(1, 0)
    add_to_following(2, 0)
    add_to_following(3, 0)
    generate_following(1)
    generate_following(2)
    generate_following(3)
    notify_streaming(0)
    time.sleep(3)
    kill_following(1)
    kill_following(2)
    kill_following(3)
"""

    my_server.flushdb()
    add_retransmission(0, 'prueba', 20170404, [0, 1], ['cuki', 'mono', 'perro'])
    add_retransmission(0, 'prueba1', 20170403, [2, 1], ['flor', 'abeja', 'blancoynegro'], 0)
    add_retransmission(0, 'prueba2', 20170405, [2, 1], ['marica', 'peleon', 'cachondo'], 0)
    add_retransmission(0, 'prueba3', 20170402, [0, 1], ['cactus', 'pincha', 'sangre'])
    add_retransmission(0, 'prueba4', 20170401, [2, 1], ['street', 'b&w', 'photography'])
    add_retransmission(0, 'prueba5', 20170406, [2, 1], ['selfie', 'stick', 'sucks'], 0)
    get_retransmissions_by_id(0)
    # get_more_retransmissions(0)