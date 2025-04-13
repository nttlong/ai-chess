# main.py
import gradio as gr
from present import Chessboard

# Create an instance of the Chessboard class
chessboard = Chessboard(
    player1_name="Grok 2.0",
    player2_name="Gemini",
    # player1_api_key="alice_key_123",
    # player2_api_key="bob_key_456"
)

# Create Gradio interface
with gr.Blocks() as demo:
    with gr.Row():
        # Left Column: Player 1 Info and Buttons
        with gr.Column(scale=1):
            gr.Markdown("### Player 1 Info")
            player1_info = gr.Textbox(
                value=str(chessboard.get_player_info(1)),
                label="Player 1 Details",
                interactive=False
            )
            with gr.Row():
                fetch_p1_rating = gr.Button("Fetch Rating")
                clear_p1_rating = gr.Button("Clear Rating")

        # Middle Column: Chessboard and Controls
        with gr.Column(scale=2):
            output_html = gr.HTML(value=chessboard.show_chessboard(), label="Chessboard")
            move_input = gr.Textbox(
                label="Enter Move (e.g., e4)",
                placeholder="Leave blank to show current board"
            )
            with gr.Row():
                show_button = gr.Button("Show Board")
                reset_button = gr.Button("Reset Board")
            status_output = gr.Textbox(label="Status", interactive=False)

        # Right Column: Player 2 Info and Buttons
        with gr.Column(scale=1):
            gr.Markdown("### Player 2 Info")
            player2_info = gr.Textbox(
                value=str(chessboard.get_player_info(2)),
                label="Player 2 Details",
                interactive=False
            )
            with gr.Row():
                fetch_p2_rating = gr.Button("Fetch Rating")
                clear_p2_rating = gr.Button("Clear Rating")

    # Link chessboard buttons to class methods
    def show_board_with_status(move):
        result = chessboard.show_chessboard(move)
        if "Invalid move" in result:
            return result, "Invalid move!"
        return result, f"Last move: {move}" if move else "Board updated"

    show_button.click(
        fn=show_board_with_status,
        inputs=move_input,
        outputs=[output_html, status_output]
    )
    reset_button.click(
        fn=lambda: (chessboard.reset_board(), "Board reset"),
        outputs=[output_html, status_output]
    )

    # Link player info buttons to class methods
    def update_p1_rating():
        result = chessboard.fetch_player_rating(1)
        return str(chessboard.get_player_info(1)) if "rating" in result else result

    def clear_p1_rating():
        return str(chessboard.clear_player_rating(1))

    def update_p2_rating():
        result = chessboard.fetch_player_rating(2)
        return str(chessboard.get_player_info(2)) if "rating" in result else result

    def clear_p2_rating():
        return str(chessboard.clear_player_rating(2))

    # fetch_p1_rating.click(fn=update_p1_rating, outputs=player1_info)
    # clear_p1_rating.click(fn=clear_p1_rating, outputs=player1_info)
    # fetch_p2_rating.click(fn=update_p2_rating, outputs=player2_info)
    # clear_p2_rating.click(fn=clear_p2_rating, outputs=player2_info)

# Launch the app
demo.launch()