import random
import pygame
import numpy
import sys

pygame.init()

field_size = 14  # количество клеток поля
cell_size = 30  # ширина одной клетки в пикселях
width = height = field_size * cell_size  # Ширина, высота экрана
FPS = 60  # Число кадров в секунду

YaUzheHZCHtoPisat = 208
inventory = {"wall": [32, 32, 20], "spawn": [1, 1, 1], "slow": [3, 3, 0], "shield": [1, 1, 1],
             "heal": [2, 2, 0], "laser": [1, 1, 0]}

EtotHodit = playerBuilder = random.randint(0, 1)
UpravlenieDlyaCHainikov = pygame.image.load("img/управление.png")
inventoryImg = pygame.image.load("img/инвентарь.png")
shift = 14
itemChosen = 0
inventoryPixelShift = 14
pervayaKnopkaCoord = [160, 19]
isBuildingCorrect = 0
leftUpperSquare2x2 = [0, 0]
buildings = []
indexes_diagonal_cells = []
currentCursorCell = [0, 0] # текущая клетка поля под курсором
print("EtotHodit = ", "красный" if EtotHodit == 0 else "зелёный")
sc = pygame.display.set_mode((YaUzheHZCHtoPisat + width + 208, height))  # Создаем экран
clock = pygame.time.Clock()  # Создаем часы для FPS
square = pygame.Rect(0, 0, cell_size, cell_size)

game_field = [['0']*field_size for i in range(field_size)]  # игровое поле
players = [[0, 0], [field_size - 1, field_size - 1]]  # координаты игроков на поле

game_field[players[0][0]][players[0][1]] = "player1"  # расположить игрока_1 на поле
game_field[players[1][0]][players[1][1]] = "player2"  # расположить игрока_2 на поле
walls = []  # список стен
square_color = (255, 255, 255)
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

class Inventory:
    items = []

def game_field_update(p_name, x, y):  # обновление данных игрового поля
    global EtotHodit
    if (p_name == "player1" and EtotHodit == 1) or (p_name == "player2" and EtotHodit == 0):
        return
    # print(*game_field, sep='\n')
    if p_name == "player1":
        p_num = 0
    else:
        p_num = 1
    x, y = players[p_num][0]+x, players[p_num][1]+y  # вычисление новых координат игрока
    if not is_move_correct(x, y):
        return
    if p_name == "player1":
        EtotHodit = 1
    else:
        EtotHodit = 0
    # if (p_name == "player1" and EtotHodit == 1) or (p_name == "player2" and EtotHodit == 0):
    #     return
    game_field[players[p_num][0]][players[p_num][1]] = '0'
    players[p_num] = [x, y]
    game_field[x][y] = p_name

def fill_indexes_diagonal_cells():
    global indexes_diagonal_cells
    indexes_diagonal_cells.clear()
    for i in range(field_size):
        indexes_diagonal_cells.append([i, field_size - 1 - i])

def is_move_correct(x, y):  # проверка корректности хода
    if x < 0 or x >= field_size or y < 0 or y >= field_size:  # выход игрока за границы поля
        return False
    if game_field[x][y] in ("wall", "player2", "player1", "spawn", "shield"):  # столкновение игрока с запрещённым объектом
        return False
    return True

def calc_current_cursor_cell(x, y):
    global currentCursorCell
    currentCursorCell = [int((x - 208) / cell_size), int(y / cell_size)]

def draw_rect_current_cursor_cell():
    square.x = currentCursorCell[0] * cell_size + YaUzheHZCHtoPisat
    square.y = currentCursorCell[1] * cell_size
    if currentCursorCell in indexes_diagonal_cells:
        pygame.draw.rect(sc, square_color, square)
    else:
        pygame.draw.rect(sc, square_color, square)

def draw_rect_2x2_current_cursor_cell():
    square.x = currentCursorCell[0] * cell_size + YaUzheHZCHtoPisat
    square.y = currentCursorCell[1] * cell_size
    # if currentCursorCell in indexes_diagonal_cells:
    square_2x2 = pygame.Rect(square.x, square.y, cell_size * 2, cell_size * 2)
    pygame.draw.rect(sc, square_color, square_2x2)
    # else:
    #    pygame.draw.rect(sc, square_color, square)

