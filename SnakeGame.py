# Snake game (My own version)
# Inspired by Bro Code
# I used pygame because for me it's better than Tkinter cuz I also imported mp3s
import pygame
import random
import os

pygame.init()

# Display window
TILE_SIZE = 60  # Larger size
COLS, ROWS = 10, 10 
WIDTH, HEIGHT = TILE_SIZE * COLS, TILE_SIZE * ROWS
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bocchi's Snake Game") # title window

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

# randomize whenever you play
# very customizable change if you want
# Bocchi The Rock color palette
snake_skins = [
    "#ffff3d", # Yellow
    "#e8a7a1", # Pink
    "#ff3232", # Red
    "#7db0a7", # Blue
]

# all sound effects // change however you want
pygame.mixer.music.load("audio.mp3")
pygame.mixer.music.set_volume(0.1)
eat_sound = pygame.mixer.Sound("Voicy_Rock You.mp3")
gameover_sound = pygame.mixer.Sound("Voicy_Attempting To Show Obedience.mp3")

# Snake image // change however you want
snake_head_img = pygame.image.load("snake_head.jpg") # Ikuyo Kita head
snake_head_img = pygame.transform.scale(snake_head_img, (TILE_SIZE, TILE_SIZE))

# Fonts // change font however you want
font = pygame.font.SysFont("Times New Roman", 25)
big_font = pygame.font.SysFont("Times New Roman", 60)

clock = pygame.time.Clock()

# High Score // sets your personal highscore through a save json file
high_score_file = "SnakeHighscore.json" # automatically creates it // my personal best Score: 24
if not os.path.exists(high_score_file):
    with open(high_score_file, "w") as f:
        f.write("0")
with open(high_score_file, "r") as f:
    personal_best = int(f.read())

def randomize_skin(): # randomize your skin whenever you play
    return random.choice(snake_skins)

def checkered_background(): # checkered background similar to google snake // I just copied the color in the game MiSide (there's a snake game also there)
    for y in range(ROWS):
        for x in range(COLS):
            rect = (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            color = BG_COLOUR_1 if (x+y)%2 == 0 else BG_COLOUR_2
            pygame.draw.rect(screen, color, rect)

def snake_body(snake, direction, color): # the snake itself
    for i, block in enumerate(snake):
        x, y = block
        if i == 0:
            # rotate the snake head based on the direction
            head_rotated = pygame.transform.rotate(snake_head_img, { # helps the head to stay in the snake
                "UP": 0, "DOWN": 180, "LEFT": 90, "RIGHT": -90
            }[direction])
            screen.blit(head_rotated, (x * TILE_SIZE, y * TILE_SIZE))
        else:
            pygame.draw.rect(screen, color, (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))

# helps with clipping // if the snake goes out the screen it comes back at the opposite direction
def wrapping(x, y):
    return x % COLS, y % ROWS

# text on the screen
def screen_text(text, font, color, x, y, center=False):
    surface = font.render(text, True, color)
    if center:
        rect = surface.get_rect(center=(x, y))
        screen.blit(surface, rect)
    else:
        screen.blit(surface, (x, y))

def show_menu(): # start menu // waits for the player to press "ENTER"
    # Waits for the player to press Enter
    in_menu = True
    while in_menu:
        screen.fill(BOCCHI_PINK)
        screen_text("SNAKE GAME", big_font, BLACK, WIDTH//2, HEIGHT//3, center=True)
        screen_text("Press ENTER to Play", font, BLACK, WIDTH//2, HEIGHT//2, center=True)
        screen_text("Inspired by Bro Code", font, DARK_GREEN, WIDTH//2, HEIGHT//2.5, center=True)
        screen_text("WASD Controls", font, RED, WIDTH//2, HEIGHT//2 + 40, center=True)
        screen_text("Made by _Bunccep", font, MY_PFP_COLOUR, WIDTH//2, HEIGHT//2 + 70, center=True)
        screen_text("---->", big_font, BOCCHI_YELLOW, WIDTH//2, HEIGHT//2 + 120, center=True)
        screen_text("<----", big_font, BOCCHI_BLUE, WIDTH//2, HEIGHT//2 + 160, center=True)
        pygame.display.update()
        gameover_sound.stop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                in_menu = False

def game_over_screen(score, personal_best): # game over when hits collision of yourself
    gameover_sound.play()
    eat_sound.stop()
    pygame.mixer.music.stop()
    screen.fill(BG_COLOUR_2)
    screen_text("Game Over!(-_-)", big_font, RED, WIDTH//2, HEIGHT//3, center=True)
    screen_text(f"Score: {score}", font, BOCCHI_YELLOW, WIDTH//2, HEIGHT//2, center=True)
    screen_text(f"Best: {personal_best}", font, BOCCHI_BLUE, WIDTH//2, HEIGHT//2 + 30, center=True)
    # Waits for R (restart) or ESC (exit)
    screen_text("Press R or ESC", font, DARK_GREEN, WIDTH//2, HEIGHT//2 + 70, center=True)
    screen_text("Inspired by Bocchi The Rock", font, BOCCHI_PINK, WIDTH//2, HEIGHT//2 + 100, center=True)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True # Restart THE GAME
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

def main(): # Main game loop: handles gameplay, movement, collisions, scoring, drawing, etc.
    global personal_best

    while True:  # Waits at the menu
        show_menu()
        pygame.mixer.music.play(-1)
        # Initialize snake, food, and variables
        snake = [(10, 10)]
        direction = "RIGHT"
        food = (random.randint(0, COLS-1), random.randint(0, ROWS-1))
        score = 0
        skin_color = randomize_skin()

        running = True
        while running:
            clock.tick(10) # the FPS
            checkered_background()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            # Input handling (WASD)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and direction != "DOWN":
                direction = "UP"
            elif keys[pygame.K_s] and direction != "UP":
                direction = "DOWN"
            elif keys[pygame.K_a] and direction != "RIGHT":
                direction = "LEFT"
            elif keys[pygame.K_d] and direction != "LEFT":
                direction = "RIGHT"
            # Move snake
            head_x, head_y = snake[0]
            if direction == "UP":
                head_y -= 1
            elif direction == "DOWN":
                head_y += 1
            elif direction == "LEFT":
                head_x -= 1
            elif direction == "RIGHT":
                head_x += 1
            # Check collision with self
            head_x, head_y = wrapping(head_x, head_y)
            new_head = (head_x, head_y)

            if new_head in snake:
                if score > personal_best:
                    personal_best = score
                    with open(high_score_file, "w") as f:
                        f.write(str(score))
                if game_over_screen(score, personal_best):
                    break

            snake.insert(0, new_head)
            # Check food eaten
            if new_head == food:
                eat_sound.play()
                score += 1
                food = (random.randint(0, COLS-1), random.randint(0, ROWS-1))
            else:
                snake.pop()

            snake_body(snake, direction, skin_color)
            pygame.draw.rect(screen, RED, (food[0]*TILE_SIZE, food[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))

            screen_text(f"Score: {score}", font, BLACK, 10, 10)
            screen_text(f"Best: {personal_best}", font, BLACK, 10, 40)

            pygame.display.update()

main()
