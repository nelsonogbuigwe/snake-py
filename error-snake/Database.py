# Database.py
import sqlite3
import json

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('game.db')
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY, username TEXT, highscore INTEGER, time_played TEXT, games_played TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS snake_games
                     (id INTEGER PRIMARY KEY, user_id INTEGER, score INTEGER, start_time TEXT, end_time TEXT, game_states TEXT)''')

    def get_top_users(self, limit=10):
        self.cursor.execute("SELECT * FROM users ORDER BY highscore DESC LIMIT ?", (limit,))
        return self.cursor.fetchall()
        
    def get_high_score(self, user_id):
        self.cursor.execute("SELECT highscore FROM users WHERE id = ?", (user_id,))
        return self.cursor.fetchone()[0]

    def insert_snake_game(self, user_id, score, start_time, end_time, game_states):
        self.cursor.execute("INSERT INTO snake_games VALUES (NULL, ?, ?, ?, ?, ?)",
                            (user_id, score, start_time, end_time, json.dumps(game_states)))
        self.conn.commit()