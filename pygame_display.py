# pygame_display.py
import pygame
import sys
from io import BytesIO
from present import Chessboard

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_SIZE = (400, 400)  # Match the PNG size
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Chessboard with Pygame")

# Create Chessboard instance
chessboard = Chessboard(
    player1_name="Alice",
    player2_name="Bob",
    player1_api_key="alice_key_123",
    player2_api_key="bob_key_456"
)


# Load initial board as PNG
def load_board_image(png_stream):
    """
    Load a PNG stream into a Pygame surface.
    """
    # Convert BytesIO stream to a format Pygame can load
    image = pygame.image.load(png_stream)
    return image


# Get initial board image
png_stream = chessboard.get_board_png_stream()
board_image = load_board_image(png_stream)

# Game loop
running = True
move_input = ""  # For collecting move input (e.g., "e4")
message = ""  # For displaying messages (e.g., invalid move)

# Font for messages
font = pygame.font.Font(None, 36)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:  # Press Q to quit
                running = False

            elif event.key == pygame.K_r:  # Press R to reset
                png_stream = chessboard.reset_board_for_pygame()
                board_image = load_board_image(png_stream)
                message = "Board reset"

            elif event.key == pygame.K_RETURN:  # Press Enter to submit move
                if move_input:
                    try:
                        png_stream = chessboard.get_board_png_stream(move_input)
                        board_image = load_board_image(png_stream)
                        message = f"Move: {move_input}"
                    except ValueError as e:
                        message = str(e)
                    move_input = ""  # Clear input after submitting

            elif event.key == pygame.K_BACKSPACE:  # Backspace to delete last character
                move_input = move_input[:-1]

            else:  # Collect move input (e.g., "e4")
                char = event.unicode
                if char.isalnum():  # Only accept alphanumeric characters
                    move_input += char

    # Draw the board
    screen.fill((255, 255, 255))  # White background
    screen.blit(board_image, (0, 0))

    # Draw move input and message
    input_text = font.render(f"Move: {move_input}", True, (0, 0, 0))
    message_text = font.render(message, True, (255, 0, 0))
    screen.blit(input_text, (10, 10))
    screen.blit(message_text, (10, 40))

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()