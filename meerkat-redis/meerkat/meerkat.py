import redis
import random
import time
from threading import Thread
import ast

my_server = redis.StrictRedis(host='localhost', port=6379, db=0)
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
    # Cookie
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
        thread = Thread(target=get_messages_for_id, args=(followingID,))
        thread.start()


def kill_following(ID):
    print 'Killing threads'
    list_of_following = my_server.smembers(str(ID) + '.following')
    for followingID in list_of_following:
        my_server.publish(str(followingID), 'KILL')


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


def add_retransmission(ID, name, date, hashtags=[]):
    retransmission_index = my_server.zadd(str(ID) + '.retransmission.index', date, name)
    if retransmission_index is 0:
        print 'El nombre ya existe! Elige otro.'
    else:
        dictionary = {'date': date, 'status': 1, 'number_of_likes': 0, 'id_likes': [],
                      'hashtags': hashtags, 'comments': []}
        my_server.hmset(str(ID) + '.retransmission.info.' + name, dictionary)
        for i in hashtags:
            my_server.zadd('hashtag.' + str(i), date, str(ID) + '.retransmission.info.' + name)


def get_retransmissions_by_id(id, max_date=99999999, min_date=0):
    set_variable('iteracion', 1)
    video_list = []
    list_index = str(id) + '.retransmission.index'
    index = my_server.zrevrangebyscore(list_index, max=max_date, min=min_date)

    if len(index) >= 3:
        number_results = 3
    else:
        number_results = len(index)
    for i in range(0, number_results):
        var = index[i]
        video = []
        video.append(var)
        info = my_server.hvals(str(id) + '.retransmission.info.' + str(var))
        for j in info:
            video.append(j)

        video_list.append(video)
    print video_list
    return index


def get_more_retransmissions(index, id=-1):
    video_list = []
    iter = get_variable('iteracion')
    if (len(index) - 3 * int(iter)) >= 3:
        number_results = 3
    else:
        number_results = (len(index) - 3 * int(iter))

        for i in range(0, number_results):
            var = index[i + 3 * int(iter)]
            video = []
            video.append(var)
            if id is not -1:
                info = my_server.hvals(str(id) + '.retransmission.info.' + str(var))
            else:
                info = my_server.hvals(str(var))
            for j in info:
                video.append(j)

            video_list.append(video)
        set_variable('iteracion', int(iter) + 1)
        print video_list


def get_retransmissions_by_hashtag(hashtag, max_date=99999999, min_date=0):
    set_variable('iteracion', 1)
    video_list = []
    list_hashtags = 'hashtag.' + str(hashtag)
    index = my_server.zrevrangebyscore(list_hashtags, max=max_date, min=min_date)

    if len(index) >= 3:
        number_results = 3
    else:
        number_results = len(index)
    for i in range(0, number_results):
        var = index[i]
        video = []
        video.append(var)
        info = my_server.hvals(str(var))
        for j in info:
            video.append(j)

        video_list.append(video)
    print video_list
    return index


def like_retransmission(id, retransmission_name, retransmission_id):
    aux = my_server.sadd(str(id) + '.liked_retransmissions', str(retransmission_id) + '.retransmission.info.' +
                         str(retransmission_name))
    if aux is 0:
        print 'Already liked'
        return
    else:
        like_list = my_server.hget(str(retransmission_id) + '.retransmission.info.' + str(retransmission_name),
                                   'id_likes')
        like_list = ast.literal_eval(like_list)
        like_list.append(id)
        my_server.hmset(str(retransmission_id) + '.retransmission.info.' + str(retransmission_name),
                        {'id_likes': like_list})
        my_server.hincrby(str(retransmission_id) + '.retransmission.info.' + str(retransmission_name),
                          'number_of_likes')


def comment_retransmission(id, retransmission_name, retransmission_id, comment):
    my_server.sadd(str(id) + '.commented_retransmissions', str(retransmission_id) + '.retransmission.info.' + str(retransmission_name))
    comment_list = my_server.hget(str(retransmission_id) + '.retransmission.info.' + str(retransmission_name), 'comments')
    comment_list = ast.literal_eval(comment_list)
    comment_list.append(str(id) + ': ' + comment)
    my_server.hmset(str(retransmission_id) + '.retransmission.info.' + str(retransmission_name), {'comments': comment_list})
    my_server.publish(str(retransmission_id) + '.' + str(retransmission_name), str(id) + ' has commented on ' + retransmission_name)


def end_retransmission(id, name):
    aux = my_server.hincrby(str(id) + '.retransmission.info.' + str(name), 'status', 0)
    if aux > 0:
        my_server.hincrby(str(id) + '.retransmission.info.' + str(name), 'status', -1)


if __name__ == "__main__":
    my_server.flushdb()
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

    add_retransmission(2, 'prueba', 20170404, ['cuki', 'stick', 'perro'])
    add_retransmission(3, 'prueba1', 20170403, ['flor', 'abeja', 'stick'])
    add_retransmission(1, 'prueba2', 20170405, ['marica', 'peleon', 'cachondo'])
    add_retransmission(0, 'prueba3', 20170402, ['cactus', 'pincha', 'sangre'])
    add_retransmission(1, 'prueba4', 20170401, ['street', 'b&w', 'photography'])
    add_retransmission(2, 'prueba5', 20170406, ['selfie', 'stick', 'sucks'])
    add_retransmission(3, 'prueba6', 20170407, ['hand', 'mug', 'purse'])
    add_retransmission(3, 'prueba7', 20170407, ['stick', 'bread', 'ham'])
    """
    index = get_retransmissions_by_id(0, 20170404, 20170401)
    get_more_retransmissions(index, 0)
    get_more_retransmissions(index, 0)
    index = get_retransmissions_by_hashtag('stick', 20170404, 20170403)
    get_more_retransmissions(index)
"""
    get_retransmissions_by_id(0)
    like_retransmission(1, 'prueba3', 0)
    like_retransmission(1, 'prueba3', 0)
    get_retransmissions_by_id(0)
    comment_retransmission(1, 'prueba3', 0, 'Me mola mazo tu rollo!')
    get_retransmissions_by_id(0)
    comment_retransmission(2, 'prueba3', 0, 'Menuda basura de stream!')
    get_retransmissions_by_id(0)
    end_retransmission(0, 'prueba3')
    get_retransmissions_by_id(0)
