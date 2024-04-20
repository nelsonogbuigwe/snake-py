# User.py
import json

class User:
    def __init__(self, id, username, highscore=0, time_played=0, games_played=None):
        self.id = id
        self.username = username
        self.highscore = highscore
        self.time_played = time_played
        self.games_played = json.loads(games_played) if games_played else {}

    def update_highscore(self, score):
        if score > self.highscore:
            self.highscore = score

    def update_time_played(self, start_time, end_time):
        self.time_played += end_time - start_time

    def update_games_played(self, game_name, score):
        self.games_played[game_name] = score