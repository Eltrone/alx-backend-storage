#!/usr/bin/env python3
"""
Module Redis pour la gestion de cache avec décorateurs pour compter les appels
et enregistrer les transactions.
"""

import uuid
import redis
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Décorateur qui compte les appels d'une méthode et stocke ce nombre.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Incrémente le compteur d'appels à chaque appel. """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Décorateur qui enregistre les entrées et sorties des appels de méthode.
    """
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Enregistre les arguments et résultats de la méthode. """
        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))
        return result
    return wrapper


def replay(method: Callable) -> None:
    """
    Affiche l'historique des appels d'une méthode, avec entrées et sorties.
    """
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"
    inputs = method.__self__._redis.lrange(input_key, 0, -1)
    outputs = method.__self__._redis.lrange(output_key, 0, -1)

    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for inp, out in zip(inputs, outputs):
        print(f"{method.__qualname__}(*{inp.decode('utf-8')}) -> " +
              f"{out.decode('utf-8')}")

class Cache:
    """
    Classe Cache pour gérer le stockage Redis.
    """
    def __init__(self):
        """ Initialise Redis et nettoie la base de données. """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stocke les données avec une clé aléatoire.
        
        Args:
            data: Donnée à stocker (str, bytes, int, float).
        
        Returns:
            str: Clé de stockage.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> \
            Union[str, bytes, int, float]:
        """
        Récupère et convertit une valeur de Redis si nécessaire.
        
        Args:
            key: Clé Redis.
            fn: Fonction de conversion (optionnelle).
        
        Returns:
            Valeur convertie ou brute.
        """
        value = self._redis.get(key)
        return fn(value) if fn else value

    def get_str(self, key: str) -> str:
        """ Convertit et retourne une chaîne stockée dans Redis. """
        return self.get(key, lambda x: x.decode())

    def get_int(self, key: str) -> int:
        """ Convertit et retourne un entier stocké dans Redis. """
        return self.get(key, int)
