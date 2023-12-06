import random
import pygame
import sys

pygame.init()

field_size = 14  # количество клеток поля
cell_size = 30  # ширина одной клетки в пикселях
width = height = field_size * cell_size  # Ширина, высота экрана
FPS = 60  # Число кадров в секунду

inventory = {"wall": [32, 32, 20], "spawn": [1, 1, 1], "slow": [3, 3, 0], "shield": [1, 1, 1],
             "heal": [2, 2, 0], "laser": [1, 1, 0]}

currentPlayerMove = playerBuilder = random.randint(0, 1)  # определить случайно чей первый ход
controlsPng = pygame.image.load("img/управление.png")
inventoryImg = pygame.image.load("img/инвентарь.png")
inventoryPngWidth = inventoryImg.get_width()
controlsPngWidth = controlsPng.get_width()
shift = 14
itemChosen = 0  # выбранный для расстановки предмет инвентаря
inventoryPixelShift = 14
firstButtonCoord = [160, 19]
isBuildingCorrect = 0
leftUpperSquare2x2 = [0, 0]
buildings = []
indexes_diagonal_cells = []  # индексы диагональных элементов
currentCursorCell = [0, 0]  # текущая клетка поля под курсором
print("currentPlayerMove = ", "красный" if currentPlayerMove == 0 else "зелёный")
sc = pygame.display.set_mode((inventoryPngWidth + width + controlsPngWidth, height))  # Создаем экран
clock = pygame.time.Clock()  # Создаем часы для FPS
square = pygame.Rect(0, 0, cell_size, cell_size)  # стандартный квадрат длиной 1 клетка для рисования на поле

game_field = [['0'] * field_size for i in range(field_size)]  # игровое поле
players = [[0, 0], [field_size - 1, field_size - 1]]  # координаты игроков на поле

