from Position import Position
from Pokemon import Pokemon
from numpy import inf
import networkx as nx

from client import Client
from load_data_from_server import *

eps = 0.1


def allocte_agents(graph: nx.DiGraph, pok_list, agent_list):
    for pok in pok_list:
        if pok.alocte_agent == -1:
            min_time = inf
            path_add = []
            best_agent = -1
            for agent in agent_list:
                if agent.dest == pok.node_dest and agent.pos.distance(pok.pos) < eps:
                    return
                elif len(agent.path_to_Pokemon) < 1:
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
            agent_ = agent_list[agent_list.index(best_agent)]
            path_len = len(best_agent.path_to_Pokemon)
            if path_len >= 2:
                for i in range(path_len - 1):
                    if best_agent.path_to_Pokemon[i] == pok.node_src and best_agent.path_to_Pokemon[
                        i + 1] == pok.node_dest:
                        return
            agent_.path_to_Pokemon.extend(path_add)
            agent_.path_to_Pokemon.append(pok.node_dest)
            new_path = [agent_.path_to_Pokemon[0]]
            for i in range(1, len(agent_.path_to_Pokemon)):
                if agent_.path_to_Pokemon[i] != agent_.path_to_Pokemon[i - 1]:
                    new_path.append(agent_.path_to_Pokemon[i])
            agent_.path_to_Pokemon = new_path


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
    start_pokemons_list.sort(key=lambda x: x.value, reverse=True)
    return start_pokemons_list


def move_agents(pokemons_list, agent_list, client: Client):
    for agent in agent_list:
        if agent.dest == -1 and len(agent.path_to_Pokemon) > 0:
            agent.path_to_Pokemon.pop(0)
            if len(agent.path_to_Pokemon) > 0:
                next_node = agent.path_to_Pokemon[0]
                client.choose_next_edge(
                    '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
            client.move()
            ttl = client.time_to_end()
            print(ttl, client.get_info())

        else:
            for pok in pokemons_list:
                if agent.pos.distance(pok.pos) < eps:
                    client.move()


def start_agents_pos(client: Client, pokemons_list):
    x = json.loads(client.get_info())
    num_of_agents = int(x["GameServer"]["agents"])
    i = 0
    while i < num_of_agents and i < len(pokemons_list):
        start_pos = str(pokemons_list[i].node_src)
        client.add_agent("{id:" + start_pos + "}")
        i += 1
