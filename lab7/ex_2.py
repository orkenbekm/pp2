import pygame

pygame.init()

screen = pygame.display.set_mode([500, 500])
current_track = 1
paused = False
trek1 = r"C:\Users\Aikorkem\Desktop\STUDY\pp2\labs\lab7\пайгей музыка\Kendrick Lamar feat. SZA - All The Stars.mp3"

trek2 = r"C:\Users\Aikorkem\Desktop\STUDY\pp2\labs\lab7\пайгей музыка\14adadca9148f2d77303bbe3c4107435.mp3"


def play_music():
    global paused
    if current_track == 1:
        pygame.mixer.music.load(trek1)
    else:
        pygame.mixer.music.load(trek2)
    pygame.mixer.music.play()
    paused = False


play_music()


go = pygame.image.load(
    r"C:\Users\Aikorkem\Desktop\STUDY\pp2\labs\lab7\пайгей музыка\возпроизвести.png"
)
stop = pygame.image.load(
    r"C:\Users\Aikorkem\Desktop\STUDY\pp2\labs\lab7\пайгей музыка\стоп.png"
)
next = pygame.image.load(
    r"C:\Users\Aikorkem\Desktop\STUDY\pp2\labs\lab7\пайгей музыка\следующая музыка.png"
)
previous = pygame.image.load(
    r"C:\Users\Aikorkem\Desktop\STUDY\pp2\labs\lab7\пайгей музыка\предыдущая музыка.png"
)

go = pygame.transform.smoothscale(go, (100, 100))
next = pygame.transform.smoothscale(next, (100, 100))
stop = pygame.transform.smoothscale(stop, (100, 100))
previous = pygame.transform.smoothscale(previous, (100, 100))
screen.fill([255, 255, 255])
running = True
while running:
    screen.blit(go, (50, 350))
    screen.blit(next, (350, 350))
    screen.blit(stop, (200, 350))
    screen.blit(previous, (50, 200))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if paused:
                    pygame.mixer.music.unpause()

            elif event.key == pygame.K_s:
                pygame.mixer.music.pause()
                paused = True
            elif event.key == pygame.K_RIGHT:
                current_track = 2
                play_music()

            elif event.key == pygame.K_LEFT:
                current_track = 1
                play_music()
