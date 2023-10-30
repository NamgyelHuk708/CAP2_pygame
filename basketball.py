import pygame
import time
import random

# Initializing
pygame.font.init()

# Screen display
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Name of the game in the caption
pygame.display.set_caption("Space Dodge")

# Background plus scaling the image to match the screen
BG = pygame.transform.scale(pygame.image.load("bg.jpeg"), (WIDTH, HEIGHT))

# Player size
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 40

# Player velocity and star size
PLAYER_VEL = 5
STAR_WIDTH = 14
STAR_HEIGHT = 30  # Adjust the size based on your star image dimensions

# Star velocity
STAR_VEL = 3

# Fonts for any text
FONT = pygame.font.SysFont("comicsans", 30)

# Load player image
PLAYER_IMAGE = pygame.transform.scale(pygame.image.load("space.webp"), (PLAYER_WIDTH, PLAYER_HEIGHT))

# Load star image
STAR_IMAGE = pygame.transform.scale(pygame.image.load("star.webp"), (STAR_WIDTH, STAR_HEIGHT))

# Drawing background image to the screen
def draw(player, elapsed_time, stars, score):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    score_text = FONT.render(f"Score: {score}", 1, "white")
    
    WIN.blit(time_text, (10, 10))
    WIN.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))

    WIN.blit(PLAYER_IMAGE, (player.x, player.y))

    for star in stars:
        WIN.blit(STAR_IMAGE, (star.x, star.y))

    pygame.display.update()

# Main game logic
def main():
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    player.width = PLAYER_IMAGE.get_width()
    player.height = PLAYER_IMAGE.get_height()

    # Clock object
    clock = pygame.time.Clock()
    # Time record
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False

    score = 0  # Initialize the score

    while run:
        star_count += clock.tick(60)   # Running 60/s
        elapsed_time = time.time() - start_time # Starting the time count

        if star_count > star_add_increment:
            for _ in range(3):
                if len(stars) < 30:  # Check if the number of stars is less than 20
                    star_x = random.randint(0, WIDTH - STAR_WIDTH)
                    star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                    stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        # Exiting the game by pressing the exit x
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # Key codes for movement plus preventing it from exiting the screen
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
                # Increment the score when a star is successfully dodged
                score += 1
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            lost_text = FONT.render("You Lost! Score: {}".format(score), 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, elapsed_time, stars, score)

    pygame.quit()

if __name__ == "__main__":
    main()
