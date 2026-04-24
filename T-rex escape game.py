import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Escape")

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
BLUE = (135, 206, 235)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)

font = pygame.font.SysFont("Arial", 24)

jump_sound = pygame.mixer.Sound("jump.mp3")
coin_sound = pygame.mixer.Sound("coin.mp3")

gravity = 0.5
dino_x, dino_y = 50, 50
dino_vel_y = 0
is_jumping = False
speed = 5
money = 0
level = 1
jump = 10
goal_money = 500
is_paused = False
level_complete = False
current_level = 1
level_money_thresholds = {1: 500, 2: 1000, 3: 1500}
escape_cost = 2000

upgrades = {
    "Jump Height": {"cost": 200, "level": 1},
    "Gravity Reduction": {"cost": 300, "level": 1},
    "Speed Increase": {"cost": 400, "level": 1},
    "Extra Life": {"cost": 500, "level": 0}
}


dino = pygame.Surface((50, 50))
dino_rect = dino.get_rect(topleft=(dino_x, dino_y))
dino.fill(GREEN)

sky = pygame.Surface((WIDTH, HEIGHT))
sky.fill(BLUE)
ground = pygame.Surface((WIDTH, 20))
ground.fill(BROWN)


dino_surface = pygame.Surface((50, 50))
dino_surface.fill(GREEN)
dino_rect = dino_surface.get_rect(topleft=(dino_x, dino_y))

sky_surface = pygame.Surface((WIDTH, HEIGHT))
sky_surface.fill(BLUE)

ground_surface = pygame.Surface((WIDTH, 20))
ground_surface.fill(BROWN)
ground_rect = ground_surface.get_rect(topleft=(0, HEIGHT - 20))

coin_surface = pygame.Surface((30, 30))
coin_surface.fill(GOLD)

obstacle_surface = pygame.Surface((20, 50))
obstacle_surface.fill(RED)

cloud_surface = pygame.Surface((70, 50))
cloud_surface.fill(WHITE)

tree_surface = pygame.Surface((30, 80))
tree_surface.fill(GREEN)


obstacles = []
coins = []
clouds = []
trees = []

def create_obstacle():
    rect1 = obstacle_surface.get_rect(topleft=(WIDTH, HEIGHT - 70))
    return rect1

def create_coin():
    rect2 = coin_surface.get_rect(topleft=(WIDTH, random.randint(15, HEIGHT - 60)))
    return rect2

def create_cloud():
    rect3 = cloud_surface.get_rect(topleft=(WIDTH, random.randint(20, 100)))
    return rect3

def create_tree():
    rect4 = tree_surface.get_rect(topleft=(WIDTH, HEIGHT - 100))
    return rect4

def draw_text(text, x, y):
    label = font.render(text, True, BLACK)
    screen.blit(label, (x, y))

def draw_dino():
    screen.blit(dino_surface, dino_rect)

def draw_objects(surface, objects):
    for obj in objects:
        screen.blit(surface, obj)

def draw_upgrade_menu():
    screen.fill(WHITE)
    draw_text("UPGRADE MENU", WIDTH // 2 - 80, 30)
    y_offset = 80
    for idx, (upgrade, info) in enumerate(upgrades.items()):
        text = f"{idx + 1}. {upgrade} (Level {info['level']}, Cost: ${info['cost']})"
        draw_text(text, 100, y_offset)
        y_offset += 40
    draw_text("Press number to purchase, 'R' to resume", 100, y_offset)

def purchase_upgrade(upgrade_key):
    global gravity, speed, extra_lives, jump
    upgrade = upgrades[upgrade_key]
    if money >= upgrade["cost"]:
        if upgrade_key == "Jump Height":
            jump += 1
            upgrade["level"] += 1
        elif upgrade_key == "Gravity Reduction":
            gravity = max(0.1, gravity - 0.1)
            upgrade["level"] += 1
        elif upgrade_key == "Speed Increase":
            speed += 1
            upgrade["level"] += 1
        elif upgrade_key == "Extra Life":
            extra_lives += 1
            upgrade["level"] += 1
        return True
    return False

def check_level_progress():
    global level, money, speed, level_complete

    if level < 3 and money >= level_money_thresholds[level]:
        level_complete = True
    elif level == 3 and money >= escape_cost:
        print("You have enough money to escape! Press 'E' to escape.")
        level_complete = True

def collision(dino_rect, obstacles):
    for obstacle in obstacles:
        if dino_rect.colliderect(obstacle):
            return True
    return False

# Main game loop
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1500)

while True:
    screen.blit(sky, (0, 0))
    screen.blit(ground, (0, HEIGHT - 20))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.USEREVENT:
            obstacles.append(create_obstacle())
            coins.append(create_coin())
            clouds.append(create_cloud())
            trees.append(create_tree())
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping and not is_paused:
                dino_vel_y = -jump
                jump_sound.play()
                is_jumping = True
            if event.key == pygame.K_u:
                is_paused = not is_paused
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            if level_complete:
                if level < 3 and event.key == pygame.K_n:
                    level += 1
                    speed += 2
                    money = 0
                    level_complete = False
                    print(f"Level up! You are now on level {level}.")
                elif level == 3 and event.key == pygame.K_e and money >= escape_cost:
                    print("Congratulations! You've escaped the island!")
                    pygame.quit()
                    sys.exit()
            if is_paused:
                if event.key == pygame.K_1:
                    purchase_upgrade("Jump Height")
                elif event.key == pygame.K_2:
                    purchase_upgrade("Gravity Reduction")
                elif event.key == pygame.K_3:
                    purchase_upgrade("Speed Increase")
                elif event.key == pygame.K_4:
                    purchase_upgrade("Extra Life")
                elif event.key == pygame.K_r:
                    is_paused = False

    if is_paused:
        draw_upgrade_menu()
        pygame.display.update()
        continue

    if collision(dino_rect, obstacles):
        print("Game Over! You hit an obstacle!")
        pygame.quit()
        sys.exit()

    dino_vel_y += gravity
    dino_rect.y += dino_vel_y
    if dino_rect.bottom >= HEIGHT - 20:
        dino_rect.bottom = HEIGHT - 20
        is_jumping = False

    for obstacle in obstacles:
        obstacle.x -= speed
    for coin in coins:
        coin.x -= speed
    for cloud in clouds:
        cloud.x-= speed // 2
    for tree in trees:
        tree.x -= speed / 2


    for coin in coins:
        coin_rect = pygame.Rect(coin.x, coin.y, 20, 20)
        if dino_rect.colliderect(coin_rect):
            money += 100
            coin_sound.play()
            coins.remove(coin)

    if level_complete:
        if level < 3:
            draw_text("Press 'N' to proceed to the next level", WIDTH // 2 - 150, HEIGHT // 2)
        elif level == 3:
            draw_text("Press 'E' to escape the island", WIDTH // 2 - 150, HEIGHT // 2)

    draw_dino()
    draw_objects(obstacle_surface, obstacles)
    draw_objects(coin_surface, coins)
    draw_objects(cloud_surface, clouds)
    draw_objects(tree_surface, trees)
    draw_text(f"Money: ${money}", 10, 10)
    draw_text(f"Level: {level}", 10, 40)

    check_level_progress()

    pygame.display.update()
    clock.tick(60)
