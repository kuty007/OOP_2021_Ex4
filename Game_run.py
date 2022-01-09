from Game_Controller import Controller
from asyncio import events
from pygame import gfxdraw
import pygame
from pygame import *
from Algo import *
from numpy import inf
from pygame_widgets.button import Button

WIDTH, HEIGHT = 1080, 720
radius = 15


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


class PokemonGame:
    def __init__(self):
        control = Controller()
        self.graph = control.graph
        self.pokemons = control.pokemons
        self.agents = control.agents
        pygame.init()
        self.screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
        self.max_x, self.min_x, self.max_y, self.min_y = self.scale_data()
        back = pygame.image.load('data/pokemons/background.png')
        back_top = self.screen.get_height() - back.get_height()
        back_left = self.screen.get_width() / 2 - back.get_width() / 2
        self.screen.blit(back, (back_top, back_left))
        button_stop = Button(self.screen, 0, 0, 200, 40, text='Stop Game', inactiveColour=(255, 255, 255),
                             hoverColour=(255, 192, 203), font=pygame.font.SysFont('calibri', 30))
        myfont = pygame.font.SysFont('Comic Sans MS', 20)
        text = myfont.render('Score', False, (0, 0, 0))
        clock = pygame.time.Clock()
        self.P1 = pygame.image.load('data/pokemons/1.png').convert()
        self.P2 = pygame.image.load('data/pokemons/3.png').convert()
        pocImg = pygame.image.load('data/pokemons/1.png').convert()
        self.agImg = pygame.image.load('data/pokemons/agent.png')
        tit = pygame.image.load('data/pokemons/titel.png')
        FONT = pygame.font.SysFont('Arial', 20, bold=True)
        control.set_start()
        self.agents = control.agents
        self.pokemons = control.pokemons
        # start = time.time()
        # draw as long as there is a connection to the server
        while control.is_run():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_stop.clicked(event.pos):
                        pygame.quit()
                        exit(0)
            self.screen.blit(back, (back_left, back_top))
            self.screen.blit(pygame.transform.scale(tit, (230, 80)), (800, 580))
            info_data = json.loads(control.client.get_info())
            self.screen.blit(myfont.render('Score: ' + str(info_data["GameServer"]["grade"]), False, (0, 0, 0)), (0, 40))
            self.screen.blit(
                myfont.render('Time to end: ' + str(int(control.client.time_to_end()) // 1000) + ' sec', False, (0, 0, 0)),
                (0, 60))
            self.screen.blit(myfont.render('Moves: ' + str(info_data["GameServer"]["moves"]), False, (0, 0, 0)), (0, 80))
            ########## Draw Graph ############
            self.draw_edges()
            self.draw_nodes()
            button_stop.draw()
            button_stop.listen(events)
            self.draw_agents()
            ########## Draw Pokemons ############
            self.draw_pokemons()
            self.agents = control.update_agents(self.agents, control.client)
            self.pokemons = control.update_pokemons(self.pokemons, control.client, self.graph)
            control.allocate_agents(self.graph, self.pokemons, self.agents)
            # update screen changes
            display.update()
            # refresh rate
            # clock.tick()
            # choose next edge
            control.chose_next_edge(self.agents, control.client)
            pygame.time.wait(85)
            control.client.move()

    def scale_data(self):
        gr = self.graph
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

    def agImage(self, x, y):
        self.screen.blit(pygame.transform.scale(self.agImg, (30, 30)), (x, y))

    # decorate scale with the correct values

    def my_scale(self, data, x=False, y=False):
        if x:
            return scale(data, 50, self.screen.get_width() - 50, self.min_x, self.max_x)
        if y:
            return scale(data, 50, self.screen.get_height() - 50, self.min_y, self.max_y)

    def draw_edges(self):
        for edge in self.graph.edges:
            # find the edge nodes
            src_pos = self.graph.nodes.get(edge[0]).get('pos')
            dest_pos = self.graph.nodes.get(edge[1]).get('pos')
            # scaled positions
            src_x = self.my_scale(src_pos.get_x(), x=True)
            src_y = self.my_scale(src_pos.get_y(), y=True)
            dest_x = self.my_scale(dest_pos.get_x(), x=True)
            dest_y = self.my_scale(dest_pos.get_y(), y=True)
            # draw the line
            pygame.draw.line(self.screen, Color(64, 30, 116),
                             (src_x, src_y), (dest_x, dest_y), 7)

    def draw_nodes(self):
        for i in self.graph.nodes:
            x = self.my_scale(self.graph.nodes.get(i).get('pos').get_x(), x=True)
            y = self.my_scale(self.graph.nodes.get(i).get('pos').get_y(), y=True)
            # its just to get a nice antialiased circle
            gfxdraw.filled_circle(self.screen, int(x), int(y),
                                  radius, Color(64, 30, 116))
            gfxdraw.aacircle(self.screen, int(x), int(y),
                             radius, Color(0, 0, 0))
            FONT = pygame.font.SysFont('Arial', 20, bold=True)
            id_srf = FONT.render(str(i), True, Color(255, 255, 255))
            rect = id_srf.get_rect(center=(x, y))
            self.screen.blit(id_srf, rect)

    def draw_agents(self):
        for agent in self.agents:
            x = self.my_scale(agent.pos.get_x(), x=True)
            y = self.my_scale(agent.pos.get_y(), y=True)
            self.screen.blit(pygame.transform.scale(self.agImg, (30, 30)), (int(x), int(y)))

    def draw_pokemons(self):
        for pok in self.pokemons:
            x = self.my_scale(pok.pos.get_x(), x=True)
            y = self.my_scale(pok.pos.get_y(), y=True)
            if (pok.type < 0):  # Different pok to any type (-1,1)
                self.screen.blit(pygame.transform.scale(self.P1, (30, 30)), (int(x), int(y)))
            else:
                self.screen.blit(pygame.transform.scale(self.P2, (30, 30)), (int(x), int(y)))


if __name__ == '__main__':
    PokemonGame()
