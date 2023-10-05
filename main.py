import random
import pygame
import sys

pygame.init()

field_size = 14
cell_size = 30
width = height = field_size * cell_size  # Ширина, высота экрана
FPS = 60  # Число кадров в секунду

sc = pygame.display.set_mode((width, height))  # Создаем экран
clock = pygame.time.Clock()  # Создаем часы для FPS
square = pygame.Rect(0, 0, cell_size, cell_size)

game_field = [['0']*field_size for i in range(field_size)]  # игровое поле
players = [[0, 0], [field_size - 1, field_size - 1]]  # координаты игроков на поле

game_field[players[0][0]][players[0][1]] = "player1"  # расположить игрока_1 на поле
game_field[players[1][0]][players[1][1]] = "player2"  # расположить игрока_2 на поле
walls = []  # список стен
player_controls = {"up": [pygame.K_w, pygame.K_u], "down": [pygame.K_s, pygame.K_j],
                   "right": [pygame.K_d, pygame.K_k], "left": [pygame.K_a, pygame.K_h],
                   "up_left": [pygame.K_q, pygame.K_y], "up_right": [pygame.K_e,  pygame.K_i],
                   "down_right": [pygame.K_c, pygame.K_m], "down_left": [pygame.K_z, pygame.K_b]}

for i in range(1, field_size - 1):  # случайная расстановка стен для теста
    rnd = random.randrange(field_size)
    walls.append([i, rnd])
    game_field[i][rnd] = "wall"


def game_field_update(p_name, x, y):  # обновление данных игрового поля
    p_num = 0 if p_name == "player1" else 1
    x, y = players[p_num][0]+x, players[p_num][1]+y  # вычисление новых координат игрока
    if not is_move_correct(x, y):
        print('denied')
        return
    game_field[players[p_num][0]][players[p_num][1]] = '0'
    players[p_num] = [x, y]
    game_field[x][y] = p_name


def is_move_correct(x, y):  # проверка корректности хода
    if x < 0 or x >= field_size or y < 0 or y >= field_size:  # выход игрока за границы поля
        return False
    if game_field[x][y] in ("wall", "player2", "player1"):  # столкновение игрока с запрещённым объектом
        return False
    return True


while True:
    events = pygame.event.get()  # Получаем события в прямом эфире
    for event in events:  # Цикл для обработки событий
        if event.type == pygame.QUIT:  # Сравниваем тип события с выходом из игры, окна
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            player_name = "player1" if event.key in [i[0] for i in player_controls.values()] else "player2"
            if event.key in player_controls["up"]:
                game_field_update(player_name, 0, -1)
            if event.key in player_controls["down"]:
                game_field_update(player_name, 0, 1)
            if event.key in player_controls["right"]:
                game_field_update(player_name, 1, 0)
            if event.key in player_controls["left"]:
                game_field_update(player_name, -1, 0)
            if event.key in player_controls["up_left"]:
                game_field_update(player_name, -1, -1)
            if event.key in player_controls["up_right"]:
                game_field_update(player_name, 1, -1)
            if event.key in player_controls["down_right"]:
                game_field_update(player_name, 1, 1)
            if event.key in player_controls["down_left"]:
                game_field_update(player_name, -1, 1)

    sc.fill((0, 0, 0))
    for i in range(field_size):
        for j in range(field_size):
            match game_field[i][j]:
                case "player1":
                    square.x = i * cell_size
                    square.y = j * cell_size
                    pygame.draw.rect(sc, (255, 0, 0), square)
                case "player2":
                    square.x = i * cell_size
                    square.y = j * cell_size
                    pygame.draw.rect(sc, (0, 128, 0), square)
                case "wall":
                    square.x = i * cell_size
                    square.y = j * cell_size
                    pygame.draw.rect(sc, (128, 128, 128), square)

    clock.tick(FPS)  # Запускаем часы с FPS кадров в секунду

    pygame.display.update()  # Обновляем экран
