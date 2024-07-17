#!/usr/bin/env python3
""" Module pour interagir avec Redis pour la gestion de cache en utilisant les décorateurs pour compter les appels et enregistrer l'historique des transactions. """

import uuid
import redis
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Décorateur pour compter et stocker le nombre de fois qu'une méthode est appelée.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Fonction enveloppe qui incrémente le compteur à chaque appel de la méthode. """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Décorateur qui enregistre l'historique des arguments et des résultats des appels de la fonction décorée.
    """
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Fonction enveloppe qui enregistre les entrées et les sorties de la fonction appelée. """
        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))
        return result
    return wrapper


def replay(method: Callable) -> None:
    """
    Fonction pour afficher l'historique des appels d'une méthode spécifique, montrant les entrées et les sorties.
    """
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"
    inputs = method.__self__._redis.lrange(input_key, 0, -1)
    outputs = method.__self__._redis.lrange(output_key, 0, -1)

    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for inp, out in zip(inputs, outputs):
        print(f"{method.__qualname__}(*{inp.decode('utf-8')}) -> {out.decode('utf-8')}")

class Cache:
    """ Classe Cache pour gérer un stockage Redis. """
    def __init__(self):
        """ Initialise le client Redis et nettoie la base de données existante. """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stocke les données dans Redis en utilisant une clé aléatoire.
        
        Args:
            data: Donnée à stocker (str, bytes, int, float).
        
        Returns:
            La clé sous laquelle les données sont stockées.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Récupère une valeur de Redis et la convertit si nécessaire.
        
        Args:
            key: La clé Redis.
            fn: Fonction optionnelle de conversion.
        
        Returns:
            Valeur convertie si fn est fournie, sinon valeur brute.
        """
        value = self._redis.get(key)
        return fn(value) if fn else value

    def get_str(self, key: str) -> str:
        """ Récupère et convertit une chaîne stockée dans Redis. """
        return self.get(key, lambda x: x.decode())

    def get_int(self, key: str) -> int:
        """ Récupère et convertit un entier stocké dans Redis. """
        return self.get(key, int)
