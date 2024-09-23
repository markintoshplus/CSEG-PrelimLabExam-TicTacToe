import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("tic_tac_toe.db")
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute(
    """CREATE TABLE IF NOT EXISTS game_state (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     game_id INTEGER,
                     board_state TEXT NOT NULL,
                     current_player TEXT NOT NULL,
                     move_number INTEGER NOT NULL,
                     FOREIGN KEY (game_id) REFERENCES game_result(game_id))"""
)

cursor.execute(
    """CREATE TABLE IF NOT EXISTS game_result (
                     game_id INTEGER PRIMARY KEY AUTOINCREMENT,
                     winner TEXT,
                     date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""
)

# Create a new game and get the game_id
def create_new_game():
    cursor.execute(
        """INSERT INTO game_result (winner) VALUES (NULL)"""
    )
    conn.commit()
    return cursor.lastrowid

# Save the current board state
def save_game_state(game_id, board, current_player, move_number):
    board_state = "".join(board)  # Convert board list to a string
    cursor.execute(
        """INSERT INTO game_state (game_id, board_state, current_player, move_number)
                      VALUES (?, ?, ?, ?)""",
        (game_id, board_state, current_player, move_number),
    )
    conn.commit()

# Update the game result when the game is over
def save_game_result(game_id, winner):
    cursor.execute(
        """UPDATE game_result SET winner = ? WHERE game_id = ?""",
        (winner if winner is not None else "QUIT", game_id),
    )
    conn.commit()

# Fetch most recent matches from db
def get_recent_matches(limit=5):
    query = "SELECT game_id, winner, date FROM game_result ORDER BY date DESC LIMIT ?"
    result = execute_query(query, (limit,))
    return result

# Executes a query and returns the result
def execute_query(query, params=()):
    conn = sqlite3.connect('tic_tac_toe.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        conn.close()

# Close the database connection
def close_connection():
    conn.close()
