import logging
import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('song_voting_app.db')
cursor = conn.cursor()

# Create a table for users
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Create a table for songs
cursor.execute('''
CREATE TABLE IF NOT EXISTS songs (
    song_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    user_id INTEGER NOT NULL,  -- Foreign key for user who submitted the song
    elo_rating REAL DEFAULT 1000.0,  -- Default ELO rating for the song
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
)
''')

# Create a table for user song lists (to track ELO ratings for user-specific songs)
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_song_lists (
    user_id INTEGER NOT NULL,
    song_id INTEGER NOT NULL,
    elo_rating REAL DEFAULT 1000.0,  -- Default ELO rating for user's song
    PRIMARY KEY (user_id, song_id),  -- Composite primary key
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (song_id) REFERENCES songs (song_id)
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

logging.info("Database and tables created successfully.")
