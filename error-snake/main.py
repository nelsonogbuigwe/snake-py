# main.py
import pygame
from User import User
from Snake import Snake
from Database import Database

def main():
    pygame.init()
    db = Database()
    db.create_tables()
    user = User(1, 'Player1')  # Create a new user or load from database
    game = Snake(user, db)
    game.start_game()
    while not game.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and game.direction != pygame.K_DOWN:
                    game.direction = event.key
                elif event.key == pygame.K_DOWN and game.direction != pygame.K_UP:
                    game.direction = event.key
                elif event.key == pygame.K_LEFT and game.direction != pygame.K_RIGHT:
                    game.direction = event.key
                elif event.key == pygame.K_RIGHT and game.direction != pygame.K_LEFT:
                    game.direction = event.key
        game.move()
        game.draw()
        game.draw_score()
        game.draw_high_score()
        pygame.time.delay(game.speed)  # Use game speed
    game.game_over_screen()
    pygame.quit()

if __name__ == "__main__":
    main()