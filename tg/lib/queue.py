"""
Queue functionality for the API
"""

import pickle

from redis import Redis
from libdev.cfg import cfg


class Queue:
    """ FIFO queue with Redis """

    def __init__(self, broker, name):
        self.broker = broker
        self.name = name

    def push(self, data):
        self.broker.rpush(self.name, pickle.dumps(data))

    def pop(self):
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
queue = lambda name: Queue(redis, name)

def save(key, data):
    """ Save value """

    data = pickle.dumps(data)

    try:
        redis.set(key, data)
    # pylint: disable=broad-except
    except Exception as e:
        print("Redis save error", e)

def get(key, default=None):
    """ Get value """

    try:
        data = redis.get(key)
    # pylint: disable=broad-except
    except Exception as e:
        print("Redis get error", e)
        return default

    if data is None:
        return default

    return pickle.loads(data)
