import pygame
from datetime import datetime

pygame.init()

screen = pygame.display.set_mode([1000, 750])

right_arm = pygame.image.load(
    r"C:\Users\Aikorkem\Desktop\STUDY\pp2\labs\lab7\img\mickey_right_arm.png"
)
left_arm = pygame.image.load(
    r"C:\Users\Aikorkem\Desktop\STUDY\pp2\labs\lab7\img\mickey_left_arm.png"
)
without_arm = pygame.image.load(
    r"C:\Users\Aikorkem\Desktop\STUDY\pp2\labs\lab7\img\mickey_without_arms.png"
)
pygame.mixer.init()
mus = pygame.mixer.music.load(
    r"C:\Users\Aikorkem\Desktop\STUDY\pp2\labs\lab7\пайгей музыка\Kendrick Lamar feat. SZA - All The Stars.mp3"
)


right_arm = pygame.transform.smoothscale(right_arm, (1000, 750))
left_arm = pygame.transform.smoothscale(left_arm, (1000, 750))
without_arm = pygame.transform.smoothscale(without_arm, (1000, 750))

running = True
while running:

    now = datetime.now()
    angle = -now.second * 6
    angle2 = -now.minute * 6

    rotated_right = pygame.transform.rotate(right_arm, angle)
    rotated_left = pygame.transform.rotate(left_arm, angle2)

    right_rect = rotated_right.get_rect(center=(500, 375))
    left_rect = rotated_left.get_rect(center=(500, 375))

    screen.blit(without_arm, (0, 0))
    screen.blit(rotated_right, right_rect.topleft)
    screen.blit(rotated_left, left_rect.topleft)

    if angle == 0:
        mus.play()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()
