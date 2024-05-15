import pygame
import random
import time
import movement

# todo: add collision with obstacles
#       increase grid size and games speed
#       collision with self and walls
#       periodically re-generate obstacles, vary size,position,time


# stack for move history
moves = movement.MovementStack()

# Constants
SCREEN_WIDTH = 800  # Increased screen width
SCREEN_HEIGHT = 600  # Increased screen height
GRID_SIZE = 33  # Increased grid size
FPS = 14  # Reduced frame rate for slower snake movement
INITIAL_SPEED = 7  # Reduced initial speed
SPEED_INCREASE_THRESHOLD = 5
FOOD_POINTS = {'small': 1, 'medium': 2, 'large': 3}
FOOD_SIZES = {'small': 1, 'medium': 2, 'large': 3}
SHRINK_TIMER_LIMIT = 10
SHRINK_AMOUNT = 1

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
OBSTACLE_COLOR = (128, 128, 128)


# Define the SnakeGame class
class SnakeGame:
    REGENERATE_EVENT = pygame.USEREVENT + 1

    def __init__(self):
        self.game_over_sound = None
        self.food_images = None
        self.eat_sound = None
        self.obstacle_image = None
        pygame.init()
        global SCREEN_HEIGHT

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()

        SCREEN_HEIGHT = SCREEN_HEIGHT // GRID_SIZE * GRID_SIZE
        self.snake = [(SCREEN_WIDTH // 2 // GRID_SIZE * GRID_SIZE, SCREEN_HEIGHT // 2 // GRID_SIZE * GRID_SIZE)]

        self.snake_body_image = None
        self.direction = 'RIGHT'
        self.difficulty = 'normal'  # Initial difficulty level
        self.food = []
        self.obstacles = self.generate_obstacles()
        self.score = 0
        self.highest_score = self.load_highest_score()
        self.game_over = False
        self.font = pygame.font.SysFont(None, 30)
        self.load_sounds()
        self.speed = INITIAL_SPEED
        self.settings = {'collision_delay': 2, 'timer_seconds': 60}
        self.timer_start = None
        self.food_size = 'small'  # Initial food size
        self.shrink_timer = 0  # Timer for shrinking snake
        self.is_paused = False  # Flag for pause state
        self.load_assets()  # Load compact PNG images
        self.opening_menu()

        # Periodically regenerate obstacles
        pygame.time.set_timer(self.REGENERATE_EVENT, 10000)

    def load_assets(self):
        # Load compact PNG images for snake body, food items, and obstacles
        self.snake_body_image = pygame.image.load("assets/snake_body.png").convert_alpha()
        self.snake_body_image = pygame.transform.scale(self.snake_body_image, (GRID_SIZE, GRID_SIZE))

        self.food_images = {
            'small': pygame.image.load("assets/food.png").convert_alpha(),
            'medium': pygame.image.load("assets/food.png").convert_alpha(),
            'large': pygame.image.load("assets/food.png").convert_alpha()
        }
        for size in self.food_images:
            self.food_images[size] = pygame.transform.scale(self.food_images[size], (GRID_SIZE, GRID_SIZE))

        self.obstacle_image = pygame.image.load("assets/obstacle.png").convert_alpha()
        self.obstacle_image = pygame.transform.scale(self.obstacle_image, (GRID_SIZE, GRID_SIZE))

    def opening_menu(self):

        ##menu_bg = pygame.image.load("menu_bg.jpg")  # Background image for the menu
        ##menu_bg = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Resize background image
        ##self.screen.blit(menu_bg, (0, 0))  # Draw background image

        menu_font = pygame.font.SysFont(None, 50)
        menu_text = menu_font.render("Press Enter to Start", True, WHITE)
        self.screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, SCREEN_HEIGHT // 2))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.reset_game()
                        self.run()
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()

    def save_highest_score(self):
        file_name = f"highest_score_{self.difficulty}.txt"
        with open(file_name, "w") as file:
            file.write(str(max(self.score, self.highest_score)))

    def load_highest_score(self):
        file_name = f"highest_score_{self.difficulty}.txt"
        try:
            with open(file_name, "r") as file:
                return int(file.read())
        except FileNotFoundError:
            with open(file_name, "w") as file:
                file.write("0")
            return 0

    def load_sounds(self):
        try:
            self.eat_sound = pygame.mixer.Sound("assets/eat.wav")
            self.game_over_sound = pygame.mixer.Sound("assets/game_over.wav")
            self.eat_sound.set_volume(0.2)  # Reduce volume for a subtle effect
            self.game_over_sound.set_volume(0.2)  # Reduce volume for a subtle effect
        except pygame.error:
            print("Error: One or more sound files not found.")
            self.eat_sound = None
            self.game_over_sound = None

    @staticmethod
    def generate_obstacles():
        obstacles = []
        num_obstacles = random.randint(1, 5)  # Initial number of obstacles
        for _ in range(num_obstacles):
            x = random.randrange(0, SCREEN_WIDTH, GRID_SIZE)
            y = random.randrange(0, SCREEN_HEIGHT, GRID_SIZE)
            obstacles.append((x, y))
        return obstacles

    def place_food(self):
        x = random.randrange(0, SCREEN_WIDTH // GRID_SIZE) * GRID_SIZE
        y = random.randrange(0, SCREEN_HEIGHT // GRID_SIZE) * GRID_SIZE

        self.food_size = random.choice(list(FOOD_SIZES.keys()))  # Random food size
        return x, y, self.food_size

    def rotate_snake_body(self):
        if len(moves) > 0:
            current_direction = moves.get()
        else:
            current_direction = self.direction

        if self.direction == 'UP' and current_direction == 'LEFT':
            self.snake_body_image = pygame.transform.rotate(self.snake_body_image, -90)
        elif self.direction == 'UP' and current_direction == 'RIGHT':
            self.snake_body_image = pygame.transform.rotate(self.snake_body_image, 90)
        elif self.direction == 'DOWN' and current_direction == 'LEFT':
            self.snake_body_image = pygame.transform.rotate(self.snake_body_image, 90)
        elif self.direction == 'DOWN' and current_direction == 'RIGHT':
            self.snake_body_image = pygame.transform.rotate(self.snake_body_image, -90)
        elif self.direction == 'LEFT' and current_direction == 'UP':
            self.snake_body_image = pygame.transform.rotate(self.snake_body_image, 90)
        elif self.direction == 'LEFT' and current_direction == 'DOWN':
            self.snake_body_image = pygame.transform.rotate(self.snake_body_image, -90)
        elif self.direction == 'RIGHT' and current_direction == 'UP':
            self.snake_body_image = pygame.transform.rotate(self.snake_body_image, -90)
        elif self.direction == 'RIGHT' and current_direction == 'DOWN':
            self.snake_body_image = pygame.transform.rotate(self.snake_body_image, 90)

        moves.push(self.direction)

    def move(self):
        if self.is_paused:
            return

        head = self.snake[0]
        x, y = head

        if self.direction == 'UP':
            y -= GRID_SIZE
            self.rotate_snake_body()
        elif self.direction == 'DOWN':
            y += GRID_SIZE
            self.rotate_snake_body()
        elif self.direction == 'LEFT':
            x -= GRID_SIZE
            self.rotate_snake_body()
        elif self.direction == 'RIGHT':
            x += GRID_SIZE
            self.rotate_snake_body()

        if x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT:
            self.game_over = True
            if self.game_over_sound:
                self.game_over_sound.play()
            self.save_highest_score()
            return

        for f in self.food:
            if abs(x - f[0]) < GRID_SIZE and abs(y - f[1]) < GRID_SIZE:
                self.score += FOOD_POINTS.get(f[2], 1)
                if self.eat_sound:
                    self.eat_sound.play()
                self.food.remove(f)
                self.food.append(self.place_food())
                self.food_size = random.choice(list(FOOD_SIZES.keys()))  # Random food size after eating

        if time.time() - self.timer_start > SHRINK_TIMER_LIMIT:
            if len(self.snake) > SHRINK_AMOUNT:
                del self.snake[-SHRINK_AMOUNT:]

        if any(abs(x - o[0]) < GRID_SIZE and abs(y - o[1]) < GRID_SIZE for o in self.obstacles):
            self.game_over = True  # Game over on collision

        if self.food_size != 'small':
            self.timer_start = time.time()
        if (
                x < 0 or x >= SCREEN_WIDTH or
                y < 0 or y >= SCREEN_HEIGHT or
                any(abs(x - s[0]) < GRID_SIZE and abs(y - s[1]) < GRID_SIZE for s in self.snake[1:]) or
                any(abs(x - o[0]) < GRID_SIZE and abs(y - o[1]) < GRID_SIZE for o in self.obstacles)
        ):
            if time.time() - self.timer_start > self.settings['collision_delay']:
                self.game_over = True
                if self.game_over_sound:
                    self.game_over_sound.play()
                self.save_highest_score()
            return

        self.snake.insert(0, (x, y))
        if len(self.snake) > self.score + 1:
            del self.snake[-1]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_highest_score()
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != 'DOWN':
                    self.direction = 'UP'
                elif event.key == pygame.K_DOWN and self.direction != 'UP':
                    self.direction = 'DOWN'
                elif event.key == pygame.K_LEFT and self.direction != 'RIGHT':
                    self.direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and self.direction != 'LEFT':
                    self.direction = 'RIGHT'
                elif event.key == pygame.K_p:  # Pause functionality
                    self.is_paused = not self.is_paused
            elif event.type == self.REGENERATE_EVENT:
                self.obstacles = self.generate_obstacles()
                self.food = [self.place_food() for _ in range(len(self.food))]
                self.draw()

    def draw(self):
        self.screen.fill(BLACK)
        for segment in self.snake:
            self.screen.blit(self.snake_body_image, (segment[0], segment[1]))
        for f in self.food:
            self.screen.blit(self.food_images[f[2]], (f[0], f[1]))
        for obstacle in self.obstacles:
            self.screen.blit(self.obstacle_image, (obstacle[0], obstacle[1]))
        self.draw_score()
        pygame.display.update()

    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, BLUE)
        food_size_text = self.font.render(f"Food Size: {self.food_size.capitalize()}", True, GREEN)
        highest_score_text = self.font.render(f"Highest Score: {self.highest_score}", True, BLUE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(food_size_text, (10, 40))
        self.screen.blit(highest_score_text, (10, 70))

    def game_over_screen(self):
        self.screen.fill(WHITE)
        game_over_text = self.font.render("Game Over!", True, RED)
        score_text = self.font.render(f"Score: {self.score}", True, RED)
        highest_score_text = self.font.render(f"Highest Score: {self.highest_score}", True, RED)
        restart_text = self.font.render("Press R to restart", True, BLUE)
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                                          SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2 - 30))
        self.screen.blit(score_text, (
            SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - score_text.get_height() // 2))
        self.screen.blit(highest_score_text, (SCREEN_WIDTH // 2 - highest_score_text.get_width() // 2,
                                              SCREEN_HEIGHT // 2 - highest_score_text.get_height() // 2 + 30))
        self.screen.blit(restart_text, (
            SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
            SCREEN_HEIGHT // 2 - restart_text.get_height() // 2 + 60))
        pygame.display.update()

    def reset_game(self):
        self.snake = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = 'RIGHT'
        self.food = [self.place_food()]
        self.obstacles = self.generate_obstacles()
        self.score = 0
        self.game_over = False
        self.speed = INITIAL_SPEED
        self.timer_start = time.time()
        self.food_size = 'small'

    def run(self):
        self.reset_game()
        while not self.game_over:
            self.handle_events()
            self.move()
            self.draw()
            self.clock.tick(self.speed)

        while self.game_over:
            self.game_over_screen()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        pygame.time.wait(1000)  # Wait for 1 second before restarting
                        self.reset_game()
                        pygame.quit()
                        self.run()


# Entry point of the program
if __name__ == "__main__":
    game = SnakeGame()
    game.run()
