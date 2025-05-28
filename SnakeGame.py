# Snake game (My own version)
# Inspired by Bro Code
# I used pygame because for me it's better than tkinter cuz I also imported mp3s

import pygame
import random
import os


class Config:
    # Display window
    TILE_SIZE = 60
    COLS, ROWS = 10, 10
    WIDTH, HEIGHT = TILE_SIZE * COLS, TILE_SIZE * ROWS
    # Colours
    BG_COLOUR_1 = "#63955B"
    BG_COLOUR_2 = "#99C06D"
    RED = "#8B0000" # not to get confused with the skin
    BLACK = "#000000"
    DARK_GREEN = "#006400"
    BOCCHI_PINK = "#e8a7a1"
    BOCCHI_YELLOW = "#ffff3d"
    BOCCHI_BLUE = "#7db0a7"
    MY_PFP_COLOUR = "#7E93AE"
    
    SNAKE_SKINS = ["#ffff3d", "#e8a7a1", "#ff3232", "#7db0a7"]
    # randomize whenever you play
    # very customizable change if you want
    # Bocchi The Rock color palette
    HIGH_SCORE_FILE = "PyGame/SnakeGame/SnakeHighscore.json"
    # all sound effects // change however you want
    AUDIO_PATHS = {
        "music": "PyGame/SnakeGame/audio.mp3",
        "eat": "PyGame/SnakeGame/Voicy_Rock You.mp3",
        "gameover": "PyGame/SnakeGame/Voicy_Attempting To Show Obedience.mp3"
    }
    SNAKE_HEAD_IMG_PATH = "PyGame/SnakeGame/snake_head.jpg"


class AssetManager:
    def __init__(self):
        pygame.mixer.music.load(Config.AUDIO_PATHS["music"])
        pygame.mixer.music.set_volume(0.1)
        self.eat_sound = pygame.mixer.Sound(Config.AUDIO_PATHS["eat"])
        self.gameover_sound = pygame.mixer.Sound(Config.AUDIO_PATHS["gameover"])
        self.snake_head_img = pygame.transform.scale(
            pygame.image.load(Config.SNAKE_HEAD_IMG_PATH),
            (Config.TILE_SIZE, Config.TILE_SIZE)
        )
        # Fonts // change font however you want
        self.font = pygame.font.SysFont("Times New Roman", 25)
        self.big_font = pygame.font.SysFont("Times New Roman", 60)

# High Score // sets your personal highscore through a save json file
class HighScoreManager:
    def __init__(self):
        if not os.path.exists(Config.HIGH_SCORE_FILE):
            with open(Config.HIGH_SCORE_FILE, "w") as f:
                f.write("0")
        with open(Config.HIGH_SCORE_FILE, "r") as f:
            self.best = int(f.read())

    def update(self, score):
        if score > self.best:
            self.best = score
            with open(Config.HIGH_SCORE_FILE, "w") as f:
                f.write(str(score))

