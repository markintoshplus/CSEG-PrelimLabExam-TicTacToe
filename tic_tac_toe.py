from database import *


# Create the Tic-Tac-Toe board
def create_board():
    return [" " for _ in range(9)]  # A 3x3 board


# Display the board in CLI
def display_board(board):
    print("\n")
    for i in range(3):
        print(f"{board[3*i]} | {board[3*i+1]} | {board[3*i+2]}")
        if i < 2:
            print("--+---+--")
    print("\n")


# Check for a win
def check_winner(board, player):
    win_conditions = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),  # Rows
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),  # Columns
        (0, 4, 8),
        (2, 4, 6),  # Diagonals
    ]
    return any(board[i] == board[j] == board[k] == player for i, j, k in win_conditions)


# Check if the game is a tie
def is_tie(board):
    return " " not in board


# Human player makes a move
def player_move(board, player):
    while True:
        try:
            move = int(input(f"Player {player}, enter your move (1-9): ")) - 1
            if move < 0 or move > 8:
                print("Invalid input. Please enter a number between 1 and 9.")
            elif board[move] != " ":
                print("That spot is already taken. Try again.")
            else:
                board[move] = player
                break
        except ValueError:
            print("Invalid input. Please enter a valid number.")


# Minimax algorithm for AI moves
def minimax(board, player):
    opponent = "X" if player == "O" else "O"

    if check_winner(board, "O"):
        return {"score": 1}
    elif check_winner(board, "X"):
        return {"score": -1}
    elif is_tie(board):
        return {"score": 0}

    moves = []
    for i in range(9):
        if board[i] == " ":
            board[i] = player
            result = minimax(board, opponent)
            moves.append({"position": i, "score": result["score"]})
            board[i] = " "  # Undo the move

    if player == "O":
        best_move = max(moves, key=lambda x: x["score"])
    else:
        best_move = min(moves, key=lambda x: x["score"])

    return best_move


# Game loop
def game():
    board = create_board()
    current_player = "X"
    move_number = 0

    # Create a new game and get its ID
    game_id = create_new_game()

    while True:
        display_board(board)

        if current_player == "X":  # Human player's turn
            player_move(board, current_player)
        else:  # AI player's turn
            move = minimax(board, current_player)["position"]
            board[move] = current_player
            print(f"AI chose position {move + 1}")

        move_number += 1
        save_game_state(
            game_id, board, current_player, move_number
        )  # Save game state for this game

        if check_winner(board, current_player):
            display_board(board)
            print(f"Player {current_player} wins!")
            save_game_result(game_id, current_player)  # Save the result for this game
            break
        elif is_tie(board):
            display_board(board)
            print("It's a tie!")
            save_game_result(game_id, "Tie")  # Save the result as a tie
            break

        current_player = "O" if current_player == "X" else "X"  # Switch turns


# Ask if the player wants to play again
def play_again():
    while True:
        choice = input("Do you want to play again? (y/n): ").lower()
        if choice == "y":
            return True
        elif choice == "n":
            return False
        else:
            print("Invalid choice. Please enter 'y' for yes or 'n' for no.")


def main():
    while True:
        game()
        if not play_again():
            print("Thanks for playing! Goodbye!")
            close_connection()  # Close the database connection when done
            break


if __name__ == "__main__":
    main()
