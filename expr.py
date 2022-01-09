from asyncio import events
from pygame import gfxdraw
import pygame
from pygame import *
from Algo import *
from pygame_widgets.button import Button

# init pygame
WIDTH, HEIGHT = 1080, 720
# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()
screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
back = pygame.image.load('data/pokemons/background.png')
back_top = screen.get_height() - back.get_height()
back_left = screen.get_width() / 2 - back.get_width() / 2
screen.blit(back, (back_top, back_left))

button_stop = Button(screen, 0, 0, 200, 40, text='Stop Game', inactiveColour=(255, 255, 255),
                     hoverColour=(255, 192, 203), font=pygame.font.SysFont('calibri', 30))

myfont = pygame.font.SysFont('Comic Sans MS', 20)
text = myfont.render('Score', False, (0, 0, 0))
clock = pygame.time.Clock()
pygame.font.init()
client = Client()
client.start_connection(HOST, PORT)
graph_json = client.get_graph()
graph = load_graph_json(graph_json)
pokemons = client.get_pokemons()
pokemon_list = load_pokemon_list(pokemons, graph)
P1 = pygame.image.load('data/pokemons/1.png').convert()
P2 = pygame.image.load('data/pokemons/3.png').convert()
pocImg = pygame.image.load('data/pokemons/1.png').convert()
agImg = pygame.image.load('data/pokemons/agent.png')
tit = pygame.image.load('data/pokemons/titel.png')
FONT = pygame.font.SysFont('Arial', 20, bold=True)


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


def agImage(x, y):
    screen.blit(pygame.transform.scale(agImg, (30, 30)), (x, y))


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
        pygame.draw.line(screen, Color(64, 30, 116),
                         (src_x, src_y), (dest_x, dest_y), 7)


def draw_nodes(graph):
    for i in graph.nodes:
        x = my_scale(graph.nodes.get(i).get('pos').get_x(), x=True)
        y = my_scale(graph.nodes.get(i).get('pos').get_y(), y=True)

        # its just to get a nice antialiased circle
        gfxdraw.filled_circle(screen, int(x), int(y),
                              radius, Color(64, 30, 116))
        gfxdraw.aacircle(screen, int(x), int(y),
                         radius, Color(0, 0, 0))
        id_srf = FONT.render(str(i), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)


def draw_agents(ag_list):
    for agent in ag_list:
        x = my_scale(agent.pos.get_x(), x=True)
        y = my_scale(agent.pos.get_y(), y=True)
        screen.blit(pygame.transform.scale(agImg, (30, 30)), (int(x), int(y)))


def draw_pokemons(pokemons_list):
    for pok in pokemons_list:
        x = my_scale(pok.pos.get_x(), x=True)
        y = my_scale(pok.pos.get_y(), y=True)
        if (pok.type < 0):  # Different pok to any type (-1,1)
            screen.blit(pygame.transform.scale(P1, (30, 30)), (int(x), int(y)))
        else:
            screen.blit(pygame.transform.scale(P2, (30, 30)), (int(x), int(y)))


radius = 15
# place the agents on the src nodes of Pokémons
start_agents_pos(client, pokemon_list)
# this commnad starts the server - the game is running now
client.start()
x = client.get_agents()
ag_list = load_agents_list(x)
allocate_agents(graph, pokemon_list, ag_list)
"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""

while client.is_running() == 'true':
    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_stop.clicked(event.pos):
                pygame.quit()
                exit(0)
    # refresh surface
    screen.blit(back, (back_left, back_top))
    screen.blit(pygame.transform.scale(tit, (230, 80)), (800, 580))
    info_data = json.loads(client.get_info())
    screen.blit(myfont.render('Score: ' + str(info_data["GameServer"]["grade"]), False, (0, 0, 0)), (0, 40))
    screen.blit(myfont.render('Time to end: ' + str(int(client.time_to_end()) // 1000) + ' sec', False, (0, 0, 0)),
                (0, 60))
    screen.blit(myfont.render('Moves: ' + str(info_data["GameServer"]["moves"]), False, (0, 0, 0)), (0, 80))
    ########## Draw Graph ############
    draw_edges(graph)
    draw_nodes(graph)
    button_stop.draw()
    button_stop.listen(events)

    ########## Draw Agents ############
    # for agent in agents:
    #     screen.blit(pygame.transform.scale(agImg, (30, 30)), (int(agent.pos.x), int(agent.pos.y)))
    draw_agents(ag_list)
    ########## Draw Pokemons ############
    draw_pokemons(pokemon_list)
    ag_list = update_agents(ag_list, client)
    pokemon_list = update_pokemons(pokemon_list, client, graph)
    allocate_agents(graph, pokemon_list, ag_list)
    # update screen changes
    display.update()
    # refresh rate
    # clock.tick(60)
    # choose next edge
    chose_next_edge(ag_list, client)
    pygame.time.wait(90)
    client.move()
    # move_agents(pokemon_list, ag_list, client, graph)
