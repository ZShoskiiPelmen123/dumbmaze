v = float(input("Напишите 1 или 2: "))
if v == 1:
    a = float(input("Напишите a: "))
    b = float(input("Напишите b: "))
    c = float(input("Напишите c: "))
    cosA = (c**2 + b**2 - a**2)/(2*c*b)
    print(cosA)
else:
    cosA = float(input("Напишите косинус угла напротив стороны, которую хотите найти: "))
    b = float(input("Напишите b: "))
    c = float(input("Напишите c: "))
    a = ((b + c) - (2 * b * c * cosA))**0.5
    print(a)