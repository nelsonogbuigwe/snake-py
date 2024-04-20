# Game.py
import time

class Game:
    def __init__(self, user):
        self.user = user
        self.start_time = None
        self.end_time = None
    
    def start_game(self):
            self.start_time = time.time()
    
    def end_game(self):
            self.end_time = time.time()
            self.user.update_time_played(self.start_time, self.end_time)
            score = self.calculate_score()
            self.user.update_highscore(score)
            self.user.update_games_played(self.__class__.__name__, score)
    
    def calculate_score(self):
            pass