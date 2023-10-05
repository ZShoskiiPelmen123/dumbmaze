import random
import pygame
import sys

pygame.init()

field_size = 14 # количество клеток поля
cell_size = 30 # ширина одной клетки в пикселях
width = height = field_size * cell_size  # Ширина, высота экрана
FPS = 60  # Число кадров в секунду

EtotHodit = random.randint(0, 1)
UpravlenieDlyaCHainikov = pygame.image.load("управление.png")
print(str(EtotHodit))
sc = pygame.display.set_mode((width + 208, height))  # Создаем экран
clock = pygame.time.Clock()  # Создаем часы для FPS
square = pygame.Rect(0, 0, cell_size, cell_size)

game_field = [['0']*field_size for i in range(field_size)]  # игровое поле
players = [[0, 0], [field_size - 1, field_size - 1]]  # координаты игроков на поле

game_field[players[0][0]][players[0][1]] = "player1"  # расположить игрока_1 на поле
game_field[players[1][0]][players[1][1]] = "player2"  # расположить игрока_2 на поле
walls = []  # список стен
player_controls = {"up": [pygame.K_w, pygame.K_u, "W", "U"], "down": [pygame.K_s, pygame.K_j, "S", "J"],
                   "right": [pygame.K_d, pygame.K_k, "D", "K"], "left": [pygame.K_a, pygame.K_h, "A", "H"],
                   "up_left": [pygame.K_q, pygame.K_y, "Q", "Y"], "up_right": [pygame.K_e,  pygame.K_i, "E", "I"],
                   "down_right": [pygame.K_c, pygame.K_m, "C", "M"], "down_left": [pygame.K_z, pygame.K_b, "Z", "B"]}

"""
for i in range(1, field_size - 1):  # случайная расстановка стен для теста
    rnd = random.randrange(field_size)
    walls.append([i, rnd])
    game_field[i][rnd] = "wall"
"""

def game_field_update(p_name, x, y):  # обновление данных игрового поля
    global EtotHodit
    if p_name == "player1" and EtotHodit == 1 or p_name == "player2" and EtotHodit == 0:
        return
    if p_name == "player1":
        p_num = 0
        EtotHodit = 1
    else:
        p_num = 1
        EtotHodit = 0
    x, y = players[p_num][0]+x, players[p_num][1]+y  # вычисление новых координат игрока
    if not is_move_correct(x, y):
        return
    if p_name == "player1" and EtotHodit == 1 or p_name == "player2" and EtotHodit == 0:
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
            if event.key in [i[0] for i in player_controls.values()]:
                player_name = "player1"
            else:
                player_name = "player2"
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
        pygame.draw.line(sc, (72, 60, 50), ((i+1)*cell_size, 0), ((i+1)*cell_size, height))
    for i in range(field_size):
        pygame.draw.line(sc, (72, 60, 50), (0, (i+1)*cell_size), (width, (i+1)*cell_size))
    sc.blit(UpravlenieDlyaCHainikov, (420, 0))

    pygame.draw.line(sc, (128, 128, 128), (width, 0), (0, width))
    for i in range(field_size):
        for j in range(field_size):
            if game_field[i][j] == "player1":
                square.x = i * cell_size
                square.y = j * cell_size
                pygame.draw.rect(sc, (255, 0, 0), square)
            elif game_field[i][j] == "player2":
                square.x = i * cell_size
                square.y = j * cell_size
                pygame.draw.rect(sc, (0, 128, 0), square)
            elif game_field[i][j] == "wall":
                square.x = i * cell_size
                square.y = j * cell_size
                pygame.draw.rect(sc, (128, 128, 128), square)

    clock.tick(FPS)  # Запускаем часы с FPS кадров в секунду

    pygame.display.update()  # Обновляем экран
