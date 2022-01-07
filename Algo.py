from Position import Position
from Pokemon import Pokemon
from numpy import inf
import networkx as nx

from client import Client
from load_data_from_server import *


def allocte_agents(graph: nx.DiGraph, pok_list, agent_list):
    for pok in pok_list:
        if pok.alocte_agent == -1:
            min_time = inf
            path_add = []
            best_agent = -1
            for agent in agent_list:
                if len(agent.path_to_Pokemon) < 1:
                    temp_path = agent.time_to_pokemon_src(graph, pok)
                    temp_pat = temp_path[0]
                    temp_time = temp_path[2]
                else:
                    temp_time = agent.time_to_pokemon_src(graph, pok)[2] + (
                            nx.shortest_path_length(graph, agent.src, agent.path_to_Pokemon[-1],
                                                    weight='weight') / agent.speed)
                    temp_pat = nx.shortest_path(graph, agent.path_to_Pokemon[-1], pok.node_src)
                if temp_time < min_time:
                    min_time = temp_time
                    best_agent = agent
                    path_add = temp_pat
            pok.alocte_agent = best_agent.id
            agent_list[agent_list.index(best_agent)].path_to_Pokemon.extend(path_add)
            agent_list[agent_list.index(best_agent)].path_to_Pokemon.append(pok.node_dest)


def update_agents(start_agent_list, client: Client):
    new_agent_list = load_agents_list(client.get_agents())
    for i in range(len(new_agent_list)):
        exsist_path = start_agent_list[i].path_to_Pokemon
        start_agent_list[i] = new_agent_list[i]
        start_agent_list[i].path_to_Pokemon = exsist_path
    return start_agent_list

def update_pokemons(start_pokemons_list, client: Client, graph: nx.DiGraph):
    new_pokemons_list = load_pokemon_list(client.get_pokemons(), graph)
    for pok in new_pokemons_list:
        for oldpok in start_pokemons_list:
            if pok.node_dest == oldpok.node_dest and pok.node_src == oldpok.node_src and pok.pos.get_x() == oldpok.pos.get_x() and pok.pos.get_y() == oldpok.pos.get_y():
                pok.alocte_agent = oldpok.alocte_agent
    start_pokemons_list = new_pokemons_list
    return start_pokemons_list
