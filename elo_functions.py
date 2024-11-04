import logging
import sqlite3
from functools import wraps
from typing import Any, Callable, List, Optional

DATABASE_NAME = 'song_voting_app.db'
K = 32

#                                                           Database connection
# =============================================================================


def with_db_connection(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Optional[Any]:
        conn = sqlite3.connect(DATABASE_NAME)
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # Commit changes after the function runs
            return result
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            raise
        finally:
            conn.close()  # Ensure the connection is closed
            logging.info("Database connection closed.")
    return wrapper

#                                                                       Setters
# =============================================================================


@with_db_connection
def add_user(conn: sqlite3.Connection, username: str) -> None:
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username) VALUES (?)', (username,))
    logging.info(f"User '{username}' added successfully.")


@with_db_connection
def add_song(conn: sqlite3.Connection, title: str, artist: str, user_id: int, elo_score: float = 1000.0) -> None:
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO songs (title, artist, user_id, elo_rating) VALUES (?, ?, ?, ?)',
        (title, artist, user_id, elo_score)
    )
    logging.info(
        f"Song '{title}' by '{artist}' added successfully with ELO score {elo_score}.")


@with_db_connection
def vote(conn: sqlite3.Connection, user_id: int, winner_id: int, loser_id: int) -> None:
    cursor = conn.cursor()

    # Fetch current ELO ratings for the user
    cursor.execute(
        'SELECT elo_rating FROM user_song_lists WHERE user_id = ? AND song_id = ?',
        (user_id, winner_id)
    )
    winner_elo = cursor.fetchone()[0]

    cursor.execute(
        'SELECT elo_rating FROM user_song_lists WHERE user_id = ? AND song_id = ?',
        (user_id, loser_id)
    )
    loser_elo = cursor.fetchone()[0]

    # Calculate expected scores
    expected_winner = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))
    expected_loser = 1 / (1 + 10 ** ((winner_elo - loser_elo) / 400))

    # Update ratings
    new_winner_elo = winner_elo + K * (1 - expected_winner)
    new_loser_elo = loser_elo + K * (0 - expected_loser)

    # Update the user's personal song list
    cursor.execute(
        'UPDATE user_song_lists SET elo_rating = ? WHERE user_id = ? AND song_id = ?',
        (new_winner_elo, user_id, winner_id)
    )
    cursor.execute(
        'UPDATE user_song_lists SET elo_rating = ? WHERE user_id = ? AND song_id = ?',
        (new_loser_elo, user_id, loser_id)
    )

    logging.info(
        f"ELO ratings updated for user ID {user_id}: Winner (Song ID {winner_id}) -> {new_winner_elo}, Loser (Song ID {loser_id}) -> {new_loser_elo}")

#                                                                       Getters
# =============================================================================


@with_db_connection
def get_user_songs(conn: sqlite3.Connection, user_id: int) -> List[dict]:
    cursor = conn.cursor()
    cursor.execute(
        'SELECT s.song_id, s.title, s.artist, us.elo_rating '
        'FROM songs s '
        'LEFT JOIN user_song_lists us ON s.song_id = us.song_id AND us.user_id = ? '
        'WHERE s.user_id != ?',
        (user_id, user_id)
    )
    return [{'song_id': row[0], 'title': row[1], 'artist': row[2], 'elo_rating': row[3] if row[3] is not None else 1000.0} for row in cursor.fetchall()]