def set_drawing_color():
    global itemChosen
    global square_color
    if currentCursorCell in indexes_diagonal_cells:
        square_color = (255, 128, 0)
    elif currentCursorCell[1] < indexes_diagonal_cells[currentCursorCell[0]][1] and playerBuilder == 0:  # часть поля первого игрока
        square_color = (0, 255, 0)
    elif currentCursorCell[1] > indexes_diagonal_cells[currentCursorCell[0]][1] and playerBuilder == 1:  # часть поля второго игрока
        square_color = (0, 255, 0)
    else:
        square_color = (255, 0, 0)


fill_indexes_diagonal_cells()

while True:
    events = pygame.event.get()  # Получаем события в прямом эфире
    for event in events:  # Цикл для обработки событий
        if event.type == pygame.QUIT:  # Сравниваем тип события с выходом из игры, окна
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] < 208:
            if 3 < event.pos[1] < 14:
                if 1 < event.pos[0] < 12 and playerBuilder == 1:
                    print("красный игрок строит")
                    playerBuilder = 0
                elif 195 < event.pos[0] < 206 and playerBuilder == 0:
                    print("зелёный игрок строит")
                    playerBuilder = 1
            elif 158 < event.pos[0] < 206:
                if event.pos[1] < inventoryPixelShift + shift:
                    # square_color = (0, 0, 0)
                    itemChosen = 1
                    print("первый предмет выбран")
                elif event.pos[1] < shift + inventoryPixelShift * 2:
                    itemChosen = 2
                    print("второй предмет выбран")
                elif event.pos[1] < shift + inventoryPixelShift * 3:
                    itemChosen = 3
                    print("третий предмет выбран")
                # elif event.pos[1] < shift + inventoryPixelShift * 5:  # 67 < x < 79
                elif 67 < event.pos[1] < 79:
                    itemChosen = 4
                    print("четвёртый предмет выбран")
            elif event.pos[0] < field_size * cell_size:
                if isBuildingCorrect == 1:
                    buildings.append(currentCursorCell)
        if event.type == pygame.MOUSEMOTION and 208 < event.pos[0] < 208 + width:
            # print(str(event.pos[0]) + " " + str(event.pos[1]))
            if itemChosen != 4:
                old_cell = currentCursorCell
                calc_current_cursor_cell(event.pos[0], event.pos[1])
                if old_cell != currentCursorCell:
                    set_drawing_color()
            elif itemChosen == 4:
                if leftUpperSquare2x2 == (0, 0):
                    calc_current_cursor_cell(event.pos[0], event.pos[1])
                    leftUpperSquare2x2 = currentCursorCell
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
        pygame.draw.line(sc, (72, 60, 50), ((i+1)*cell_size + YaUzheHZCHtoPisat, 0), ((i+1)*cell_size + YaUzheHZCHtoPisat, height))
        pygame.draw.line(sc, (72, 60, 50), (YaUzheHZCHtoPisat, (i+1)*cell_size), (width + YaUzheHZCHtoPisat, (i+1)*cell_size))
    sc.blit(UpravlenieDlyaCHainikov, (420 + YaUzheHZCHtoPisat, 0))
    sc.blit(inventoryImg, (0, 0))
    if itemChosen != 4:
        draw_rect_current_cursor_cell()
    elif itemChosen == 4:
        draw_rect_2x2_current_cursor_cell()
    pygame.draw.line(sc, (128, 128, 128), (width + YaUzheHZCHtoPisat, 0), (YaUzheHZCHtoPisat, width))
    for i in range(field_size):
        for j in range(field_size):
            if game_field[i][j] == "player1":
                square.x = i * cell_size + YaUzheHZCHtoPisat
                square.y = j * cell_size
                pygame.draw.rect(sc, (255, 0, 0), square)
            elif game_field[i][j] == "player2":
                square.x = i * cell_size + YaUzheHZCHtoPisat
                square.y = j * cell_size
                pygame.draw.rect(sc, (0, 128, 0), square)
            elif game_field[i][j] == "wall":
                square.x = i * cell_size
                square.y = j * cell_size
                pygame.draw.rect(sc, (128, 128, 128), square)

    clock.tick(FPS)  # Запускаем часы с FPS кадров в секунду

    pygame.display.update()  # Обновляем экран
