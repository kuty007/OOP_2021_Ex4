# Ex4-OOP - Final Project - Pokemon Game

Made by Asaf Yekutiel,Yulia Katz

GitHub pages:

https://github.com/yukatz

https://github.com/kuty007

![Ex4](https://user-images.githubusercontent.com/92925727/148643445-b552ead0-e767-45b7-887a-37255081cf26.png)

# Introduction

This project is an final assignment in an object-oriented course at Ariel University. In this project we implemented a
simple Pokemon game. The game is running by a simple server, and a client that receiving information from the server
such as: graph structure, location of the Pokemon, the amount and speed of the agents and more. On our side we have
implemented algorithms to optimize the agents work by efective allocation to pokemons. Also we build a pygame design to
the client side.

# Creating and Implementing Directed Weighted Graph Theory.

In this assignment we based our graph on Phyton package NetworkX see more info her: https://networkx.org/

# Algorithm
The algorithm work in the following way:
iterate on all pokemons in the pokemons list
and check who is the best agent to collect him using the allocate_agents function
its work in the following way:

First check if the agent is close to the pokemon if so return.

Second check if there is free agent using free_agents method the and if so assign him to this pokemon and add the path to collect
this pokemon to the agent path_to_Pokemon.

Third find the agent who will collect the pokemon the fastest.
assign him to this pokemon and add the path to collect this pokemon to the agent path_to_Pokemon.



# UML
![UML](https://user-images.githubusercontent.com/73474039/148698948-edc938d1-5fc5-44ed-902a-b256fea43f2b.jpg)

# Results
| **Case**   | **Graph**   | **Pokemons** | **Time**   | **Agents**  | **Grade** | **Moves** |
|------------|-------------|--------------|------------|-------------|-----------|-----------|
| 0          | A0          |  1           |  30 sec    |  1          | 140       | 300       |
| 1          | A0          |  2           |  1 min     |  1          | 349       | 599       |
| 2          | A0          |  3           |  30 sec    |  1          | 256       | 300       |
| 3          | A0          |  4           |  1 min     |  1          | 624       | 598       |
| 4          | A1          |  5           |  30 sec    |  1          | 284       | 178       |
| 5          | A1          |  6           |  1 min     |  1          | 550       | 571       |
| 6          | A1          |  1           |  30 sec    |  1          | 79        | 289       |
| 7          | A1          |  2           |  1 min     |  1          | 249       | 574       |
| 8          | A2          |  3           |  30 sec    |  1          | 40        | 260       |
| 9          | A2          |  4           |  1 min     |  1          | 236       | 529       |
| 10         | A2          |  5           |  30 sec    |  1          | 47        | 260       |
| 11         | A2          |  6           |  1 min     |  3          | 1129      | 585       |
| 12         | A3          |  1           |  30 sec    |  1          | 40        | 252       |
| 13         | A3          |  2           |  1 min     |  2          | 152       | 501       |
| 14         | A3          |  3           |  30 sec    |  3          | 152       | 249       |
| 15         | A3          |  4           |  1 min     |  1          | 229       | 496       |


##   Download and run the Project:

Before running this project, install the following packages:
```
Pygame Version 2.1.0.,numpy,networkx
```

Download the whole project and export it by the above actions:
```
Click Code (Green Button) -> Click Download ZIP -> Choose Extract to Folder in Zip 
```

Run the Server from cmd in the folder which contains 'Ex4_Server_v0.0.jar', choose one of the 16 cases ([0,15]):
```
java -jar Ex4_Server_v0.0.jar [0,15]
```

Then, open the Game_run.py file and run it:
```
OOP_2021_Ex4-> Game_run.py -> RUN
```

## For more information please visit our [WIKI pages](../../wiki)



