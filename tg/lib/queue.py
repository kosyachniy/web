"""
Queue functionality for the API
"""

import pickle

from libdev.cfg import cfg
from redis import Redis


class Queue:
    """ FIFO queue with Redis """

    def __init__(self, broker, name):
        self.broker = broker
        self.name = name

    def push(self, data):
        """ Push data to queue """
        self.broker.rpush(self.name, pickle.dumps(data))

    def pop(self):
        """ Pop data from queue """
        if not self.length():
            return None
        return pickle.loads(self.broker.blpop(self.name)[1])

    def length(self):
        """ Length of queue """
        return self.broker.llen(self.name)


redis = Redis(
    host=cfg('redis.host'),
    db=0,
    password=cfg('redis.pass'),
)


def queue(name):
    """ Create queue object """
    return Queue(redis, name)

def expire(key, ttl):
    """ Change expiration time """
    try:
        redis.expire(key, ttl)
    except Exception as e:  # pylint: disable=broad-except
        print("Redis expire error", e)

def save(key, data, ttl=None):
    """ Save value """

    data = pickle.dumps(data)

    try:
        redis.set(key, data)
    except Exception as e:  # pylint: disable=broad-except
        print("Redis save error", e)
        return

    if ttl is not None:
        expire(key, ttl)

def get(key, default=None):
    """ Get value """

    try:
        data = redis.get(key)
    except Exception as e:  # pylint: disable=broad-except
        print("Redis get error", e)
        return default

    if data is None:
        return default

    return pickle.loads(data)