game_field[players[0][0]][players[0][1]] = "player1"  # расположить игрока_1 на поле
game_field[players[1][0]][players[1][1]] = "player2"  # расположить игрока_2 на поле
walls = []  # список стен
square_color = (0, 0, 0)
player_controls = {"up": [pygame.K_w, pygame.K_u, "W", "U"], "down": [pygame.K_s, pygame.K_j, "S", "J"],
                   "right": [pygame.K_d, pygame.K_k, "D", "K"], "left": [pygame.K_a, pygame.K_h, "A", "H"],
                   "up_left": [pygame.K_q, pygame.K_y, "Q", "Y"], "up_right": [pygame.K_e, pygame.K_i, "E", "I"],
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
    global currentPlayerMove
    if (p_name == "player1" and currentPlayerMove == 1) or (p_name == "player2" and currentPlayerMove == 0):
        return
    # print(*game_field, sep='\n')
    if p_name == "player1":
        p_num = 0
    else:
        p_num = 1
    x, y = players[p_num][0] + x, players[p_num][1] + y  # вычисление новых координат игрока
    if not is_move_correct(x, y):
        return
    if p_name == "player1":
        currentPlayerMove = 1
    else:
        currentPlayerMove = 0
    game_field[players[p_num][0]][players[p_num][1]] = '0'
    players[p_num] = [x, y]
    game_field[x][y] = p_name


def fill_indexes_diagonal_cells():  # заполнить индексы диагональных элементов
    global indexes_diagonal_cells
    indexes_diagonal_cells.clear()
    for i in range(field_size):
        indexes_diagonal_cells.append([i, field_size - 1 - i])


def is_move_correct(x, y):  # проверка корректности хода
    if x < 0 or x >= field_size or y < 0 or y >= field_size:  # выход игрока за границы поля
        return False
    # столкновение игрока с запрещённым объектом
    if game_field[x][y] in ("wall", "player2", "player1", "spawn", "shield"):
        return False
    return True


def calc_current_cursor_cell(x, y):  # вычисление текущих координат курсора
    global currentCursorCell
    currentCursorCell = [int((x - inventoryPngWidth) / cell_size), int(y / cell_size)]


def draw_rect_current_cursor_cell():  # нарисовать квадрат под курсором
    square.x = currentCursorCell[0] * cell_size + inventoryPngWidth
    square.y = currentCursorCell[1] * cell_size
    pygame.draw.rect(sc, square_color, square)


def draw_rect_2x2_current_cursor_cell():  # нарисовать квадрат 2x2 под курсором
    square.x = leftUpperSquare2x2[0] * cell_size + inventoryPngWidth
    square.y = leftUpperSquare2x2[1] * cell_size
    square_2x2 = pygame.Rect(square.x, square.y, cell_size * 2, cell_size * 2)
    pygame.draw.rect(sc, square_color, square_2x2)


def set_drawing_color():
    global itemChosen
    global square_color
    if currentCursorCell in indexes_diagonal_cells:
        square_color = (255, 128, 0)
    # часть поля первого игрока
    elif currentCursorCell[1] < indexes_diagonal_cells[currentCursorCell[0]][1] and playerBuilder == 0:
        square_color = (0, 255, 0)
    # часть поля второго игрока
    elif currentCursorCell[1] > indexes_diagonal_cells[currentCursorCell[0]][1] and playerBuilder == 1:
        square_color = (0, 255, 0)
    else:
        square_color = (255, 0, 0)


def set_drawing_color_2x2():
    global itemChosen
    global square_color
    if [leftUpperSquare2x2[0] + 1, leftUpperSquare2x2[1] + 1] in indexes_diagonal_cells and playerBuilder == 0 or \
            [leftUpperSquare2x2[0], leftUpperSquare2x2[1]] in indexes_diagonal_cells and playerBuilder == 1:
        square_color = (255, 128, 0)
    elif [leftUpperSquare2x2[0] + 1, leftUpperSquare2x2[1]] in indexes_diagonal_cells:
        square_color = (255, 0, 0)
    # часть поля первого игрока
    elif leftUpperSquare2x2[1] + 1 < indexes_diagonal_cells[leftUpperSquare2x2[0]][1] and playerBuilder == 0:
        square_color = (0, 255, 0)
    # часть поля второго игрока
    elif leftUpperSquare2x2[1] + 1 > indexes_diagonal_cells[leftUpperSquare2x2[0]][1] and playerBuilder == 1:
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
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if event.pos[0] < inventoryPngWidth:
                if 3 < event.pos[1] < 14:
                    if 12 > event.pos[0] > 1 == playerBuilder:
                        print("красный игрок строит")
                        playerBuilder = 0
                    elif 195 < event.pos[0] < 206 and playerBuilder == 0:
                        print("зелёный игрок строит")
                        playerBuilder = 1
                elif 158 < event.pos[0] < 206:
                    if event.pos[1] < inventoryPixelShift + shift:
                        itemChosen = 1
                        print("первый предмет выбран")
                    elif event.pos[1] < shift + inventoryPixelShift * 2:
                        itemChosen = 2
                        print("второй предмет выбран")
                    elif event.pos[1] < shift + inventoryPixelShift * 3:
                        itemChosen = 3
                        print("третий предмет выбран")
                    elif 67 < event.pos[1] < 79:
                        itemChosen = 4
                        print("четвёртый предмет выбран")
            elif event.pos[0] < field_size * cell_size:
                if isBuildingCorrect == 1:
                    buildings.append(currentCursorCell)
        if event.type == pygame.MOUSEMOTION:
            if inventoryPngWidth < event.pos[0] < inventoryPngWidth + width:
                if itemChosen != 4:
                    old_cell = currentCursorCell
                    calc_current_cursor_cell(event.pos[0], event.pos[1])
                    leftUpperSquare2x2 = currentCursorCell
                    if old_cell != currentCursorCell:
                        set_drawing_color()
                elif itemChosen == 4:
                    if leftUpperSquare2x2 == (0, 0):
                        calc_current_cursor_cell(event.pos[0], event.pos[1])
                        if (currentCursorCell[0] != field_size - 1 and
                                currentCursorCell[1] != field_size - 1):
                            leftUpperSquare2x2 = currentCursorCell
                        elif currentCursorCell[1] == field_size - 1:
                            leftUpperSquare2x2 = currentCursorCell
                            leftUpperSquare2x2[1] -= 1
                        elif currentCursorCell[0] == field_size - 1:
                            leftUpperSquare2x2 = currentCursorCell
                            leftUpperSquare2x2[0] -= 1
                    else:
                        calc_current_cursor_cell(event.pos[0], event.pos[1])
                        # курсор левее нарисованного квадрата
                        if (currentCursorCell[0] == leftUpperSquare2x2[0] - 1 and
                                currentCursorCell[1] == leftUpperSquare2x2[1] + 1):
                            leftUpperSquare2x2[0] -= 1
                        # курсор выше нарисованного квадрата
                        elif (currentCursorCell[0] == leftUpperSquare2x2[0] + 1 and
                              currentCursorCell[1] == leftUpperSquare2x2[1] - 1):
                            leftUpperSquare2x2[1] -= 1
                        # курсор правее нарисованного квадрата
                        elif currentCursorCell[0] == leftUpperSquare2x2[0] + 2:
                            leftUpperSquare2x2[0] += 1
                        # курсор ниже нарисованного квадрата
                        elif currentCursorCell[1] == leftUpperSquare2x2[1] + 2:
                            leftUpperSquare2x2[1] += 1
                        # курсор не в одной из клеток нарисованного квадрата
                        elif not (currentCursorCell[0] in (leftUpperSquare2x2[0], leftUpperSquare2x2[0] + 1) and
                                  (currentCursorCell[1] in (leftUpperSquare2x2[1], leftUpperSquare2x2[1] + 1))):
                            # курсор в нижнем правом углу
                            if currentCursorCell[0] == currentCursorCell[1] == field_size - 1:
                                leftUpperSquare2x2 = currentCursorCell
                                leftUpperSquare2x2[0] -= 1
                                leftUpperSquare2x2[1] -= 1
                            # курсор на последнем столбце
                            elif currentCursorCell[0] == field_size - 1:
                                leftUpperSquare2x2 = currentCursorCell
                                leftUpperSquare2x2[0] -= 1
                            # курсор на последней строке
                            elif currentCursorCell[1] == field_size - 1:
                                leftUpperSquare2x2 = currentCursorCell
                                leftUpperSquare2x2[1] -= 1
                            else:
                                leftUpperSquare2x2 = currentCursorCell
        # управление игроками с клавиатуры
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
    # прорисовка поля линиями для визуального разделения его на клетки
    for i in range(field_size):
        pygame.draw.line(sc, (72, 60, 50), ((i + 1) * cell_size + inventoryPngWidth, 0),
                         ((i + 1) * cell_size + inventoryPngWidth, height))
        pygame.draw.line(sc, (72, 60, 50), (inventoryPngWidth, (i + 1) * cell_size),
                         (width + inventoryPngWidth, (i + 1) * cell_size))
    sc.blit(controlsPng, (420 + inventoryPngWidth, 0))
    sc.blit(inventoryImg, (0, 0))
    # динамическая прорисовка объекта при расстановке объектов на поле
    if itemChosen != 4:
        draw_rect_current_cursor_cell()
    elif itemChosen == 4 and leftUpperSquare2x2 != (0, 0):
        set_drawing_color_2x2()
        draw_rect_2x2_current_cursor_cell()
    # прорисовка диагональной линии
    pygame.draw.line(sc, (128, 128, 128), (width + inventoryPngWidth, 0), (inventoryPngWidth, width))
    # прорисовка объектов по матрице
    for i in range(field_size):
        for j in range(field_size):
            if game_field[i][j] == "player1":
                square.x = i * cell_size + inventoryPngWidth
                square.y = j * cell_size
                pygame.draw.rect(sc, (255, 0, 0), square)
            elif game_field[i][j] == "player2":
                square.x = i * cell_size + inventoryPngWidth
                square.y = j * cell_size
                pygame.draw.rect(sc, (0, 128, 0), square)
            elif game_field[i][j] == "wall":
                square.x = i * cell_size
                square.y = j * cell_size
                pygame.draw.rect(sc, (128, 128, 128), square)

    clock.tick(FPS)  # Запускаем часы с FPS кадров в секунду

    pygame.display.update()  # Обновляем экран
