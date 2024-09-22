---

# Tic-Tac-Toe Game with AI and Database Integration

## Overview

This is a command-line Tic-Tac-Toe game where a human player competes against an AI player that uses the Minimax algorithm. The game also integrates a SQLite database to store game states and results. Players can play multiple rounds, and the game states and results for each round are saved and linked in the database.

## Features

- **Two-player game**: A human player ("X") versus an AI player ("O").
- **AI decision-making**: The AI player uses the Minimax algorithm to determine optimal moves.
- **Persistent storage**: Game states and results are stored in a SQLite database.
- **Play multiple rounds**: After each game, players are asked if they want to play again.
- **Game history**: Every game and its moves are saved to the database for future reference.

## How It Works

- **Game State**: The current state of the game board, player moves, and move numbers are stored in the `game_state` table.
- **Game Result**: The result of each game (win, tie, or in-progress) is stored in the `game_result` table.
- **AI Player**: The AI uses the Minimax algorithm to calculate the best possible move at every turn.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Database Schema](#database-schema)
- [How It Works](#how-it-works)
- [License](#license)

## Requirements

- Python 3.6+
- SQLite (no additional installation needed, as it's included with Python's `sqlite3` module)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/markintoshplus/CSEG5-LabExam-TicTacToe.git
    ```

2. Navigate to the project directory:

    ```bash
    cd CSEG5-LabExam-TicTacToe
    ```

3. Run the game:

    ```bash
    python tic_tac_toe.py
    ```

## How to Play

1. The game is played in the terminal.
2. The human player is assigned "X" and the AI player is assigned "O".
3. Players take turns by entering a number (1-9) corresponding to the board position:

    ```
     1 | 2 | 3
    -----------
     4 | 5 | 6
    -----------
     7 | 8 | 9
    ```

4. The game continues until either player wins or a tie occurs.
5. At the end of each game, you will be prompted to play again. Enter `y` to play another round or `n` to exit.

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

- **Minimax Algorithm**: The AI player uses Minimax, which recursively evaluates all possible game states to select the best move. It minimizes the possible loss by considering the opponent's best moves as well.
- **Persistent Storage**: Each move is recorded in the database, and the final result of the game is stored once the game is complete. You can query the database to review past games.
- **Playing Multiple Rounds**: After each round, the player is given the option to play again. If they choose yes, a new game starts, and its game states and results are stored separately in the database.

## Example Game Play

```
Player X, enter your move (1-9): 1

 X |   |  
-----------
   |   |  
-----------
   |   |  

AI chose position 5

 X |   |  
-----------
   | O |  
-----------
   |   |  

Player X, enter your move (1-9): 2
...
```

## License

This project is licensed under the MIT License. Feel free to use and modify the code for your own purposes.

---