"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""
from types import SimpleNamespace
from client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *
from load_data_from_server import *
import networkx as nx
from Position import Position
from numpy import inf
from Algo import *

# init pygame
WIDTH, HEIGHT = 1080, 720
# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()
client = Client()
client.start_connection(HOST, PORT)
x = client.get_agents()
print(x)
graph_json = client.get_graph()
graph = load_graph_json(graph_json)
pokemons = client.get_pokemons()
pokemon_list = load_pokemon_list(pokemons, graph)

print(pokemon_list[0].node_src)
graph_json = client.get_graph()
graph = load_graph_json(graph_json)

FONT = pygame.font.SysFont('Arial', 20, bold=True)


# load the json string into SimpleNamespace Object
# get data proportions

def scale_data():
    gr = graph
    x_min = inf
    x_max = -inf
    y_min = inf
    y_max = -inf
    for i in gr.nodes:
        loction = gr.nodes.get(i).get('pos')
        if loction.get_x() > x_max:
            x_max = loction.get_x()
        if loction.get_x() < x_min:
            x_min = loction.get_x()
        if loction.get_y() > y_max:
            y_max = loction.get_y()
        if loction.get_y() < y_min:
            y_min = loction.get_y()

    return x_max, x_min, y_max, y_min


max_x, min_x, max_y, min_y = scale_data()


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


# decorate scale with the correct values

def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)


def draw_nodes(graph):
    for i in graph.nodes:
        x = my_scale(graph.nodes.get(i).get('pos').get_x(), x=True)
        y = my_scale(graph.nodes.get(i).get('pos').get_y(), y=True)

        # its just to get a nice antialiased circle
        gfxdraw.filled_circle(screen, int(x), int(y),
                              radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y),
                         radius, Color(255, 255, 255))
        id_srf = FONT.render(str(i), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)


def draw_edges(graph):
    for edge in graph.edges:
        # find the edge nodes
        src_pos = graph.nodes.get(edge[0]).get('pos')
        dest_pos = graph.nodes.get(edge[1]).get('pos')
        # scaled positions
        src_x = my_scale(src_pos.get_x(), x=True)
        src_y = my_scale(src_pos.get_y(), y=True)
        dest_x = my_scale(dest_pos.get_x(), x=True)
        dest_y = my_scale(dest_pos.get_y(), y=True)
        # draw the line
        pygame.draw.line(screen, Color(61, 72, 126),
                         (src_x, src_y), (dest_x, dest_y))


radius = 15
start_pos = str(pokemon_list[0].node_src)
print(start_pos)
client.add_agent("{id:" + start_pos + "}")
# client.add_agent("{\"id\":1}")
# client.add_agent("{\"id\":2}")
# client.add_agent("{\"id\":3}")
# this commnad starts the server - the game is running now
client.start()
x = client.get_agents()
print(x)
ag_list = load_agents_list(x)
allocte_agents(graph, pokemon_list, ag_list)
"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""

while client.is_running() == 'true':
    draw_nodes(graph)
    draw_edges(graph)
    pokemons = json.loads(client.get_pokemons(),
                          object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pokemons = [p.Pokemon for p in pokemons]
    for p in pokemons:
        x, y, _ = p.pos.split(',')
        p.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    agents = json.loads(client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]
    for a in agents:
        x, y, _ = a.pos.split(',')
        a.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    # refresh surface
    screen.fill(Color(0, 0, 0))
    # draw nodes
    draw_nodes(graph)
    draw_edges(graph)

    # draw agents
    for agent in agents:
        pygame.draw.circle(screen, Color(122, 61, 23),
                           (int(agent.pos.x), int(agent.pos.y)), 10)
    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in pokemons:
        pygame.draw.circle(screen, Color(0, 255, 255), (int(p.pos.x), int(p.pos.y)), 10)

    # update screen changes
    display.update()

    # refresh rate
    # clock.tick(60)

    # choose next edge
    for agent in ag_list:
        if agent.dest == -1:
            agent.path_to_Pokemon.pop(0)
            next_node = agent.path_to_Pokemon[0]
            client.choose_next_edge(
                '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())
    client.move()
