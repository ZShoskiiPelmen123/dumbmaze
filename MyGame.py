import random
import pygame
import sys

pygame.init()

field_size = 14  # количество клеток поля
cell_size = 30  # ширина одной клетки в пикселях
width = height = field_size * cell_size  # Ширина, высота экрана
FPS = 60  # Число кадров в секунду
# inventory: "название предмета": доступноИгроку1, доступноИгроку2, минимум, максимум
inventory = {"wall": [32, 32, 20, 32], "spawn": [1, 1, 1, 1], "slow": [3, 3, 0, 3], "shield": [1, 1, 1, 1],
             "heal": [2, 2, 0, 1], "laser": [1, 1, 0, 1]}

currentPlayerMove = playerBuilder = random.randint(0, 1)  # определить случайно чей первый ход
controlsPng = pygame.image.load("app/img/управление.png")
inventoryImg = pygame.image.load("app/img/инвентарь.png")
inventoryPngWidth = inventoryImg.get_width()
controlsPngWidth = controlsPng.get_width()
shift = 14
itemChosen = 1  # выбранный для расстановки предмет инвентаря
inventoryPixelShift = 14
leftUpperSquare2x2 = [0, 0]  # координаты верхнего левого угла квадрата 2x2
square2x2AllCells = []  # координаты всех клеток квадрата 2x2
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
square_color = (0, 0, 0)
# "НазваниеНаправленияДвижения": [клавишаПервогоИгрока, клавишаВторогоИгрока, смещениеПоИксу, смещениеПоИгреку]
player_controls = {"up": [pygame.K_w, pygame.K_u, 0, -1], "down": [pygame.K_s, pygame.K_j, 0, 1],
                   "left": [pygame.K_a, pygame.K_h, -1, 0], "right": [pygame.K_d, pygame.K_k, 1, 0],
                   "up_left": [pygame.K_q, pygame.K_y, -1, -1], "up_right": [pygame.K_e, pygame.K_i, 1, -1],
                   "down_left": [pygame.K_z, pygame.K_b, -1, 1], "down_right": [pygame.K_c, pygame.K_m, 1, 1]}


def game_field_update(p_name, x, y):  # обновление данных игрового поля
    global currentPlayerMove
    if (p_name == "player1" and currentPlayerMove == 1) or (p_name == "player2" and currentPlayerMove == 0):
        return
    # print(*game_field, sep='\n')
    p_num = 0 if p_name == "player1" else 1
    x, y = players[p_num][0] + x, players[p_num][1] + y  # вычисление новых координат игрока
    if not is_move_correct(x, y):
        return
    currentPlayerMove = 1 if p_name == "player1" else 0
    new_name = p_name
    if game_field[x][y] in ['slow1', 'slow2']:  # клетка, в которую происходит переход
        new_name = game_field[x][y] + "|" + new_name
    if game_field[players[p_num][0]][players[p_num][1]].startswith("slow1|"):  # нынешняя клетка игрока
        game_field[players[p_num][0]][players[p_num][1]] = "slow1"
    elif game_field[players[p_num][0]][players[p_num][1]].startswith("slow2|"):  # нынешняя клетка игрока
        game_field[players[p_num][0]][players[p_num][1]] = "slow2"
    else:
        game_field[players[p_num][0]][players[p_num][1]] = '0'
    players[p_num] = [x, y]  # новые координаты игрока
    game_field[x][y] = new_name


def fill_2x2_cells(left_upper_coord):  # заполнить координаты клеток квадрата 2x2
    square2x2AllCells.clear()
    square2x2AllCells.append(left_upper_coord)
    square2x2AllCells.append([left_upper_coord[0], left_upper_coord[1] + 1])
    square2x2AllCells.append([left_upper_coord[0] + 1, left_upper_coord[1]])
    square2x2AllCells.append([left_upper_coord[0] + 1, left_upper_coord[1] + 1])


def fill_indexes_diagonal_cells():  # заполнить индексы диагональных элементов
    global indexes_diagonal_cells
    indexes_diagonal_cells.clear()
    for i in range(field_size):
        indexes_diagonal_cells.append([i, field_size - 1 - i])


