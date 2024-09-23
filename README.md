---

# Tic-Tac-Toe Game with AI and Database Integration

## Overview

This is a graphical Tic-Tac-Toe game where a human player competes against an AI player using the Minimax algorithm. The game integrates a SQLite database to store game states and results. Players can play multiple rounds, with each round's states and results saved and linked in the database.

## Features

- **Single-player game**: A human player ("X") versus an AI player ("O").
- **AI decision-making**: The AI uses the Minimax algorithm to determine optimal moves.
- **Persistent storage**: Game states and results are stored in a SQLite database.
- **Play multiple rounds**: After each game, players can choose to play again.
- **Game history**: All games and their moves are saved in the database for future reference.
- **Difficulty levels**: Choose between Easy, Medium, and Hard difficulty levels for the AI.
- **Game history and details**: View recent matches and detailed move-by-move history of each game.

## How It Works

- **Game State**: The current state of the game board, player moves, and move numbers are stored in the `game_state` table.
- **Game Result**: The result of each game (win, tie, or in-progress) is stored in the `game_result` table.
- **AI Player**: The AI uses the Minimax algorithm to calculate the best possible move at every turn.
- **Difficulty Levels**: The AI's decision-making process varies based on the selected difficulty level (Easy, Medium, Hard).

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Database Schema](#database-schema)
- [How It Works](#how-it-works)
- [License](#license)

## Requirements

- Python 3.6+
- SQLite (included with Python's `sqlite3` module)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/markintoshplus/CSEG5-LabExam-TicTacToe.git
    ```

2. Navigate to the project directory:

    ```bash
    cd CSEG5-LabExam-TicTacToe
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the game:

    ```bash
    python tic_tac_toe.py
    ```

## How to Play

1. The game opens in a GUI window.
2. The human player is assigned "X" and the AI player is assigned "O".
3. Players take turns by clicking on the board positions.
4. The game continues until either player wins or a tie occurs.
5. After each game, you will be prompted to play again. Choose "Yes" to play another round or "No" to exit.
6. You can view the history of recent matches and detailed move-by-move history of each game.

## Database Schema

The game data is stored in a SQLite database (`tic_tac_toe.db`) with two tables:

1. **`game_state`**: Stores the game states (board position, current player, and move number) for each game.
   
    ```sql
    CREATE TABLE game_state (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_id INTEGER,
        board_state TEXT NOT NULL,
        current_player TEXT NOT NULL,
        move_number INTEGER NOT NULL,
        FOREIGN KEY (game_id) REFERENCES game_result(game_id)
    );
    ```

2. **`game_result`**: Stores the results of each game (whether the game was won, tied, or in progress).
   
    ```sql
    CREATE TABLE game_result (
        game_id INTEGER PRIMARY KEY AUTOINCREMENT,
        winner TEXT,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ```

- **game_id**: Links the game states to the corresponding game result.
- **board_state**: Represents the current state of the board as a string (e.g., `'XOXOXOXOX'`).

## How It Works

- **Minimax Algorithm**: The AI player uses Minimax, which recursively evaluates all possible game states to select the best move while minimizing potential losses by considering the opponent's moves.
- **Persistent Storage**: Each move is recorded in the database, and the final result of the game is stored once completed. Past games can be queried from the database.
- **Playing Multiple Rounds**: After each round, players can opt to play again. If yes, a new game starts, with its states and results stored separately in the database.
- **Difficulty Levels**: The AI's decision-making process varies based on the selected difficulty level (Easy, Medium, Hard).

## License

This project is licensed under the MIT License. Feel free to use and modify the code for your own purposes.

---