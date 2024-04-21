# Tic-Tac-Toe game with gRPC
## Description:
### Client Implementation:
Client accepts an address of the server as an argument and prompts a user to play Tic-Tac-Toe
To play the game you have two options:
- create a new game, or
- connect to an existing game.

When creating a new game, client:
- prompts the user to ask for a mark he wants to play (cross or nought);
- sends a request to the server to create a new game;
- prints the ID of a created game and mark the user plays;
- then prompts the user to make moves until the game is finished.

When connecting to an existing game, client:
- prompts the user to enter an ID of the game to join;
- prompts the user to ask for a mark he wants to play (cross or nought);
- connects to a game (i.e. just fetches the actual game state from the server);
- prints the ID of a created game and mark the user plays;
- then prompts the user to make moves until the game is finished.
When waiting for the opponent's move, client just repeatedly calls the GetGame method once a second until its the user's turn or until the game is over.





Additionally, users should be able to unsubscribe from the channel, and they should not receive
any new notifications from this channel after unsubscribing.
I implemented the described app using the Observer design pattern. Mandatory classes to
implement are:
- class Channel (should enable to subscribe
- class User
- interface Content
- class Video implements Content
- class Shorts implements Content
- class LiveStream implements Content