def is_move_correct(x, y):  # проверка корректности хода при передвижении игрока
    if x < 0 or x >= field_size or y < 0 or y >= field_size:  # выход игрока за границы поля
        return False
    # столкновение игрока с объектом, запрещённым для прохода сквозь него
    if not (game_field[x][y] == "0" or game_field[x][y] in ["slow1", "slow2"]):
        return False
    return True


def is_building_correct(item_num):  # проверка корректности размещения объекта на поле
    obj_cells = [currentCursorCell]
    if item_num == 4:
        fill_2x2_cells(leftUpperSquare2x2)
        obj_cells = square2x2AllCells
    for obj_cell in obj_cells:
        if game_field[obj_cell[0]][obj_cell[1]] in inventory.keys() | ["player1", "player2"]:
            return False
        if itemChosen == 4 and (
            [leftUpperSquare2x2[0] + 1, leftUpperSquare2x2[1]] in indexes_diagonal_cells or
            leftUpperSquare2x2[1] + 1 < indexes_diagonal_cells[leftUpperSquare2x2[0]][1] and playerBuilder == 1 or
            leftUpperSquare2x2[1] + 1 > indexes_diagonal_cells[leftUpperSquare2x2[0]][1] and playerBuilder == 0
        ):
            return False
        else:
            if (currentCursorCell[1] < indexes_diagonal_cells[currentCursorCell[0]][1] and playerBuilder == 1 or
                    currentCursorCell[1] > indexes_diagonal_cells[currentCursorCell[0]][1] and playerBuilder == 0):
                return False
    return True


# взять у игрока предмет из инвентаря
def take_from_inventory(player_num, item_num):
    global inventory
    if list(inventory.values())[item_num][player_num] > 0:  # оставшееся кол-во > 0
        inventory[list(inventory.keys())[item_num]][player_num] -= 1  # уменьшить кол-во
    else:
        return False  # не удалось взять предмет (их нет)
    return True  # предмет успешно взят


def calc_current_cursor_cell(x, y):  # вычисление текущих координат курсора
    global currentCursorCell
    currentCursorCell = [int((x - inventoryPngWidth) / cell_size), int(y / cell_size)]


def draw_rect_current_cursor_cell(size):  # нарисовать квадрат длиной size под курсором
    temp_cell = currentCursorCell if size == 1 else leftUpperSquare2x2
    x = temp_cell[0] * cell_size + inventoryPngWidth
    y = temp_cell[1] * cell_size
    temp_square = pygame.Rect(x, y, cell_size * size, cell_size * size)
    pygame.draw.rect(sc, square_color, temp_square)


def set_drawing_color(size):
    global square_color
    lus = leftUpperSquare2x2
    if is_building_correct(itemChosen):
        if (size == 1 and currentCursorCell in indexes_diagonal_cells or
            size == 2 and
            (playerBuilder == 0 and [lus[0] + 1, lus[1] + 1] in indexes_diagonal_cells or
             playerBuilder == 1 and [lus[0], lus[1]] in indexes_diagonal_cells)):
            square_color = (255, 128, 0)
        else:
            square_color = (0, 255, 0)
    else:
        square_color = (255, 0, 0)


