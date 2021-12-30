# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 22:55:11 2021

@author: Alejandra Pabon
"""

################IMPORT################

from typing import Any, Dict
import httpx

################FUNCTIONS################

def load_data(api: str) -> Dict[str, Any]:
    """
    This function is used to load the data from an api
    :param api: The api from which it will retrieve the data
    :type api: str
    :return: The response of the request in a Dictionary
    :rtype: Dict[str, Any]
    """
    data: Dict = {}
    try:
        res = httpx.get(api, timeout=15.0)
        res.raise_for_status()
        data = res.json()
    except httpx.HTTPStatusError as err:
        print("Error -> "
            f"[ERROR]: status code: {err.response.status_code} - "
            f"message: {err.response.json()}")
    return data


def pokemonName() -> int:
    """
    This function shows the number of pokemones that have an "at" and two "a" 
    in it's name
    :return: The number of pokemones that meet the conditions
    :rtype: int
    """
    data: Dict = load_data('https://pokeapi.co/api/v2/pokemon/?offset=0&limit=100')
    cen: bool = False
    rta: int = 0
    while cen == False:
        for elem in data["results"]:
                if ("at" in elem["name"]) and elem["name"].count('a')==2:
                    rta +=1
        if data['next']== None:
            cen = True
        else:
            data = load_data(data['next'])
    return rta


def raichuSpecies() -> int:
    """
    This function shows the number of species of pokemon that can breed with
    Raichu
    :return: The number of species of pokemon that can breed with Raichu
    :rtype: int
    """
    data: Dict = load_data('https://pokeapi.co/api/v2/pokemon/raichu')
    data = load_data(data["species"]["url"])
    rta: set = set()
    for elem in data["egg_groups"]:
        data_aux: Dict = load_data(elem["url"])
        for specie in data_aux["pokemon_species"]:
            rta.add(specie["name"])
    return len(rta)


def min_max_weight() -> list:
    """
    This function shows a list with the maximun and minimun weight of the first
    generation pokemones of type fighting. The first position is the maximun
    weight and the second position is the minimun weight
    :return: A list with the maximun and minimun weight of the first
    generation pokemones of type fighting
    :rtype: list
    """
    data: Dict = load_data('https://pokeapi.co/api/v2/type/fighting/')
    weights: list = []
    for elem in data["pokemon"]:
        aux: str = elem["pokemon"]["url"]
        if int(aux.split("/")[6]) <= 151:
            weights.append((load_data(aux)["weight"]))
    return [max(weights), min(weights)]
    
print(pokemonName())
print(raichuSpecies())
print(min_max_weight())
