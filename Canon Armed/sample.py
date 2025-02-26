import pygame
import random
import time

# Initialize Pygame
pygame.init()


# Function to get the game dimensions based on screen width
def get_game_dimensions():
    info = pygame.display.Info()
    screen_width = info.current_w
    
    if screen_width <= 480:
        # Small Phones
        return (320, 568)
    elif screen_width <= 640:
        # Medium Phones
        return (480, 854)
    elif screen_width <= 768:
        # Large Phones
        return (640, 1136)
    elif screen_width <= 1024:
        # Small Tablets
        return (768, 1024)
    # else:
    #     # Defaults to a larger device or desktop size
    #     return (800, 600)  # Default size if none of the conditions above are met
    return (400, 600)


# Get dynamic dimensions
WIDTH, HEIGHT = get_game_dimensions()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Canon Armed')

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BUTTON_COLOR = (0, 150, 0)
BUTTON_HOVER_COLOR = (0, 180, 0)
TEXT_COLOR = (255, 255, 255)

# Load images
background = pygame.image.load('Images/background.jpg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Load sounds
pygame.mixer.music.load('Images/background_sound.mp3')
hit_sound = pygame.mixer.Sound('Images/hit-sound.mp3')

# Load and scale images
background = pygame.image.load('Images/background.jpg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

vehicle_image = pygame.image.load('Images/canon.png')
# Vehicle setup with new dimensions
vehicle_width = 35
vehicle_height = 50
vehicle_image = pygame.transform.scale(vehicle_image, (vehicle_width, vehicle_height))
vehicle_x = WIDTH // 2 - vehicle_width // 2
vehicle_y = HEIGHT - vehicle_height - 5
vehicle_speed = 10

# Bullet setup
bullet_width = 5
bullet_height = 5
bullet_speed = 15
bullets = []
fire_bullets = False
last_bullet_time = 0
bullet_interval = 250  # milliseconds

# Obstacle setup
obstacle_width = 40
obstacle_height = 40
obstacle_speed = 5
obstacles = []

# Game variables
score = 0
font = pygame.font.SysFont('arial', 30)


# Create the vehicle
def draw_vehicle(x, y):
    screen.blit(vehicle_image, (x, y))


# Create bullets
def draw_bullets(bullets):
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)


def move_bullets(bullets):
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)


# Create obstacles
def draw_obstacles(obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, obstacle)


def create_obstacle():
    x = random.randint(0, WIDTH - obstacle_width)
    y = -obstacle_height
    return pygame.Rect(x, y, obstacle_width, obstacle_height)


# Check for collision
def check_collision(vehicle, obstacles):
    for obstacle in obstacles[:]:
        if vehicle.colliderect(obstacle):
            return True
    return False


def check_bullet_collision(bullets, obstacles):
    global score
    for bullet in bullets[:]:
        for obstacle in obstacles[:]:
            if bullet.colliderect(obstacle):
                bullets.remove(bullet)
                obstacles.remove(obstacle)
                score += 10
                hit_sound.play()
                break


# Display score
def show_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))


# Play Button Design
def draw_play_button():
    button_width = 200
    button_height = 100
    button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height // 2, button_width, button_height)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect, border_radius=20)
    pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect.inflate(-10, -10), border_radius=15)
    play_text = font.render("Play", True, TEXT_COLOR)
    screen.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, HEIGHT // 2 - play_text.get_height() // 2))
    return button_rect


# Game loop
running = True
game_started = False
score = 0
touch_move = False
previous_touch_x = 0
vehicle_x = WIDTH // 2 - vehicle_width // 2
move_left = False
move_right = False

while running:
    screen.fill(BLACK)  # Clear the screen
    current_time = pygame.time.get_ticks()

    if not game_started:
        play_button_rect = draw_play_button()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    game_started = True
                    pygame.mixer.music.play(-1)

    else:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_left = True
                elif event.key == pygame.K_RIGHT:
                    move_right = True
                elif event.key == pygame.K_SPACE:
                    fire_bullets = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    move_left = False
                elif event.key == pygame.K_RIGHT:
                    move_right = False
                elif event.key == pygame.K_SPACE:
                    fire_bullets = False

        # Continuous firing logic
        if fire_bullets and (current_time - last_bullet_time > bullet_interval):
            bullet = pygame.Rect(vehicle_x + vehicle_width // 2 - bullet_width // 2, vehicle_y, bullet_width, bullet_height)
            bullets.append(bullet)
            last_bullet_time = current_time

        if move_left and vehicle_x > 0:
            vehicle_x -= vehicle_speed
        if move_right and vehicle_x < WIDTH - vehicle_width:
            vehicle_x += vehicle_speed

        if random.random() < 0.02:
            obstacles.append(create_obstacle())

        for obstacle in obstacles[:]:
            obstacle.y += obstacle_speed
            if obstacle.y > HEIGHT:
                obstacles.remove(obstacle)

        move_bullets(bullets)
        draw_bullets(bullets)
        vehicle_rect = pygame.Rect(vehicle_x, vehicle_y, vehicle_width, vehicle_height)
        draw_vehicle(vehicle_x, vehicle_y)
        draw_obstacles(obstacles)
        check_bullet_collision(bullets, obstacles)

        if check_collision(vehicle_rect, obstacles):
            game_started = False
            screen.fill(BLACK)
            final_score = font.render(f"Game Over! Final Score: {score}", True, WHITE)
            screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, HEIGHT // 2 - 100))
            pygame.mixer.music.stop()
            pygame.display.update()
            time.sleep(3)
            running = False

        show_score()

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
