#!/usr/bin/env python3
""" Redis basic """

import uuid
import redis
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ count_calls function """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wrapper function """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """ call_history function """
    inkey = method.__qualname__ + ":inputs"
    outkey = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wrapper function """
        self._redis.rpush(inkey, str(args))
        res = method(self, *args, **kwargs)
        self._redis.rpush(outkey, str(res))
        return res

    return wrapper


def replay(method: Callable) -> None:
    """ replay function """
    input_key = "{}:inputs".format(method.__qualname__)
    output_key = "{}:outputs".format(method.__qualname__)

    inputs = method.__self__._redis.lrange(input_key, 0, -1)
    outputs = method.__self__._redis.lrange(output_key, 0, -1)

    print("{} was called {} times:".format(method.__qualname__, len(inputs)))
    for inp, out in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(
            method.__qualname__, inp.decode("utf-8"), out.decode("utf-8")
            )
        )


class Cache:
    def __init__(self):
        """ init function """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ store function """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
            self, key: str, fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, float]:
        """ get function """
        if fn:
            return fn(self._redis.get(key))
        val = self._redis.get(key)
        return val

    def get_str(self, key: str) -> str:
        """ get_str function """
        return int.from_bytes(self, sys.byteorder)

    def get_int(self, key: str) -> int:
        """ get_int function """
        return self.decode("utf-8")
