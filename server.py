import sys
import threading
from typing import Iterable, Optional
import grpc
import tic_tac_toe_pb2_grpc as ttt_grpc
import tic_tac_toe_pb2 as ttt
from concurrent import futures


def get_winner(moves: Iterable[ttt.Move]) -> Optional[ttt.Mark]:
    winning_combinations = (
        (1, 2, 3), (4, 5, 6), (7, 8, 9),  # Rows
        (1, 4, 7), (2, 5, 8), (3, 6, 9),  # Cols
        (1, 5, 9), (3, 5, 7),  # Diagonals
    )

    x_moves = []
    o_moves = []

    for move in moves:
        if move.mark == ttt.MARK_CROSS:
            x_moves.append(move.cell)
        elif move.mark == ttt.MARK_NOUGHT:
            o_moves.append(move.cell)

    for combination in winning_combinations:
        if all((cell in x_moves) for cell in combination):
            return ttt.MARK_CROSS
        if all((cell in o_moves) for cell in combination):
            return ttt.MARK_NOUGHT

    return None


class TicTacToeServicer(ttt_grpc.TicTacToeServicer):
    def __init__(self):
        self.games = {}
        self.lock = threading.Lock()

    def CreateGame(self, request, context):
        game_id = 1 + len(self.games)
        game = ttt.Game()
        game.id = game_id
        with self.lock:
            self.games[game_id] = game
        print("CreateGame()")
        return game

    def GetGame(self, request, context):
        game_id = request.game_id
        print(f"GetGame(game_id={game_id})")
        with self.lock:
            game = self.games.get(game_id)
            if game is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Game not found')
                return ttt.Game()
            else:
                return self.games[game_id]

    def MakeMove(self, request, context):
        game_id = request.game_id
        move = request.move
        if move.mark == 0:
            mark = 'O'
        else:
            mark = 'X'
        print(f"MakeMove(game_id={game_id}, move=Move(mark={mark}, cell={move.cell}))")

        with self.lock:
            game = self.games.get(game_id)
            if not game:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Game not found')
                return ttt.Game()

            if game.is_finished:
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
                context.set_details("Game is already finished")
                return game

            if move.cell < 1 or move.cell > 9:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Move's cell is invalid")
                return game

            for existing_move in game.moves:
                if existing_move.cell == move.cell:
                    context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
                    context.set_details("Move's cell is already occupied")
                    return game

            if game.turn != move.mark:
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
                context.set_details("It is not the player's turn")
                return game

            game.moves.append(move)
            winner = get_winner(game.moves)
            if winner is not None:
                game.is_finished = True
                game.winner = winner
            elif len(game.moves) == 9:
                game.is_finished = True
            if game.turn == ttt.MARK_CROSS:
                game.turn = ttt.MARK_NOUGHT
            else:
                game.turn = ttt.MARK_CROSS
            return game


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ttt_grpc.add_TicTacToeServicer_to_server(TicTacToeServicer(), server)
    server.add_insecure_port(f"0.0.0.0:{sys.argv[1]}")
    server.start()
    print(f"Server listening on 0.0.0.0:{sys.argv[1]}...")
    try:
        while True:
            server.wait_for_termination()
    except KeyboardInterrupt:
        print("Exiting...")
        server.stop(0)
