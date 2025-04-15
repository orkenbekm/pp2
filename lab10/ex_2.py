import pygame
import random
import psycopg2
from datetime import datetime

conn = psycopg2.connect(
    dbname="snake", user="postgres", password="123321", host="localhost", port="5432"
)
cur = conn.cursor()
cur.execute(
    """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE
);
"""
)
cur.execute(
    """
CREATE TABLE IF NOT EXISTS user_score (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    score INTEGER,
    level INTEGER,
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
)
conn.commit()
username = input("Enter your username: ")
cur.execute("SELECT id FROM users WHERE username = %s", (username,))
user = cur.fetchone()
if user:
    user_id = user[0]
    print("Welcome back,", username)
else:
    cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
    user_id = cur.fetchone()[0]
    conn.commit()
    print("New user created.")

cur.execute(
    "SELECT level FROM user_score WHERE user_id = %s ORDER BY id DESC LIMIT 1",
    (user_id,),
)
row = cur.fetchone()
level = row[0] if row else 1
print(f"Current level: {level}")
pygame.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
snake = [(100, 100)]
dx, dy = CELL_SIZE, 0
apple = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
score = 0


def draw():
    screen.fill((0, 0, 0))
    for x, y in snake:
        pygame.draw.rect(screen, (0, 255, 0), (x, y, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, (255, 0, 0), (*apple, CELL_SIZE, CELL_SIZE))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    pygame.display.flip()


def save_to_db():
    cur.execute(
        "INSERT INTO user_score (user_id, score, level) VALUES (%s, %s, %s)",
        (user_id, score, level),
    )
    conn.commit()
    print("Game paused and score saved!")


running = True
paused = False
speed = 10 + (level - 1) * 2

while running:
    clock.tick(speed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and dx == 0:
                dx, dy = -CELL_SIZE, 0
            elif event.key == pygame.K_RIGHT and dx == 0:
                dx, dy = CELL_SIZE, 0
            elif event.key == pygame.K_UP and dy == 0:
                dx, dy = 0, -CELL_SIZE
            elif event.key == pygame.K_DOWN and dy == 0:
                dx, dy = 0, CELL_SIZE
            elif event.key == pygame.K_p:
                paused = True
                save_to_db()

    if paused:
        continue
    head = (snake[0][0] + dx, snake[0][1] + dy)
    snake.insert(0, head)

    if head == apple:
        score += 10
        apple = (
            random.randrange(0, WIDTH, CELL_SIZE),
            random.randrange(0, HEIGHT, CELL_SIZE),
        )
    else:
        snake.pop()

    if (
        head in snake[1:]
        or head[0] < 0
        or head[0] >= WIDTH
        or head[1] < 0
        or head[1] >= HEIGHT
    ):
        save_to_db()
        running = False
    draw()
pygame.quit()
cur.close()
conn.close()
