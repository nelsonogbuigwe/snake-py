# GUI.py
import tkinter as tk
from User import User
from Snake import Snake
# Import other games here

class GUI:
    def __init__(self, db):
        self.db = db
        self.root = tk.Tk()
        self.root.title("Game App")
        self.username_entry = None
        self.user = None
        self.game = None
        self.canvas = None

    def start(self):
        self._render_homepage()
        self.root.mainloop()

    def _render_homepage(self):
        tk.Label(self.root, text="Enter your username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()
        tk.Button(self.root, text="Start", command=self._start_game).pack()

    def _start_game(self):
        username = self.username_entry.get()
        user_data = self.db.get_user(username)
        if user_data is None:
            self.user = User(len(self.db.get_all_users()) + 1, username)
            self.db.insert_user(self.user)
        else:
            self.user = User(*user_data)
        self._render_game_selection()

    def _render_game_selection(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text=f"Welcome, {self.user.username}! Your high score: {self.user.highscore}").pack()
        tk.Label(self.root, text="Select a game").pack()
        tk.Button(self.root, text="Snake", command=self._start_snake).pack()
        # Add buttons for other games here
        
    def _render_leaderboard(self):
            for widget in self.root.winfo_children():
                widget.destroy()
            tk.Label(self.root, text="Leaderboard").pack()
            top_users = self.db.get_top_users()
            for i, user_data in enumerate(top_users):
                user = User(*user_data)
                tk.Label(self.root, text=f"{i + 1}. {user.username}: {user.highscore}").pack()
            tk.Button(self.root, text="Back to game selection", command=self._render_game_selection).pack()

    def _start_snake(self):
        self.game = Snake(self.user)
        self.game.start_game()
                self._render_game()

    def _render_game(self):
        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack()
        self.root.bind("<Key>", self._key_press)
        self._update_game()

    def _key_press(self, event):
        if event.keysym == "Up":
            self.game.direction = "Up"
        elif event.keysym == "Down":
            self.game.direction = "Down"
        elif event.keysym == "Left":
            self.game.direction = "Left"
        elif event.keysym == "Right":
            self.game.direction = "Right"

    def _update_game(self):
        if self.game.game_over:
            self.db.update_user(self.user)
            self._render_game_over()
            return
                self.canvas.delete("all")
                self.game.move()
                for i, point in enumerate(self.game.snake):
                    x = point[0] * 25
                    y = point[1] * 25
                    self.canvas.create_rectangle(x, y, x + 25, y + 25, fill="green" if i == 0 else "black")
                x = self.game.food[0] * 25
                y = self.game.food[1] * 25
                self.canvas.create_rectangle(x, y, x + 25, y + 25, fill="red")
                self.root.after(100, self._update_game)
        
            def _render_game_over(self):
                for widget in self.root.winfo_children():
                    widget.destroy()
                tk.Label(self.root, text="Game Over").pack()
                tk.Label(self.root, text=f"Your score: {self.game.calculate_score()}").pack()
                tk.Button(self.root, text="Back to game selection", command=self._render_game_selection).pack()