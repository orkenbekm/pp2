import pygame
import random
import time
import sys
from pygame.locals import *

pygame.init()
pygame.mixer.init()

# Настройки экрана
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")

# Частота кадров
FPS = 60
clock = pygame.time.Clock()

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Шрифты
font = pygame.font.SysFont("Verdana", 20)
font_large = pygame.font.SysFont("Verdana", 40)

# Загрузка изображений
background = pygame.image.load(
    r"C:\Users\Aikorkem\Desktop\STUDY\pp2\labs\lab8\img\Road.png"
).convert()
background = pygame.transform.scale(
    background, (SCREEN_WIDTH, SCREEN_HEIGHT * 2)
)  # Удлиняем дорогу
player_img = pygame.image.load(
    r"C:\Users\Aikorkem\Desktop\STUDY\pp2\labs\lab8\img\Player.png"
).convert_alpha()
enemy_img = pygame.image.load(
    r"C:\Users\Aikorkem\Desktop\STUDY\pp2\labs\lab8\img\Enemy.png"
).convert_alpha()
coin_img = pygame.image.load(
    r"C:\Users\Aikorkem\Desktop\STUDY\pp2\labs\lab8\img\coin.png"
).convert_alpha()
coin_img = pygame.transform.scale(coin_img, (40, 40))

# Звук
crash_sound = pygame.mixer.Sound(
    r"C:\Users\Aikorkem\Desktop\STUDY\pp2\labs\lab8\img\Lab8_pictures_crash.wav"
)

# Параметры игры
SPEED = 5
SCORE = 0
COINS = 0
road_y = 0  # Позиция дороги


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.reset_position()
        self.speed = SPEED  # Добавляем скорость врагу

    def reset_position(self):
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -100)

    def move(self):
        self.rect.y += self.speed  # Используем собственную скорость
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()
            self.speed = SPEED * random.uniform(0.9, 1.1)  # Случайная скорость


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -300)

    def move(self):
        self.rect.y += SPEED * 5
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.speed = 5
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if pressed_keys[K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if pressed_keys[K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed


# Создание объектов
player = Player()
enemy = Enemy()
coin = Coin()

# Основной цикл
while True:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Обновление позиции дороги
    road_y += SPEED
    if road_y >= SCREEN_HEIGHT:
        road_y = 0

    # Обновление объектов
    player.move()
    enemy.move()
    coin.move()

    # Увеличение счета
    SCORE += 0.1

    # Проверка столкновений с монеткой
    if pygame.sprite.collide_mask(player, coin):
        COINS += 1
        coin.reset_position()

    # Проверка столкновений с врагом
    if pygame.sprite.collide_mask(player, enemy):
        crash_sound.play()  # Звук столкновения
        time.sleep(0.5)

        # Game Over экран
        SCREEN.fill(RED)
        game_over_text = font_large.render("GAME OVER", True, BLACK)
        score_text = font.render(f"Final Score: {int(SCORE)}", True, BLACK)
        coins_text = font.render(f"Coins: {COINS}", True, BLACK)

        SCREEN.blit(
            game_over_text,
            (
                SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                SCREEN_HEIGHT // 2 - 60,
            ),
        )
        SCREEN.blit(
            score_text,
            (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2),
        )
        SCREEN.blit(
            coins_text,
            (SCREEN_WIDTH // 2 - coins_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40),
        )

        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    # Отрисовка дороги
    SCREEN.blit(background, (0, road_y - SCREEN_HEIGHT))
    SCREEN.blit(background, (0, road_y))

    # Отрисовка остальных объектов
    SCREEN.blit(enemy.image, enemy.rect)
    SCREEN.blit(coin.image, coin.rect)
    SCREEN.blit(player.image, player.rect)

    # Отображение счетчиков
    score_display = font.render(f"Score: {int(SCORE)}", True, BLACK)
    coins_display = font.render(f"Coins: {COINS}", True, YELLOW)

    SCREEN.blit(score_display, (10, 10))
    SCREEN.blit(coins_display, (10, 40))

    pygame.display.update()
    clock.tick(FPS)