fill_indexes_diagonal_cells()

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # 1-я часть ширины экрана - до конца инвентаря
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
            # 2-я часть ширины экрана - до конца игрового поля
            elif event.pos[0] < field_size * cell_size + inventoryPngWidth:
                if itemChosen != 0 and is_building_correct(itemChosen):
                    if not (take_from_inventory(playerBuilder, itemChosen - 1)):
                        continue
                    if itemChosen == 4:
                        for cellCoord2x2 in square2x2AllCells:
                            game_field[cellCoord2x2[0]][cellCoord2x2[1]] = list(inventory.keys())[itemChosen - 1]
                    elif itemChosen == 3:
                        game_field[currentCursorCell[0]][currentCursorCell[1]] = (list(inventory.keys())[itemChosen - 1]
                                                                                  + str(playerBuilder + 1))
                    else:
                        game_field[currentCursorCell[0]][currentCursorCell[1]] = list(inventory.keys())[itemChosen - 1]
        if event.type == pygame.MOUSEMOTION:
            if inventoryPngWidth < event.pos[0] < inventoryPngWidth + width and 0 < event.pos[1] < height:
                if itemChosen != 4:
                    old_cell = currentCursorCell
                    calc_current_cursor_cell(event.pos[0], event.pos[1])
                    leftUpperSquare2x2 = currentCursorCell
                    if old_cell != currentCursorCell:
                        set_drawing_color(1)
                # блок вычисления координат верхнего левого угла квадрата 2x2
                # для отображения на поле при расстановке объектов
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
                        # курсор ни в одной из клеток нарисованного квадрата
                        elif not (currentCursorCell[0] in (leftUpperSquare2x2[0], leftUpperSquare2x2[0] + 1) and
                                  (currentCursorCell[1] in (leftUpperSquare2x2[1], leftUpperSquare2x2[1] + 1))):
                            # курсор в нижнем правом углу игрового поля
                            if currentCursorCell[0] == currentCursorCell[1] == field_size - 1:
                                leftUpperSquare2x2 = currentCursorCell
                                leftUpperSquare2x2[0] -= 1
                                leftUpperSquare2x2[1] -= 1
                            # курсор на последнем столбце игрового поля
                            elif currentCursorCell[0] == field_size - 1:
                                leftUpperSquare2x2 = currentCursorCell
                                leftUpperSquare2x2[0] -= 1
                            # курсор на последней строке игрового поля
                            elif currentCursorCell[1] == field_size - 1:
                                leftUpperSquare2x2 = currentCursorCell
                                leftUpperSquare2x2[1] -= 1
                            else:
                                leftUpperSquare2x2 = currentCursorCell
        # управление игроками с клавиатуры
        if event.type == pygame.KEYDOWN:
            player_name = "player1" if event.key in [i[0] for i in player_controls.values()] else "player2"
            for value in player_controls.values():
                if event.key in [value[0], value[1]]:
                    game_field_update(player_name, value[2], value[3])
                    break

    sc.fill((0, 0, 0))
    # прорисовка поля линиями для визуального разделения его на клетки
    for i in range(field_size):
        pygame.draw.line(sc, (72, 60, 50), ((i + 1) * cell_size + inventoryPngWidth, 0),
                         ((i + 1) * cell_size + inventoryPngWidth, height))
        pygame.draw.line(sc, (72, 60, 50), (inventoryPngWidth, (i + 1) * cell_size),
                         (width + inventoryPngWidth, (i + 1) * cell_size))
    sc.blit(controlsPng, (420 + inventoryPngWidth, 0))
    sc.blit(inventoryImg, (0, 0))
    # динамическая прорисовка объекта при их расстановке на поле
    if itemChosen != 4:
        draw_rect_current_cursor_cell(1)
    elif itemChosen == 4 and leftUpperSquare2x2 != (0, 0):
        set_drawing_color(2)
        draw_rect_current_cursor_cell(2)
    # прорисовка диагональной линии
    pygame.draw.line(sc, (128, 128, 128), (width + inventoryPngWidth, 0), (inventoryPngWidth, width))
    # прорисовка объектов по матрице, состоящей из индексов элементов поля
    for i in range(field_size):
        for j in range(field_size):
            if game_field[i][j] != 0:
                square.x = i * cell_size + inventoryPngWidth
                square.y = j * cell_size
            if game_field[i][j] in ["player1", "slow1|player1", "slow2|player1"]:
                pygame.draw.rect(sc, (255, 0, 0), square)
            elif game_field[i][j] in ["player2", "slow1|player2", "slow2|player2"]:
                pygame.draw.rect(sc, (0, 128, 0), square)
            elif game_field[i][j] == "wall":
                pygame.draw.rect(sc, (128, 128, 128), square)
            elif game_field[i][j] == "shield":
                pygame.draw.rect(sc, (0, 64, 255), square)
            elif game_field[i][j] == "spawn":
                pygame.draw.rect(sc, (128, 64, 64), square)
            elif game_field[i][j] in ["slow1"]:
                pygame.draw.rect(sc, (0, 123, 255), square)
            elif game_field[i][j] in ["slow2"]:
                pygame.draw.rect(sc, (0, 255, 123), square)
            elif game_field[i][j] == "heal":
                pygame.draw.rect(sc, (255, 0, 255), square)
            elif game_field[i][j] == "laser":
                pygame.draw.rect(sc, (255, 255, 0), square)

    clock.tick(FPS)  # Запускаем часы с FPS кадров в секунду

    pygame.display.update()  # Обновляем экран
