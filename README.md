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

### Server Implementation:
Server should accept a port as an argument and run an implemented TicTacToe gRPC servicer that listens on all interfaces on the specified port (i.e. 0.0.0.0:port).

Server should store all created games in order to be able to retrieve them by their IDs and update them with new moves.
It's OK to store games in memory (e.g. in any Python structure), but you need to make sure that the server can handle multiple games at once and avoid race conditions when using threading.

Server should implement the TicTacToe gRPC service defined by you in the tic_tac_toe.proto.
It should have 3 RPCs:

- CreateGame — accepts an empty message and returns a message with a new Game.
- GetGame — accepts a message with a single game_id field and returns a Game with the specified ID.
- MakeMove - accepts a message with two fields: game_id and move, validates the move, updates the state of a Game (according to the rules of Tic-Tac-Toe game) and returns the updated Game.

All three RPCs return Game message that represents the state of the Tic-Tac-Toe game.
It has the following fields:
- id — unique identifier of the game.
- is_finished — whether the game is finished or not.
- winner — mark of the winner, if the game is finished. Not present if the game is not finished or it's a draw.
- turn — mark of the player who should make a move. Not present if the game is finished.
- moves — sequence of moves made in the game.

Move message represents a single move in the game:
- mark — mark of the player who made the move.
- cell — cell number where the player placed the mark (1-9).

When processing requests, server should handle the following errors:

CreateGame should not have any errors.
GetGame should return an error with status code NOT_FOUND if the game with the specified ID does not exist.
MakeMove should validate the request and return error with the following status codes:
- NOT_FOUND — if the game with the specified ID does not exist.
- INVALID_ARGUMENT — if the move's cell is invalid.
- FAILED_PRECONDITION — if the game is already finished.
- FAILED_PRECONDITION — if it's not the player's turn.
- FAILED_PRECONDITION — if the move's cell is already occupied.
