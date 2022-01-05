from Position import Position
from Pokemon import Pokemon
from numpy import inf
import networkx as nx


def allocte_agents(graph: nx.DiGraph, pok_list, agent_list):
    for pok in pok_list:
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

