import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QGridLayout,
    QVBoxLayout,
    QLabel,
    QWidget,
    QSpacerItem,
    QSizePolicy,
    QMessageBox,
)
from PyQt5.QtCore import Qt
from database import *


# Create the Tic-Tac-Toe board
def create_board():
    return [" " for _ in range(9)]  # A 3x3 board


# Check for a win
def check_winner(board, player):
    win_conditions = [
        # Rows
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        # Columns
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        # Diagonals
        (0, 4, 8),
        (2, 4, 6),
    ]
    return any(board[i] == board[j] == board[k] == player for i, j, k in win_conditions)


# Check if the game is a tie
def is_tie(board):
    return " " not in board


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


class TicTacToe(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tic Tac Toe")
        self.setGeometry(100, 100, 300, 300)

        self.current_player = "X"  # Human player starts as X
        self.board = create_board()
        self.move_number = 0
        self.game_id = create_new_game()
        self.game_finished = False  # Track if the game has finished

        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.grid_layout = QGridLayout()
        self.central_widget.setLayout(self.grid_layout)

        self.buttons = {}
        for i in range(3):
            for j in range(3):
                button = QPushButton(" ")
                button.setFixedSize(80, 80)
                button.clicked.connect(lambda checked, x=i, y=j: self.player_move(x, y))
                self.grid_layout.addWidget(button, i, j)
                self.buttons[(i, j)] = button

    def player_move(self, x, y):
        if self.board[3 * x + y] == " " and not self.game_finished:
            self.board[3 * x + y] = self.current_player
            self.buttons[(x, y)].setText(self.current_player)
            self.move_number += 1
            save_game_state(
                self.game_id, self.board, self.current_player, self.move_number
            )

            if check_winner(self.board, self.current_player):
                QMessageBox.information(
                    self, "Game Over", f"Player {self.current_player} wins!"
                )
                save_game_result(self.game_id, self.current_player)
                self.game_finished = True  # Mark the game as finished
                self.show_play_again_prompt()
            elif self.move_number >= 9:
                QMessageBox.information(self, "Game Over", "It's a tie!")
                save_game_result(self.game_id, "Tie")
                self.game_finished = True  # Mark the game as finished
                self.show_play_again_prompt()
            else:
                self.current_player = "O"  # Set AI as O
                self.ai_move()

    def ai_move(self):
        move = minimax(self.board, self.current_player)["position"]
        self.board[move] = self.current_player
        self.buttons[(move // 3, move % 3)].setText(self.current_player)
        self.move_number += 1
        save_game_state(self.game_id, self.board, self.current_player, self.move_number)

        if check_winner(self.board, self.current_player):
            QMessageBox.information(self, "Game Over", "Player O wins!")
            save_game_result(self.game_id, "O")
            self.game_finished = True  # Mark the game as finished
            self.show_play_again_prompt()
        elif self.move_number >= 9:
            QMessageBox.information(self, "Game Over", "It's a tie!")
            save_game_result(self.game_id, "Tie")
            self.game_finished = True  # Mark the game as finished
            self.show_play_again_prompt()
        else:
            self.current_player = "X"

    def show_play_again_prompt(self):
        reply = QMessageBox.question(
            self,
            "Play Again?",
            "Do you want to play again?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.reset_game()
        else:
            self.close()  # Close the game window without saving NULL

    def reset_game(self):
        self.board = create_board()
        self.move_number = 0
        self.current_player = "X"
        self.game_id = create_new_game()
        self.game_finished = False  # Reset game finished status
        for button in self.buttons.values():
            button.setText(" ")


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tic Tac Toe - Main Menu")
        self.setGeometry(100, 100, 400, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(layout)

        # Title Label
        title_label = QLabel("Welcome to Tic Tac Toe")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Spacer
        layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        # Play Button
        play_button = QPushButton("Play")
        play_button.setFixedSize(150, 40)  # Set fixed size for the button
        play_button.setStyleSheet("font-size: 18px; padding: 10px;")
        play_button.clicked.connect(self.start_game)
        layout.addWidget(play_button, alignment=Qt.AlignCenter)  # Center the button

        # Spacer
        layout.addSpacerItem(
            QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        # Quit Button
        quit_button = QPushButton("Quit")
        quit_button.setFixedSize(150, 40)  # Set fixed size for the button
        quit_button.setStyleSheet("font-size: 18px; padding: 10px;")
        quit_button.clicked.connect(self.quit_game)
        layout.addWidget(quit_button, alignment=Qt.AlignCenter)  # Center the button

        # Additional Spacing at Bottom
        layout.addSpacerItem(
            QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

    def start_game(self):
        self.hide()  # Hide the main menu
        self.game = TicTacToe()
        self.game.show()

    def quit_game(self):
        close_connection()  # Close the database connection
        self.close()

    def closeEvent(self, event):
        close_connection()  # Ensure the connection is closed on exit
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = MainMenu()
    menu.show()
    sys.exit(app.exec_())
