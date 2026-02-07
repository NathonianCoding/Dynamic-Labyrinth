A 2D maze game I made for my A-level NEA. It uses Pygame and SQLite3. In this game, the player navigates an algorithmically generated maze, collecting coins and evading zombies. When they reach the exit, a harder level is generated. 
This process continues until the player loses.

This game uses a relational database with two relations 'accounts' and 'savedGames'. The 'accounts' relation stores details about accounts, 
includinglogin details and performance statistics. The 'savedGames' relation stores information about levels (e.g. level and maze size), so that a saved 
game can be resumed.
