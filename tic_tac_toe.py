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
    QTableWidget,
    QTableWidgetItem,
    QRadioButton,
    QButtonGroup,
    QScrollArea,
    QHBoxLayout
)
from PyQt5.QtCore import (Qt, QDateTime)
from database import *
import random

BOARD_SIZE = 9
BOARD_DIM = 3

# Create the Tic-Tac-Toe board
def create_board():
    return [" " for _ in range(BOARD_SIZE)]  # A 3x3 board


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
    for i in range(BOARD_SIZE):
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


# Tic Tac Toe Interface
class TicTacToe(QMainWindow):
    def __init__(self, difficulty):
        super().__init__()
        self.setWindowTitle("Tic Tac Toe")
        self.setGeometry(100, 100, 400, 400)

        self.current_player = "X"  # Human player starts as X
        self.board = create_board()
        self.move_number = 0
        self.game_id = create_new_game()
        self.game_finished = False  # Track if the game has finished
        self.difficulty = difficulty  # Store the selected difficulty

        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.grid_layout = QGridLayout()
        self.central_widget.setLayout(self.grid_layout)

        self.buttons = {}
        for i in range(BOARD_DIM):
            for j in range(BOARD_DIM):
                button = QPushButton(" ")
                button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                button.setStyleSheet("font-size: 24px;")
                button.clicked.connect(lambda checked, x=i, y=j: self.player_move(x, y))
                self.grid_layout.addWidget(button, i, j)
                self.buttons[(i, j)] = button

    def player_move(self, x, y):
        if self.board[BOARD_DIM * x + y] == " " and not self.game_finished:
            self.board[BOARD_DIM * x + y] = self.current_player
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
            elif self.move_number >= BOARD_SIZE:
                QMessageBox.information(self, "Game Over", "It's a tie!")
                save_game_result(self.game_id, "TIE")
                self.game_finished = True  # Mark the game as finished
                self.show_play_again_prompt()
            else:
                self.current_player = "O"  # Set AI as O
                self.ai_move()

    def ai_move(self):
        if self.difficulty == "easy":
            move = random.choice([i for i, spot in enumerate(self.board) if spot == " "])
        elif self.difficulty == "medium":
            if random.choice([True, False]):
                move = random.choice([i for i, spot in enumerate(self.board) if spot == " "])
            else:
                move = minimax(self.board, self.current_player)["position"]
        else:  # Hard difficulty
            move = minimax(self.board, self.current_player)["position"]

        self.make_move(move)

    def make_move(self, move):
        self.board[move] = self.current_player
        self.buttons[(move // BOARD_DIM, move % BOARD_DIM)].setText(self.current_player)
        self.move_number += 1
        save_game_state(self.game_id, self.board, self.current_player, self.move_number)

        if check_winner(self.board, self.current_player):
            QMessageBox.information(self, "Game Over", f"Player {self.current_player} wins!")
            save_game_result(self.game_id, self.current_player)
            self.game_finished = True  # Mark the game as finished
            self.show_play_again_prompt()
        elif self.move_number >= BOARD_SIZE:
            QMessageBox.information(self, "Game Over", "It's a tie!")
            save_game_result(self.game_id, "TIE")
            self.game_finished = True  # Mark the game as finished
            self.show_play_again_prompt()
        else:
            self.current_player = "X" if self.current_player == "O" else "O"

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
            self.main_menu = MainMenu()  # Create an instance of MainMenu
            self.main_menu.show()  # Show the main menu
            self.close()  # Close the current game window

    def reset_game(self):
        self.board = create_board()
        self.move_number = 0
        self.current_player = "X"
        self.game_id = create_new_game()
        self.game_finished = False  # Reset game finished status
        for button in self.buttons.values():
            button.setText(" ")

    def closeEvent(self, event):
        if not self.game_finished:
            save_game_result(self.game_id, "QUIT")  # Save the game result as "QUIT"
        event.accept()  # Accept the close event

# Main Menu interface
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
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Spacer
        layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        # Difficulty Selection
        difficulty_label = QLabel("Select Difficulty:")
        difficulty_label.setStyleSheet("font-size: 18px;")
        layout.addWidget(difficulty_label, alignment=Qt.AlignCenter)

        self.difficulty_group = QButtonGroup(self)
        self.easy_button = QRadioButton("Easy")
        self.medium_button = QRadioButton("Medium")
        self.hard_button = QRadioButton("Hard")
        self.easy_button.setChecked(True)  # Default to Easy

        self.difficulty_group.addButton(self.easy_button)
        self.difficulty_group.addButton(self.medium_button)
        self.difficulty_group.addButton(self.hard_button)

        layout.addWidget(self.easy_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.medium_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.hard_button, alignment=Qt.AlignCenter)

        # Spacer
        layout.addSpacerItem(
            QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        # Play Button
        play_button = QPushButton("Play")
        layout.addWidget(play_button, alignment=Qt.AlignCenter)
        play_button.clicked.connect(self.start_game)

        # Spacer
        layout.addSpacerItem(
            QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        # History Button
        history_button = QPushButton("History")
        layout.addWidget(history_button, alignment=Qt.AlignCenter)
        history_button.clicked.connect(self.open_History)

        # Spacer
        layout.addSpacerItem(
            QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        # Quit Button
        quit_button = QPushButton("Quit")
        layout.addWidget(quit_button, alignment=Qt.AlignCenter)
        quit_button.clicked.connect(self.quit_game)

        # Additional Spacing at Bottom
        layout.addSpacerItem(
            QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

    def start_game(self):
        self.hide()  # Hide the main menu
        difficulty = "easy" if self.easy_button.isChecked() else "medium" if self.medium_button.isChecked() else "hard"
        self.game = TicTacToe(difficulty)
        self.game.show()

    def quit_game(self):
        close_connection()  # Close the database connection
        self.close()

    def closeEvent(self, event):
        close_connection()  # Ensure the connection is closed on exit
        event.accept()

    def open_History(self):
        self.hide()  # Hide the main menu
        self.history_window = HistoryWindow()
        self.history_window.show()

class HistoryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game History")
        self.setGeometry(100, 100, 600, 400)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(layout)

        # Title Label
        title_label = QLabel("Recent Matches")
        title_label.setObjectName("historyTitle")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Table Widget
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["Game ID", "Winner", "Date/Time"])
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_widget.cellDoubleClicked.connect(self.show_match_details)
        layout.addWidget(self.table_widget)

        # Fetch and display recent matches
        self.display_recent_matches()

        # Back Button
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.back_to_menu)
        layout.addWidget(back_button)

    def display_recent_matches(self):
        recent_matches = get_recent_matches()  # Fetch all matches from the database

        if not recent_matches:
            no_matches_label = QLabel("No matches found.")
            no_matches_label.setAlignment(Qt.AlignCenter)
            self.table_widget.setRowCount(0)
            self.table_widget.setCellWidget(0, 0, no_matches_label)
            return

        self.table_widget.setRowCount(len(recent_matches))
        for row, (game_id, winner, timestamp) in enumerate(recent_matches):
            self.table_widget.setItem(row, 0, QTableWidgetItem(str(game_id)))
            self.table_widget.setItem(row, 1, QTableWidgetItem(winner))
            self.table_widget.setItem(row, 2, QTableWidgetItem(timestamp))

    def show_match_details(self, row, column):
        game_id = int(self.table_widget.item(row, 0).text())
        self.hide()
        self.match_details_window = MatchDetailsWindow(game_id)
        self.match_details_window.show()

    def back_to_menu(self):
        self.hide()
        self.main_menu = MainMenu()
        self.main_menu.show()

class MatchDetailsWindow(QMainWindow):
    def __init__(self, game_id):
        super().__init__()
        self.setWindowTitle(f"Match Details - Game ID: {game_id}")
        self.setGeometry(100, 100, 400, 400)

        self.game_id = game_id
        self.moves = get_match_details(game_id)  # Fetch match details from the database
        self.current_move_index = 0
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Title Label
        title_label = QLabel(f"Match Details for Game ID: {self.game_id}")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title_label)

        # Tic Tac Toe Board
        self.board_layout = QGridLayout()
        self.buttons = {}
        for i in range(BOARD_DIM):
            for j in range(BOARD_DIM):
                button = QPushButton(" ")
                button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                button.setStyleSheet("font-size: 24px;")
                self.board_layout.addWidget(button, i, j)
                self.buttons[(i, j)] = button
        self.layout.addLayout(self.board_layout)

        # Navigation Buttons
        self.nav_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.show_previous_move)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.show_next_move)
        self.nav_layout.addWidget(self.prev_button)
        self.nav_layout.addWidget(self.next_button)
        self.layout.addLayout(self.nav_layout)

        # Back Button
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.back_to_history)
        self.layout.addWidget(self.back_button)

        # Display the first move
        self.display_move(self.current_move_index)

    def display_move(self, move_index):
        if 0 <= move_index < len(self.moves):
            move_number, board_state, current_player = self.moves[move_index]
            for i in range(BOARD_DIM):
                for j in range(BOARD_DIM):
                    self.buttons[(i, j)].setText(board_state[BOARD_DIM * i + j])

    def show_previous_move(self):
        if self.current_move_index > 0:
            self.current_move_index -= 1
            self.display_move(self.current_move_index)

    def show_next_move(self):
        if self.current_move_index < len(self.moves) - 1:
            self.current_move_index += 1
            self.display_move(self.current_move_index)

    def back_to_history(self):
        self.hide()
        self.history_window = HistoryWindow()
        self.history_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Load the stylesheet
    with open("styles.qss", "r") as file:
        app.setStyleSheet(file.read())
    
    menu = MainMenu()
    menu.show()
    sys.exit(app.exec_())
