# Ex4-OOP - Final Project - Pokemon Game

Made by Asaf Yekutiel,Yulia Katz

GitHub pages:

https://github.com/yukatz

https://github.com/kuty007

![Ex4](https://user-images.githubusercontent.com/92925727/148643445-b552ead0-e767-45b7-887a-37255081cf26.png)

## Introduction

This project is an final assignment in an object-oriented course at Ariel University. In this project we implemented a
simple Pokemon game. The game is running by a simple server, and a client that receiving information from the server
such as: graph structure, location of the Pokemon, the amount and speed of the agents and more. On our side we have
implemented algorithms to optimize the agents work by efective allocation to pokemons. Also we build a pygame design to
the client side.

## Creating and Implementing Directed Weighted Graph Theory.

In this assignment we based our graph on Phyton package NetworkX see more info her: https://networkx.org/

## Class.

---------

### Agent:

this class is used to crate an Agent object the agent have the following fields:

path_to_Pokemon:list of nodes to go to catch a Pokemon

pos:the Position of the agent at the moment

speed:the agent speed update when catch Pokemon

dest: next node to go to

src: last node the agent was placed on

value:  the collective amount of Pokémons values the agent has benn collect so far

id: agent number

### Pokemon

this class is used to crate an Pokemon object the Pokemon have the following fields:

alocte_agent: the agent id that assign to collect this Pokemon

value: how many points the Pokemon worth

node_src: the src node of the edge the Pokemon lying on

node_dest: the dest node of the edge the Pokemon lying on

pos:the Position of the Pokemon (used to find the edge the Pokemon lying on)

type: for pokemon lying on edge (src,dest) if src < dest => type > 0 else dest < src => type

### Controller

this class is used to crate a Controller object that do all the algorithmic work and the connection to the server
Controller have the following fields:

client: use to communicate with the server

graph: nxDIgraph

Pokémons: list of Pokémons

agents = list of agents

info: info form the server

this class use the following methods:

allocate_agents: use to allocate agents to Pokémons

update_agents: receives the agents list and client load the agents new values from the client and update the agents in
the agents list accordingly

chose_next_edge: receives the agents list and client send message to server using client.choose_next_edge with each
agent next edge

start_agents_pos: receives pokemons_list and client find out how many agents are in this stage and then locate them on
the Pokémons src node

### PokemonGame

This class is used to draw the game this class gets all the information from the Controller and

use it to draw the changes in the game in real time.

We use this class to run the game

---------

# Algorithm
The algorithm work in this way:
itrite on all pokemons in the pokemons list
and check who is the best agent to collect him using the allocate_agents function
its work in the following way:

First check if the agent is close to the pokemon if so return.

Second check if there is free agent using free_agents method the and if so assign him to this pokemon and add the path to collect
this pokemon to the agent path_to_Pokemon.

Third find the agent who will collect the pokemon the fastest.
assign him to this pokemon and add the path to collect this pokemon to the agent path_to_Pokemon.




# UML

## For more information please visit our [WIKI pages](../../wiki)


