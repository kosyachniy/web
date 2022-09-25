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
        self.broker.rpush(self.name, pickle.dumps(data))

    def pop(self):
        if not self.length():
            return None
        return pickle.loads(self.broker.blpop(self.name)[1])

    def length(self):
        return self.broker.llen(self.name)


redis = Redis(
    host=cfg('redis.host'),
    db=1,
    password=cfg('redis.pass'),
)
queue = lambda name: Queue(redis, name)

def save(key, data):
    data = pickle.dumps(data)

    try:
        redis.set(key, data)
    except:
        pass

def get(key, default=None):
    try:
        data = redis.get(key)
    except:
        return default

    if data is None:
        return default

    return pickle.loads(data)
