import sqlite3

from flask import Flask, jsonify, render_template, request

import elo_functions

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        try:
            elo_functions.add_user(username)
            return jsonify({'message': f"User '{username}' added successfully."})
        except sqlite3.IntegrityError:
            return jsonify({'error': f"Username '{username}' already exists."})

    return render_template('add_user.html')

# Function to add a new song


@app.route('/add_song', methods=['GET', 'POST'])
def add_song():
    if request.method == 'POST':
        data = request.get_json()
        title = data.get('title')
        artist = data.get('artist')
        try:
            elo_functions.add_song(title, artist)
            return jsonify({'message': f"Song '{title}' by '{artist}' added successfully."})
        except Exception as e:
            return jsonify({'error': str(e)})

    return render_template('add_song.html')


@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        data = request.get_json()
        winner_id = data.get('winner_id')
        loser_id = data.get('loser_id')
        try:
            elo_functions.vote(winner_id, loser_id)
            return jsonify({'message': f"Vote recorded: Winner ID {winner_id}, Loser ID {loser_id}."})
        except Exception as e:
            return jsonify({'error': str(e)})

    return render_template('vote.html')


@app.route('/get_songs', methods=['GET'])
def get_songs():
    # Ensure this function fetches all songs from the database
    songs = elo_functions.get_all_songs()
    return jsonify({'songs': songs})


@ app.route('/show_database', methods=['GET'])
def show_database():
    conn = sqlite3.connect('song_voting_app.db')
    cursor = conn.cursor()

    # Fetch data from users table
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    # Fetch data from songs table
    cursor.execute('SELECT * FROM songs')
    songs = cursor.fetchall()

    # Fetch data from song_submissions table
    cursor.execute('SELECT * FROM song_submissions')
    submissions = cursor.fetchall()

    conn.close()

    # Format data as HTML
    html_content = "<h1>Database Contents</h1>"

    html_content += "<h2>Users</h2><ul>"
    for user in users:
        html_content += f"<li>User ID: {user[0]}, Username: {user[1]}, Created At: {user[2]}</li>"
    html_content += "</ul>"

    html_content += "<h2>Songs</h2><ul>"
    for song in songs:
        html_content += f"<li>Song ID: {song[0]}, Title: {song[1]}, Artist: {song[2]}, Created At: {song[3]}</li>"
    html_content += "</ul>"

    html_content += "<h2>Song Submissions</h2><ul>"
    for submission in submissions:
        html_content += (f"<li>Submission ID: {submission[0]}, User ID: {submission[1]}, "
                         f"Song List: {submission[2]}, ELO Rating: {submission[3]}, "
                         f"Created At: {submission[4]}</li>")
    html_content += "</ul>"

    return html_content


if __name__ == '__main__':
    app.run(debug=True)
