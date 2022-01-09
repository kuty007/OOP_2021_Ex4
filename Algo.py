from numpy import inf
from client import Client
from load_data_from_server import *

eps = 0.01


def allocate_agents(graph: nx.DiGraph, pok_list, agent_list):
    """Function receives the agents list,graph and Pokemons list and allocate for each Pokemon an agent
    first check if the agent is close to the pokemon if so return.

    second check if there is free agent and if so assign him to this pokemon and add the path to collect
    this pokemon to the agent path_to_Pokemon.

    third find the agent who will collect the pokemon the fastest.
    assign him to this pokemon and add the path to collect this pokemon to the agent path_to_Pokemon.
    """
    for pok in pok_list:
        if pok.alocte_agent == -1:
            min_time = inf
            path_add = []
            best_agent = -1
            x = free_agents(graph, agent_list, pok)
            for agent in agent_list:
                if agent.dest == pok.node_dest and agent.pos.distance(pok.pos) < eps:
                    return
                if pok.alocte_agent == -1 and x != -1:
                    pok.alocte_agent = x[0].id
                    agent_ = agent_list[agent_list.index(x[0])]
                    agent_.path_to_Pokemon = x[1]
                    agent_.path_to_Pokemon.append(pok.node_dest)
                    return
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


def free_agents(graph: nx.DiGraph, agent_list, pok: Pokemon):
    """Function receives the agents list,graph and Pokemon and find from the unbusy agents who will
    collect the Pokemon in the fastest time"""
    min_time = inf
    path = -1
    best_agent = -1
    for agent in agent_list:
        if not agent.path_to_Pokemon:
            temp_path = agent.time_to_pokemon_src(graph, pok)
            if temp_path[2] < min_time:
                min_time = temp_path[2]
                path = temp_path
                best_agent = agent
    if path != -1:
        return best_agent, path[0]
    return -1


def update_agents(start_agent_list, client: Client):
    """Function receives the agents list and client load the agents new values from the client and
     update the agents in the agents list accordingly  """
    new_agent_list = load_agents_list(client.get_agents())
    for i in range(len(new_agent_list)):
        exsist_path = start_agent_list[i].path_to_Pokemon
        start_agent_list[i] = new_agent_list[i]
        start_agent_list[i].path_to_Pokemon = exsist_path
    return start_agent_list


def update_pokemons(start_pokemons_list, client: Client, graph: nx.DiGraph):
    """Function receives the pokemons_list and client load the new pokemons from the client and
         update the pokemons_list accordingly  """
    new_pokemons_list = load_pokemon_list(client.get_pokemons(), graph)
    for pok in new_pokemons_list:
        for oldpok in start_pokemons_list:
            if pok.node_dest == oldpok.node_dest and pok.node_src == oldpok.node_src and pok.pos.get_x() == oldpok.pos.get_x() and pok.pos.get_y() == oldpok.pos.get_y():
                pok.alocte_agent = oldpok.alocte_agent
    start_pokemons_list = new_pokemons_list
    start_pokemons_list.sort(key=lambda x: x.value, reverse=True)
    return start_pokemons_list


# not working at this moment
def move_agents(pokemons_list, agent_list, client: Client, graph: nx.DiGraph):
    for agent in agent_list:
        if agent.dest != -1:
            if agent.pos.distance(graph.nodes[agent.src]['pos']) < 0.0001:
                client.move()
        else:
            for pok in pokemons_list:
                if agent.pos.distance(pok.pos) < eps:
                    client.move()


def chose_next_edge(agent_list, client: Client):
    """Function receives the agents list and client send massage to server using
    client.choose_next_edge with each agent next edge """
    for agent in agent_list:
        if agent.dest == -1 and len(agent.path_to_Pokemon) > 0:
            agent.path_to_Pokemon.pop(0)
            if len(agent.path_to_Pokemon) > 0:
                next_node = agent.path_to_Pokemon[0]
                agent.dest = next_node
                client.choose_next_edge(
                    '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')


def start_agents_pos(client: Client, pokemons_list):
    """Function receives pokemons_list and client find out how many agents are in this
    stage and then locate them on the Pokémons src node
     """
    x = json.loads(client.get_info())
    num_of_agents = int(x["GameServer"]["agents"])
    i = 0
    while i < num_of_agents and i < len(pokemons_list):
        start_pos = str(pokemons_list[i].node_src)
        client.add_agent("{id:" + start_pos + "}")
        i += 1
