# Snake.py
import pygame
import random
from Game import Game

class Snake(Game):
    def __init__(self, user, db):
        super().__init__(user)
        self.db = db
        self.snake = [[4, 4]]
        self.food = None
        self.score = 0
        self.direction = pygame.K_RIGHT
        self.game_over = False
        self.board_size = 20
        self.game_states = []
        self.block_size = 20  # Size of each block in pixels
        self.screen = pygame.display.set_mode((self.board_size * self.block_size, self.board_size * self.block_size))
        self.speed = 100  # Initial speed
        self.font = pygame.font.Font('freesansbold.ttf', 32) 
    def start_game(self):
        super().start_game()
        self._place_food()

    def _place_food(self):
        while True:
            pos = [random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)]
            if pos not in self.snake:
                self.food = pos
                break

    def move(self):
        head = self.snake[0][:]
        if self.direction == pygame.K_RIGHT:
            head[0] = (head[0] + 1) % self.board_size
        elif self.direction == pygame.K_LEFT:
            head[0] = (head[0] - 1) % self.board_size
        elif self.direction == pygame.K_UP:
            head[1] = (head[1] - 1) % self.board_size
        elif self.direction == pygame.K_DOWN:
            head[1] = (head[1] + 1) % self.board_size
        if head in self.snake:
            self.game_over = True
            self.end_game()
            return
        self.snake.insert(0, head)
        if head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        self._collect_game_state()

    def _collect_game_state(self):
        self.game_states.append({
            'snake': self.snake,
            'food': self.food,
            'score': self.score,
            'direction': self.direction
        })

    def end_game(self):
        super().end_game()
        self.user.games_played['Snake'] = self.score
        self.db.insert_snake_game(self.user.id, self.score, self.start_time, self.end_time, self.game_states)

    def calculate_score(self):
        return self.score

    def draw(self):
        self.screen.fill((0, 0, 0))  # Fill the screen with black
        for position in self.snake:
            pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(position[0] * self.block_size, position[1] * self.block_size, self.block_size, self.block_size))  # Draw the snake
        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(self.food[0] * self.block_size, self.food[1] * self.block_size, self.block_size, self.block_size))  # Draw the food
        pygame.display.update()

    def draw_score(self):
            text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
            self.screen.blit(text, (10, 10))  # Draw the score at a fixed position
    
    def draw_high_score(self):
        high_score = self.db.get_high_score(self.user.id)
        text = self.font.render(f"High Score: {high_score}", True, (255, 255, 255))
        self.screen.blit(text, (self.board_size * self.block_size - text.get_width() - 10, 10))  # Draw the high score at a fixed position

    def game_over_screen(self):
        self.screen.fill((0, 0, 0))  # Fill the screen with black
        game_over_text = self.font.render("Game Over", True, (255, 255, 255))
        score_text = self.font.render(f"Final Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(game_over_text, (self.board_size * self.block_size // 2 - game_over_text.get_width() // 2, self.board_size * self.block_size // 2 - game_over_text.get_height() // 2))
        self.screen.blit(score_text, (self.board_size * self.block_size // 2 - score_text.get_width() // 2, self.board_size * self.block_size // 2 + game_over_text.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(2000)  # Wait for 2 seconds before quitting