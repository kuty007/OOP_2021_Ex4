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
![UML](https://user-images.githubusercontent.com/73474039/148698948-edc938d1-5fc5-44ed-902a-b256fea43f2b.jpg)


## For more information please visit our [WIKI pages](../../wiki)



