import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Justice Defence!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 3, 0, 6, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

DEMON_LAUGH = pygame.mixer.Sound('Assets/devil_laugh.mp3')
DEMON_DYING = pygame.mixer.Sound('Assets/demon-slaughter.mp3')
DEMON_FIRE = pygame.mixer.Sound('Assets/DEMON_FIRE.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 32)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3


COWBOY_HIT = pygame.USEREVENT + 1
DEMON_HIT = pygame.USEREVENT + 2

COWBOY_IMAGE = pygame.image.load(os.path.join('Assets', 'cowboy.png'))
COWBOY = pygame.transform.scale(COWBOY_IMAGE, (40, 80))

DEMON_IMAGE = pygame.image.load(os.path.join('Assets', 'demon.png'))
DEMON = pygame.transform.scale(DEMON_IMAGE, (110,150))

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets\Tilesets', 'Tileset8.jpg')), (WIDTH, HEIGHT))


def draw_window(demon, cowboy, demon_bullets, cowboy_bullets, demon_health, cowboy_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    demon_health_text = HEALTH_FONT.render("Health: " + str(demon_health), 1, WHITE)
    cowboy_health_text = HEALTH_FONT.render("Health: " + str(cowboy_health), 1, WHITE)
    WIN.blit(demon_health_text, (WIDTH - demon_health_text.get_width() - 10, 10))
    WIN.blit(cowboy_health_text, (10, 10))

    WIN.blit(COWBOY, (cowboy.x, cowboy.y))
    WIN.blit(DEMON, (demon.x, demon.y))

    for bullet in demon_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in cowboy_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def handle_cowboy_movement(keys_pressed, cowboy):
    if keys_pressed[pygame.K_a] and cowboy.x - VEL > 0:  # LEFT
        cowboy.x -= VEL
    if keys_pressed[pygame.K_d] and cowboy.x + VEL + cowboy.width - 30 < BORDER.x:  # RIGHT
        cowboy.x += VEL
    if keys_pressed[pygame.K_w] and cowboy.y - VEL > 0:  # UP
        cowboy.y -= VEL
    if keys_pressed[pygame.K_s] and cowboy.y + VEL + cowboy.height -30 < HEIGHT :  # DOWN
        cowboy.y += VEL


def handle_demon_movement(keys_pressed, demon):
    if keys_pressed[pygame.K_LEFT] and demon.x - VEL > BORDER.x + BORDER.width:  # LEFT
        demon.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and demon.x + VEL + demon.width + 30 < WIDTH:  # RIGHT
        demon.x += VEL
    if keys_pressed[pygame.K_UP] and demon.y - VEL > 0:  # UP
        demon.y -= VEL
    if keys_pressed[pygame.K_DOWN] and demon.y + VEL + demon.height + 30 < HEIGHT:  # DOWN
        demon.y += VEL


def handle_bullets(cowboy_bullets, demon_bullets, cowboy, demon):
    for bullet in cowboy_bullets:
        bullet.x += BULLET_VEL
        if demon.colliderect(bullet):
            pygame.event.post(pygame.event.Event(DEMON_HIT))
            cowboy_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            cowboy_bullets.remove(bullet)

    for bullet in demon_bullets:
        bullet.x -= BULLET_VEL
        if cowboy.colliderect(bullet):
            pygame.event.post(pygame.event.Event(COWBOY_HIT))
            demon_bullets.remove(bullet)
        elif bullet.x < 0:
            demon_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    cowboy = pygame.Rect(100, 300, 40, 80)
    demon = pygame.Rect(700, 300, 110, 150)

    demon_bullets = []
    cowboy_bullets = []

    demon_health = 10
    cowboy_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(cowboy_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(cowboy.x + cowboy.width, cowboy.y + cowboy.height//2 - 2, 10, 5)
                    cowboy_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(demon_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(demon.x, demon.y + demon.height//2 - 4, 20, 10)
                    demon_bullets.append(bullet)
                    DEMON_FIRE.play()

            if event.type == DEMON_HIT:
                demon_health -= 1
                DEMON_DYING.play()

            if event.type == COWBOY_HIT:
                cowboy_health -= 1
                DEMON_LAUGH.play()

        winner_text = ""
        if demon_health <= 0:
            winner_text = "Cowboy Wins!"

        if cowboy_health <= 0:
            winner_text = "Demon Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        handle_cowboy_movement(keys_pressed, cowboy)
        handle_demon_movement(keys_pressed, demon)

        handle_bullets(cowboy_bullets, demon_bullets, cowboy, demon)

        draw_window(demon, cowboy, demon_bullets, cowboy_bullets,demon_health, cowboy_health)

    main()


if __name__ == "__main__":
    main()