                                                                           MINI GAME HUB
It is a two player game platform made using bash and python . The basic structure of the project is that two users will log in and undergo authentication , then from the game menu the users can choose any game they want to play from available three games , play through a GUI and view results recorded in a leaderboard system.

Features :

1. Authentication -
   Two -player login system , new user could register , credentials will be stored in "users.tsv" , password storage will be done using SHA-256 hashing
   
2. Game Engine -
   Python and pygame will be used , GUI based gameplay , turn based logic for two players
   
3. Games -
   i) Tic-Tac-Toe (10 * 10) - players must get 5 symbols in a row (horizontal,vertical,diagonal)
   
   ii) Connect Four ( 7 * 7 ) - players drops coins or any symbol or mark into columns , first to           connect four wins.
   
   iii) Othello (8 * 8) - players capture opponent discs by trapping them
   
5. Leaderboard and Analytics -
    Results of game will be stored in "history.csv" , leaderboard will be generated , win loss statistics will be displayed , graphs will be generated using Matplotlib.
   
   
   
