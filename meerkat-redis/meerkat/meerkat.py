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

    set_variable(str(ID) + '.username', username)
    set_variable(str(ID) + '.password', password)
    set_variable(str(ID) + '.cookie', random.randint(0, 99999))
    my_server.expire(str(ID) + '.cookie', 604800)
    my_server.incr('ID')


def add_follower(ID, list_of_follower_IDs):
    my_server.sadd(str(ID) + '.followers', list_of_follower_IDs)


def add_to_following(ID, list_of_IDs_to_follow):
    my_server.sadd(str(ID) + '.following', list_of_IDs_to_follow)


def notify_streaming(ID):
    time.sleep(2)
    my_server.publish(str(ID), 'I started streaming, join me!')


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


def generate_threads_following(ID):
    list_of_following = my_server.smembers(str(ID) + '.following')
    for followingID in list_of_following:
        thread = Thread(target=get_messages_for_id, args=(followingID,))
        thread.start()


def kill_threads_following(ID):
    print 'Killing threads'
    list_of_following = my_server.smembers(str(ID) + '.following')
    for followingID in list_of_following:
        my_server.publish(str(followingID), 'KILL')


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


def get_retransmissions_by_hashtag(hashtag, max_date=99999999, min_date=0, status=0):
    set_variable('iteracion', 1)
    video_list = []
    list_hashtags = 'hashtag.' + str(hashtag)
    index = my_server.zrevrangebyscore(list_hashtags, max=max_date, min=min_date)

    if len(index) >= 3:
        number_results = 3
    else:
        number_results = len(index)

    for i in range(0, number_results):
        retransmission_link = index[i]
        video = []
        # If we want to see every retransmission, active or ended
        if status is 0:
            video.append(retransmission_link)
            retransmission_info = my_server.hvals(str(retransmission_link))
            for info in retransmission_info:
                video.append(info)
            video_list.append(video)
        else:
            # If we only want to see active retransmissions
            if int(my_server.hget(index[i], 'status')) is 1:
                video.append(retransmission_link)
                retransmission_info = my_server.hvals(str(retransmission_link))
                for info in retransmission_info:
                    video.append(info)
                video_list.append(video)

    for i in video_list:
        print i
    return index


def get_retransmissions_by_id(id, max_date=99999999, min_date=0, status=0):
    set_variable('iteracion', 1)
    video_list = []
    list_index = str(id) + '.retransmission.index'
    index = my_server.zrevrangebyscore(list_index, max=max_date, min=min_date)

    if len(index) >= 3:
        number_results = 3
    else:
        number_results = len(index)
    for i in range(0, number_results):
        retransmission_link = index[i]
        video = []
        # If we want to see every retransmission, active or ended
        if status is 0:
            video.append(retransmission_link)
            retransmission_info = my_server.hvals(str(id) + '.retransmission.info.' + str(retransmission_link))
            for info in retransmission_info:
                video.append(info)
            video_list.append(video)
        # If we only want to see active retransmissions
        else:
            if int(my_server.hget(str(id) + '.retransmission.info.' + str(retransmission_link), 'status')) is 1:
                video.append(retransmission_link)
                retransmission_info = my_server.hvals(str(id) + '.retransmission.info.' + str(retransmission_link))
                for info in retransmission_info:
                    video.append(info)
                video_list.append(video)

    for i in video_list:
        print i
    return index


def get_more_retransmissions(index, id=-1, status=0):
    video_list = []
    iter = get_variable('iteracion')
    if (len(index) - 3 * int(iter)) >= 3:
        number_results = 3
    else:
        number_results = (len(index) - 3 * int(iter))

        for i in range(0, number_results):
            # Depending on the iterator, we select different retransmission links
            retransmission_link = index[i + 3 * int(iter)]
            video = []
            # If we want to see every retransmission, active or ended
            if status is 0:
                video.append(retransmission_link)
                # checks whether we want more id retransmissions or hashtag retransmissions
                if id is not -1:
                    info = my_server.hvals(str(id) + '.retransmission.info.' + str(retransmission_link))
                else:
                    info = my_server.hvals(str(retransmission_link))
                for j in info:
                    video.append(j)
                video_list.append(video)
            # If we only want to see active retransmissions
            else:
                aux_status = None
                # checks whether we want more id retransmissions or hashtag retransmissions
                if id is not -1:
                    aux_status = str(id) + '.retransmission.info.' + str(retransmission_link)
                else:
                    aux_status = str(retransmission_link)
                # If we only want to see active retransmissions
                if int(my_server.hget(aux_status, 'status')) is 1:
                    video.append(retransmission_link)
                    if id is not -1:
                        info = my_server.hvals(str(id) + '.retransmission.info.' + str(retransmission_link))
                    else:
                        info = my_server.hvals(str(retransmission_link))
                    for j in info:
                        video.append(j)
                    video_list.append(video)

        set_variable('iteracion', int(iter) + 1)
        for i in video_list:
            print i


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
    # If we need to create a channel, this would do it.
    # my_server.publish(str(retransmission_id) + '.' + str(retransmission_name), str(id) + ' has commented on ' + retransmission_name)


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
    generate_threads_following(1)
    generate_threads_following(2)
    generate_threads_following(3)
    notify_streaming(0)
    time.sleep(3)
    kill_threads_following(1)
    kill_threads_following(2)
    kill_threads_following(3)
"""

    add_retransmission(3, 'prueba', 20170404, ['cuki', 'stick', 'perro'])
    add_retransmission(3, 'prueba1', 20170403, ['flor', 'abeja', 'stick'])
    add_retransmission(1, 'prueba2', 20170405, ['marica', 'peleon', 'cachondo'])
    add_retransmission(0, 'prueba3', 20170402, ['cactus', 'pincha', 'sangre'])
    add_retransmission(1, 'prueba4', 20170401, ['street', 'b&w', 'photography'])
    add_retransmission(2, 'prueba5', 20170406, ['selfie', 'stick', 'sucks'])
    add_retransmission(3, 'prueba6', 20170407, ['hand', 'mug', 'purse'])
    add_retransmission(3, 'prueba7', 20170407, ['stick', 'bread', 'ham'])

    end_retransmission(3, 'prueba7')
    end_retransmission(3, 'prueba6')

    index = get_retransmissions_by_id(3,status=1)
    get_more_retransmissions(index, 3,status=1)
    get_more_retransmissions(index, 3,status=1)
    index = get_retransmissions_by_hashtag('stick',status=1)
    get_more_retransmissions(index,status=1)

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
    """