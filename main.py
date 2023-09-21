import pygame
import sys

pygame.init()

width = 420  # Ширина экрана
height = 420  # Высота экрна
FPS = 60  # Число кадров в секунду

sc = pygame.display.set_mode((width, height))  # Создаем экран
clock = pygame.time.Clock()  # Создаем часы для FPS

square = pygame.Rect(width / 1.075, height / 1.075, 30, 30)
second_square = pygame.Rect(width / 1000, height / 1000, 30, 30)

while True:
    events = pygame.event.get()  # Получаем события в прямом эфире

    for event in events:  # Цикл для обработки событий
        if event.type == pygame.QUIT:  # Сравниваем тип события с выходом из игры, окна
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                square.y -= 30
            if event.key == pygame.K_s:
                square.y += 30
            if event.key == pygame.K_d:
                square.x += 30
            if event.key == pygame.K_a:
                square.x -= 30
            if event.key == pygame.K_q:
                square.x -= 30
                square.y -= 30
            if event.key == pygame.K_e:
                square.x += 30
                square.y -= 30
            if event.key == pygame.K_c:
                square.x += 30
                square.y += 30
            if event.key == pygame.K_z:
                square.x -= 30
                square.y += 30

    for event in events:  # Цикл для обработки событий
        if event.type == pygame.QUIT:  # Сравниваем тип события с выходом из игры, окна
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:
                second_square.y -= 30
            if event.key == pygame.K_j:
                second_square.y += 30
            if event.key == pygame.K_k:
                second_square.x += 30
            if event.key == pygame.K_h:
                second_square.x -= 30
            if event.key == pygame.K_y:
                second_square.x -= 30
                second_square.y -= 30
            if event.key == pygame.K_i:
                second_square.x += 30
                second_square.y -= 30
            if event.key == pygame.K_m:
                second_square.x += 30
                second_square.y += 30
            if event.key == pygame.K_b:
                second_square.x -= 30
                second_square.y += 30

    sc.fill((0, 0, 0))
    pygame.draw.rect(sc, (255, 0, 0), second_square)
    pygame.draw.rect(sc, (0, 128, 0), square)

    clock.tick(FPS)  # Запускаем часы с FPS кадров в секунду

    pygame.display.update()  # Обновляем экран
