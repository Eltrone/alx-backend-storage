#!/usr/bin/env python3
"""
Ce module implémente une classe de cache avancée utilisant Redis.
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps

class Cache:
    """
    Cache classe pour stocker et récupérer des valeurs à partir de Redis.
    """

    def __init__(self):
        """
        Initialise le client Redis et efface la base de données Redis existante.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stocke la donnée dans Redis en utilisant une clé unique et renvoie cette clé.
        """
        key = str(uuid.uuid4())
        if isinstance(data, str):
            data = data.encode('utf-8')
        self._redis.set(name=key, value=data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Optional[Union[str, bytes, int, float]]:
        """
        Récupère une valeur de Redis par sa clé et utilise une fonction optionnelle
        pour convertir cette valeur dans le format souhaité.
        """
        value = self._redis.get(key)
        if fn and value is not None:
            return fn(value)
        return value

    def get_str(self, key: str) -> Optional[str]:
        """
        Récupère une chaîne de caractères de Redis.
        """
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Récupère un entier de Redis.
        """
        return self.get(key, fn=int)

def count_calls(method: Callable) -> Callable:
    """
    Décorateur pour compter le nombre de fois qu'une méthode est appelée.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    """
    Décorateur pour enregistrer l'historique des appels d'une méthode.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        inputs_key = f"{method.__qualname__}:inputs"
        outputs_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(inputs_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, str(result))
        return result
    return wrapper

def replay(method: Callable):
    """
    Affiche l'historique des appels d'une méthode.
    """
    instance = method.__self__
    qualname = method.__qualname__
    inputs = instance._redis.lrange(f"{qualname}:inputs", 0, -1)
    outputs = instance._redis.lrange(f"{qualname}:outputs", 0, -1)
    count = instance._redis.get(qualname).decode('utf-8')
    print(f"{qualname} was called {count} times:")
    for inp, out in zip(inputs, outputs):
        print(f"{qualname}{inp.decode('utf-8')} -> {out.decode('utf-8')}")

Cache.store = count_calls(Cache.store)
Cache.store = call_history(Cache.store)
