import math

print("-----Calculate_Discriminant 1.6-----")

f = int(input('Если задача с одной переменной напишите "1" если с двумя переменными где всего один корень напишите "2": '))

def pelmen():
    if f == 1:
        a = int(input("Напиши x^2: "))
        b = int(input("Напиши x: "))
        c = int(input("Напиши число: "))
        while a == 0 or b == 0 or c == 0:
            if a == 0:
                print("Напишите так чтобы x^2 не был равен нулю.")
            elif b == 0:
                print("Напишите так чтобы x не был равен нулю.")
            elif c == 0:
                print("Напишите так чтобы число не было равно нулю.")
            a = int(input("Напиши x^2: "))
            b = int(input("Напиши x: "))
            c = int(input("Напиши число: "))

        d = b**2 - 4 * a * c

        print("D = ", d)

        if d > 0:
            x1 = (-b - math.sqrt(d)) / (2 * a)
            print("x1 = ", x1)
            x2 = (-b + math.sqrt(d)) / (2 * a)
            print("x2 = ", x2)
            x1_str = "- " + str(x1) if x1 >= 0 else " " + str(x1)
            x2_str = "- " + str(x2) if x2 >= 0 else " " + str(x2)
            print("Разложение на множители: " + str(a) + "( x " + x1_str + ") * ( x " + x2_str + ")")
        elif d == 0:
            x1 = (-b - math.sqrt(d)) / 2 * a
            print("x1 = ", x1)
        elif d < 0:
            print("Пустое множество")
    elif f == 2:
        a = int(input("Напиши x^2: "))
        b = int(input("Напиши x: "))
        c_str = input("Напиши число с переменной: ")
        # c = int(input("Напиши число с переменной: ")[0])
        while a == 0 or b == 0:
            if a == 0:
                print("Напишите так чтобы x^2 не был равен нулю.")
            elif b == 0:
                print("Напишите так чтобы x не был равен нулю.")
            a = int(input("Напиши x^2: "))
            b = int(input("Напиши x: "))
            c_str = input("Напиши число с переменной: ")

        p = b**2 / (4*a) - int(c_str[0])
        if c_str[1] == '-':
            p *= -1

        print("p = ", p)

        if c_str[1] == "+":
            d = b ** 2 - 4 * a * (int(c_str[0]) + p)
        elif c_str[1] == "-":
            d = b ** 2 - 4 * a * (int(c_str[0]) - p)
        print("D = ", d)

        if d > 0:
            x1 = (-b - math.sqrt(d)) / 2 * a
            print("x1 = ", x1)
            x2 = (-b + math.sqrt(d)) / 2 * a
            print("x2 = ", x2)
        elif d == 0:
            x1 = (-b - math.sqrt(d)) / 2 * a
            print("x1 = ", x1)
        elif d < 0:
            print("Пустое множество")


pelmen()


if f < 1 or f > 2:
    while f < 1 or f > 2:
        f = int(input('Напишите так, чтобы была цифра "1" или "2": '))
        pelmen()