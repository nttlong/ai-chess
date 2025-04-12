# main.py
import gradio as gr
from present import Chessboard

# Create an instance of the Chessboard class with player info
chessboard = Chessboard(
    player1_name="Alice",
    player2_name="Bob",
    player1_api_key="alice_key_123",
    player2_api_key="bob_key_456"
)

# Create Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("## Chessboard Display")

    # Chessboard controls
    move_input = gr.Textbox(label="Enter Move (e.g., e4)", placeholder="Leave blank to show current board")
    output_html = gr.HTML(label="Chessboard")
    show_button = gr.Button("Show Board")
    reset_button = gr.Button("Reset Board")

    # Player info and API controls
    gr.Markdown("### Player Info")
    player_select = gr.Radio(choices=["Player 1", "Player 2"], label="Select Player", value="Player 1")
    player_info_output = gr.Textbox(label="Player Info")
    fetch_rating_button = gr.Button("Fetch Rating")
    rating_output = gr.Textbox(label="Rating Result")

    # Link buttons to class methods
    show_button.click(fn=chessboard.show_chessboard, inputs=move_input, outputs=output_html)
    reset_button.click(fn=chessboard.reset_board, outputs=output_html)


    # Player info and API interactions
    def get_player_info(player):
        player_num = 1 if player == "Player 1" else 2
        return str(chessboard.get_player_info(player_num))


    def fetch_rating(player):
        player_num = 1 if player == "Player 1" else 2
        # Replace with real API endpoint if available
        return chessboard.fetch_player_rating(player_num, endpoint="https://api.example.com/rating")


    player_select.change(fn=get_player_info, inputs=player_select, outputs=player_info_output)
    fetch_rating_button.click(fn=fetch_rating, inputs=player_select, outputs=rating_output)

# Launch the app
demo.launch()