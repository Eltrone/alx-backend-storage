#!/usr/bin/env python3
"""
Ce module implémente une classe de cache simple utilisant Redis.
"""

import redis
import uuid
from typing import Union


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
        Stocke la donnée dans Redis en utilisant une clé unique et renvoie
        cette clé.
        Arguments:
            data: La donnée à stocker, peut être de type str, bytes, int ou
            float.
        Returns:
            Une chaîne de caractères représentant la clé sous laquelle les
            données sont stockées.
        """
        key = str(uuid.uuid4())
        self._redis.set(name=key, value=data)
        return key


# L'utilisation dans un script principal pourrait ressembler à ceci:
if __name__ == "__main__":
    cache = Cache()
    data = b"hello"
    key = cache.store(data)
    print(key)

    local_redis = redis.Redis()
    print(local_redis.get(key))