# Main Class with multiple game loops
class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
        pygame.display.set_caption("Bocchi's Snake Game")
        self.clock = pygame.time.Clock()
        self.assets = AssetManager()
        self.high_score = HighScoreManager()

    def random_skin(self):
        return random.choice(Config.SNAKE_SKINS)

    def draw_checkered_bg(self):
        for y in range(Config.ROWS):
            for x in range(Config.COLS):
                color = Config.BG_COLOUR_1 if (x + y) % 2 == 0 else Config.BG_COLOUR_2
                rect = (x * Config.TILE_SIZE, y * Config.TILE_SIZE, Config.TILE_SIZE, Config.TILE_SIZE)
                pygame.draw.rect(self.screen, color, rect)

    def draw_snake(self, snake, direction, color):
        for i, (x, y) in enumerate(snake):
            if i == 0:
                head_rotated = pygame.transform.rotate(self.assets.snake_head_img, {
                    "UP": 0, "DOWN": 180, "LEFT": 90, "RIGHT": -90
                }[direction])
                self.screen.blit(head_rotated, (x * Config.TILE_SIZE, y * Config.TILE_SIZE))
            else:
                pygame.draw.rect(self.screen, color,
                                 (x * Config.TILE_SIZE, y * Config.TILE_SIZE, Config.TILE_SIZE, Config.TILE_SIZE))

    def draw_text(self, text, font, color, x, y, center=False):
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(x, y)) if center else surface.get_rect(topleft=(x, y))
        self.screen.blit(surface, rect)

    def wrapping(self, x, y):
        return x % Config.COLS, y % Config.ROWS

    def show_menu(self):
        while True:
            self.screen.fill(Config.BOCCHI_PINK)
            self.draw_text("SNAKE GAME", self.assets.big_font, Config.BLACK, Config.WIDTH // 2, Config.HEIGHT // 3, True)
            self.draw_text("Press ENTER to Play", self.assets.font, Config.BLACK, Config.WIDTH // 2, Config.HEIGHT // 2, True)
            self.draw_text("Inspired by Bro Code", self.assets.font, Config.DARK_GREEN, Config.WIDTH // 2, Config.HEIGHT // 2.5, True)
            self.draw_text("WASD Controls", self.assets.font, Config.RED, Config.WIDTH // 2, Config.HEIGHT // 2 + 40, True)
            self.draw_text("Made by _Bunccep", self.assets.font, Config.MY_PFP_COLOUR, Config.WIDTH // 2, Config.HEIGHT // 2 + 70, True)
            self.draw_text("---->", self.assets.big_font, Config.BOCCHI_YELLOW, Config.WIDTH // 2, Config.HEIGHT // 2 + 120, True)
            self.draw_text("<----", self.assets.big_font, Config.BOCCHI_BLUE, Config.WIDTH // 2, Config.HEIGHT // 2 + 160, True)
            pygame.display.update()
            self.assets.gameover_sound.stop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return

    def game_over(self, score):
        self.assets.gameover_sound.play()
        self.assets.eat_sound.stop()
        pygame.mixer.music.stop()
        self.screen.fill(Config.BG_COLOUR_2)
        self.draw_text("Game Over!(-_-)", self.assets.big_font, Config.RED, Config.WIDTH // 2, Config.HEIGHT // 3, True)
        self.draw_text(f"Score: {score}", self.assets.font, Config.BOCCHI_YELLOW, Config.WIDTH // 2, Config.HEIGHT // 2, True)
        self.draw_text(f"Best: {self.high_score.best}", self.assets.font, Config.BOCCHI_BLUE, Config.WIDTH // 2, Config.HEIGHT // 2 + 30, True)
        self.draw_text("Press R or ESC", self.assets.font, Config.DARK_GREEN, Config.WIDTH // 2, Config.HEIGHT // 2 + 70, True)
        self.draw_text("Inspired by Bocchi The Rock", self.assets.font, Config.BOCCHI_PINK, Config.WIDTH // 2, Config.HEIGHT // 2 + 100, True)
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return True
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

    def run(self):
        while True:
            self.show_menu()
            pygame.mixer.music.play(-1)
            snake = [(10, 10)]
            direction = "RIGHT"
            food = (random.randint(0, Config.COLS - 1), random.randint(0, Config.ROWS - 1))
            score = 0
            color = self.random_skin()

            while True:
                self.clock.tick(15)
                self.draw_checkered_bg()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                keys = pygame.key.get_pressed()
                if keys[pygame.K_w] and direction != "DOWN":
                    direction = "UP"
                elif keys[pygame.K_s] and direction != "UP":
                    direction = "DOWN"
                elif keys[pygame.K_a] and direction != "RIGHT":
                    direction = "LEFT"
                elif keys[pygame.K_d] and direction != "LEFT":
                    direction = "RIGHT"

                x, y = snake[0]
                if direction == "UP":
                    y -= 1
                elif direction == "DOWN":
                    y += 1
                elif direction == "LEFT":
                    x -= 1
                elif direction == "RIGHT":
                    x += 1

                x, y = self.wrapping(x, y)
                new_head = (x, y)

                if new_head in snake:
                    self.high_score.update(score)
                    if self.game_over(score):
                        break

                snake.insert(0, new_head)
                if new_head == food:
                    self.assets.eat_sound.play()
                    score += 1
                    food = (random.randint(0, Config.COLS - 1), random.randint(0, Config.ROWS - 1))
                else:
                    snake.pop()

                self.draw_snake(snake, direction, color)
                pygame.draw.rect(self.screen, Config.RED,
                                 (food[0] * Config.TILE_SIZE, food[1] * Config.TILE_SIZE, Config.TILE_SIZE, Config.TILE_SIZE))

                self.draw_text(f"Score: {score}", self.assets.font, Config.BLACK, 10, 10)
                self.draw_text(f"Best: {self.high_score.best}", self.assets.font, Config.BLACK, 10, 40)
                pygame.display.update()


if __name__ == "__main__":
    SnakeGame().run()
