# present.py
import chess
import chess.svg
import base64
from player import Player


class Chessboard:
    def __init__(self, player1_name="Player 1", player2_name="Player 2",
                 player1_api_key="key1", player2_api_key="key2"):
        """
        Initialize the chessboard and two players.
        """
        self.board = chess.Board()  # Starting position: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR
        self.player1 = Player(player1_name, player1_api_key)
        self.player2 = Player(player2_name, player2_api_key)
        self.player1.info["color"] = "white"
        self.player2.info["color"] = "black"

    def show_chessboard(self, move=None):
        """
        Generate an SVG chessboard and return it as an HTML string for Gradio.
        If a move is provided, apply it to the board.
        """
        if move:
            try:
                self.board.push_san(move)
            except ValueError:
                return "<p style='color:red;'>Invalid move!</p>"

        svg = chess.svg.board(self.board)
        svg_base64 = base64.b64encode(svg.encode()).decode()
        html = f'<img src="data:image/svg+xml;base64,{svg_base64}" style="width:400px; height:400px;" />'
        return html

    def reset_board(self):
        """
        Reset the board to the starting position.
        Returns an HTML string with the SVG chessboard.
        """
        self.board = chess.Board()
        svg = chess.svg.board(self.board)
        svg_base64 = base64.b64encode(svg.encode()).decode()
        html = f'<img src="data:image/svg+xml;base64,{svg_base64}" style="width:400px; height:400px;" />'
        return html

    def get_player_info(self, player_num):
        """
        Return the info dictionary for the specified player (1 or 2).
        """
        if player_num == 1:
            return self.player1.info
        elif player_num == 2:
            return self.player2.info
        return "Invalid player number!"

    def fetch_player_rating(self, player_num, endpoint="https://api.example.com/rating"):
        """
        Fetch the player's rating via API using their API key.
        Returns the API response or an error message.
        """
        player = self.player1 if player_num == 1 else self.player2 if player_num == 2 else None
        if not player:
            return "Invalid player number!"
        response = player.connect_to_api(endpoint)
        if isinstance(response, dict) and "rating" in response:
            player.info["rating"] = response["rating"]
            return f"{player.info['name']} rating: {player.info['rating']}"
        return response