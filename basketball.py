# Import necessary libraries
import pygame
import time
import random

# Initialize Pygame and the mixer for music
pygame.init()
pygame.mixer.init()

# Load and play the background music
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.set_volume(0.5)  # Adjust the volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # The '-1' means the music will loop indefinitely

# Initialize Pygame fonts
pygame.font.init()

# Set up window dimensions
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

# Function to load an image and scale it to the window size
def load_and_scale_image(image_path):
    return pygame.transform.scale(pygame.image.load(image_path), (WIDTH, HEIGHT))

# Load background images
BG = load_and_scale_image("bg.jpeg")
MENU_BG = load_and_scale_image("menu_background.jpg")

# Player parameters
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 40
PLAYER_VEL = 5

# Star parameters
STAR_WIDTH = 14
STAR_HEIGHT = 30
STAR_VEL = 3

# Set up fonts
FONT = pygame.font.SysFont("comicsans", 30)
START_FONT = pygame.font.SysFont("comicsans", 40)

# Load player and star images
PLAYER_IMAGE = pygame.transform.scale(pygame.image.load("space.webp"), (PLAYER_WIDTH, PLAYER_HEIGHT))
STAR_IMAGE = pygame.transform.scale(pygame.image.load("star.webp"), (STAR_WIDTH, STAR_HEIGHT))

# Define the Player class
class Player:
    def __init__(self, x, y, width, height, velocity, image):
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity = velocity
        self.image = pygame.transform.scale(pygame.image.load(image), (width, height))

    def move(self, direction):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x - self.velocity >= 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.x + self.velocity + self.rect.width <= WIDTH:
            self.rect.x += self.velocity

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Define the Star class
class Star:
    def __init__(self, x, y, width, height, velocity, image):
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity = velocity
        self.image = pygame.transform.scale(pygame.image.load(image), (width, height))

    def fall(self):
        self.rect.y += self.velocity

    def is_out_of_screen(self):
        return self.rect.y > HEIGHT

    def collide_with_player(self, player):
        return self.rect.colliderect(player.rect)

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Function to draw text on the window
def draw_text(window, elapsed_time, score, paused, message="", display_time=0):
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    score_text = FONT.render(f"Score: {score}", 1, "white")
    
    window.blit(time_text, (10, 10))
    window.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))

    if paused:
        pause_text = FONT.render("PAUSED", 1, "white")
        window.blit(pause_text, (WIDTH/2 - pause_text.get_width()/2, HEIGHT/2 - pause_text.get_height()/2))

    if message:
        message_text = FONT.render(message, 1, "red")
        window.blit(message_text, (WIDTH/2 - message_text.get_width()/2, HEIGHT - 50))
        if display_time > 0:
            display_time -= 1
        else:
            message = ""  # Reset the message after the display time is over

    return message, display_time

# Function to draw the game over screen
def draw_game_over(window, elapsed_time, score):
    final_score = int(elapsed_time * score)  # Calculate the final score as time * score
    lost_text = FONT.render("You Lost! Score: {}".format(final_score), 1, "white")
    restart_text = FONT.render("Press R to restart", 1, "white")
    exit_text = FONT.render("Press ESC to exit", 1, "white")

    #position of text
    window.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
    window.blit(restart_text, (WIDTH/2 - restart_text.get_width()/2, HEIGHT/2 + 50))
    window.blit(exit_text, (WIDTH/2 - exit_text.get_width()/2, HEIGHT/2 + 80))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game
                    return True
                elif event.key == pygame.K_ESCAPE:  # Exit the game
                    pygame.quit()
                    exit()

# Function to draw the start menu
def draw_start_menu(window, background_img):
    window.blit(background_img, (0, 0))
    
    menu_text = START_FONT.render("Space Dodge", 1, "black")
    start_text = FONT.render("Press ENTER to start", 1, "black")
    instruction_text1 = FONT.render("Move left: Left Arrow Key", 1, "black")
    instruction_text2 = FONT.render("Move right: Right Arrow Key", 1, "black")
    pause_instruction = FONT.render("Pause: Space Bar", 1, "black")

    #position of the text
    window.blit(menu_text, (WIDTH/2 - menu_text.get_width()/2, HEIGHT/4 - menu_text.get_height()/2))
    window.blit(start_text, (WIDTH/2 - start_text.get_width()/2, HEIGHT/2))
    window.blit(instruction_text1, (WIDTH/2 - instruction_text1.get_width()/2, HEIGHT/2 + 50))
    window.blit(instruction_text2, (WIDTH/2 - instruction_text2.get_width()/2, HEIGHT/2 + 80))
    window.blit(pause_instruction, (WIDTH/2 - pause_instruction.get_width()/2, HEIGHT/2 + 110))

# Main game loop
def main():
    pygame.mixer.music.play(-1)  # Play the background music in a loop

    # Function to draw game elements
    def draw(player, elapsed_time, stars, score, paused, message="", display_time=0):
        WIN.blit(BG, (0, 0))

        for star in stars:
            star.draw(WIN)

        player.draw(WIN)
        
        message, display_time = draw_text(WIN, elapsed_time, score, paused, message, display_time)

        pygame.display.update()

        return message, display_time

    run = True
    in_start_menu = True

    # Create the player object
    player = Player(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_VEL, "space.webp")

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False

    score = 0
    paused = False

    error_message = ""
    error_display_time = 0

    # Main game loop
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if in_start_menu and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                in_start_menu = False

            if not in_start_menu and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key not in (pygame.K_LEFT, pygame.K_RIGHT):
                    error_message = "Use only Left and Right Arrow Keys!"
                    error_display_time = 180  # 3 seconds

        if in_start_menu:
            draw_start_menu(WIN, MENU_BG)
            pygame.display.update()
            continue  # Skip the rest of the game loop if in the start menu

        if paused:
            clock.tick(5)  # Reduce the frame rate when paused
            continue  # Skip the rest of the game loop if paused

        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                if len(stars) < 35:
                    star_x = random.randint(0, WIDTH - STAR_WIDTH)
                    star = Star(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT, STAR_VEL, "star.webp")
                    stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        player.move(PLAYER_VEL)

        for star in stars[:]:
            star.fall()
            if star.is_out_of_screen():
                stars.remove(star)
                score += 1
            elif star.collide_with_player(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            if not draw_game_over(WIN, elapsed_time, score):  # Check the return value
                run = False
                break
            else:
                # Reset the game state
                player.rect.x = 200
                player.rect.y = HEIGHT - PLAYER_HEIGHT
                stars.clear()
                hit = False
                score = 0
                start_time = time.time()

        error_message, error_display_time = draw(player, elapsed_time, stars, score, paused, error_message, error_display_time)

    # Stop the music when the program exits
    pygame.mixer.music.stop()
    pygame.quit()

# Run the game if this script is executed
if __name__ == "__main__":
    main()
