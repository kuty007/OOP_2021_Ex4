import math
import networkx as nx
from Position import Position
from Pokemon import Pokemon


class Agent:
    def __init__(self, id: int = 0, value: float = 0, src: int = 0, dest: int = 0, speed: float = 0,
                 pos: Position = Position(), agent_str=None):
        self.path_to_Pokemon = []
        if agent_str is not None:
            self.load_agent(agent_str)
        else:
            self.pos = pos
            self.speed = speed
            self.dest = dest
            self.src = src
            self.value = value
            self.id = id

    def load_agent(self, json_agent_str):
        """Function receives the agent string and load the values to the agent object """
        self.pos = Position(location=json_agent_str['pos'])
        self.speed = json_agent_str['speed']
        self.id = json_agent_str['id']
        self.value = json_agent_str['value']
        self.src = json_agent_str['src']
        self.dest = json_agent_str['dest']
