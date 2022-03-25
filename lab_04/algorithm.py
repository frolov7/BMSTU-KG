import numpy as np
from math import sin, cos, radians, pi, sqrt


def tmirrored(dots, x, y, x_center, y_center, color):
    dots.extend([
        [x, y, color],
        [2 * x_center - x, y, color],
        [x, 2 * y_center - y, color],
        [2 * x_center - x, 2 * y_center - y, color],
        [y + x_center - y_center, x + y_center - x_center, color],
        [-y + x_center + y_center, x + y_center - x_center, color],
        [y + x_center - y_center, -x + y_center + x_center, color],
        [-y + x_center + y_center, -x + y_center + x_center, color]
    ])


def dmirrored(dots, x, y, x_center, y_center, color):
    dots.extend([
        [x, y, color],
        [2 * x_center - x, y, color],
        [x, 2 * y_center - y, color],
        [2 * x_center - x, 2 * y_center - y, color]
    ])


# Bresenham method circle
# разность квадратов расстояний от окружности до пикселов в горизонтальном и диагональном направлениях
# d = |(xi + 1)2 + (yi )2 -R2| - |(xi + 1)2 + (yi -1)2 -R2|
# Di < 0
# d <= 0 выбираем пиксел (xi +1 , уi ) - горизонт
# d > 0 выбираем пиксел (xi +1 , уi -1) - диагональный
# Di > 0
# d' <= 0 выбираем пиксел (xi +1 , уi -1) - диагональный
# d' > 0 выбираем пиксел (xi , уi -1)- вертикальный
# Di = 0 выбираем пиксел (xi +1 , уi -1) - диагональный
def brescircle(x_center, y_center, radius, color):
    dots = []
    x = 0
    y = radius
    delta = 2 * (1 - radius)

    tmirrored(dots, x + x_center, y + y_center, x_center, y_center, color)

    while x < y:  # идем от нуля до радиуса
        if delta <= 0:  # если d < 0 диагональная точка (xi, + 1, уi - 1) находится внутри окружности
            delta_temp = 2 * (
                    delta + y) - 1  # Дополнение до полного квадрата члена (yi )^2 с помощью добавления и вычитания - 2yi + 1
            x += 1
            if delta_temp >= 0:  # расстояние до диагонального пикселя меньше
                delta += 2 * (x - y + 1)  # диагональный шаг
                y -= 1
            else: 
                delta += 2 * x + 1  # горизонтальный шаг

        else:
            delta_temp = 2 * (delta - x) - 1
            y -= 1
            if delta_temp < 0:  # расстояние от окружности до вертикального пиксела (xi, , уi -1) больше
                delta += 2 * (x - y + 1)  # выбираем диагональный
                x += 1
            else:  # расстояние от окружности до диагонального пиксела больше. Если = 0, то диагональный
                delta -= 2 * y - 1  # вертикальный

        tmirrored(dots, x + x_center, y + y_center, x_center, y_center, color)

    return dots


# Bresenham method ellipse
def bresellipse(x_center, y_center, frad, srad, color):
    dots = []
    x = 0  # Компонента x
    y = srad  # Компонента y
    # srad^2, srad - большая полуось
    # frad^2, frad - малая полуось
    delta = srad ** 2 - frad ** 2 * (2 * srad + 1)  # Функция координат точки (x+1, y-1/2)

    dmirrored(dots, x + x_center, y + y_center, x_center, y_center, color)

    while y > 0:
        if delta <= 0:  # Если это значение меньше нуля, то дополнительная точка (x+1, y-1/2) находится внутри эллипса
            delta_temp = 2 * delta + frad ** 2 * (2 * y - 1)
            x += 1
            delta += srad ** 2 * (2 * x + 1)
            if delta_temp >= 0:  # расстояние до диагонального пикселя меньше
                y -= 1
                delta += frad ** 2 * (-2 * y + 1)  # диагональный шаг
        else:
            delta_temp = 2 * delta + srad ** 2 * (-2 * x - 1)  # Переход по вертикали
            y -= 1
            delta += frad ** 2 * (-2 * y + 1)
            if delta_temp < 0:  # расстояние от окружности до вертикального пиксела (xi, , уi -1) больше
                x += 1
                delta += srad ** 2 * (2 * x + 1)

        dmirrored(dots, x + x_center, y + y_center, x_center, y_center, color)

    return dots


# Canonical equation circle
# из канонического уравнения выражается у, устанавливается приращение аргумента х = 1
# находятся точки для 1/8 окружности и отражаются относительно х и у
def cancircle(x_center, y_center, radius, color):
    dots = []

    for x in range(x_center, x_center + int(radius / sqrt(2)) + 1):
        y = sqrt(radius ** 2 - (x - x_center) ** 2) + y_center  # y = sqrt(R^2 - x^2)
        tmirrored(dots, x, y, x_center, y_center, color)

    return dots


# Canonical equation ellipse
# Строим 1 /4 часть элипса, потому как эллипс не симетричен относительно биссектрисы.
# Находим точку где угол наклона касательной к элипсу становится < 45, т.к в этой точке приращения х и н меняют свою динамику:
# координата имевшая большее приращение, теперь получает меньшее и наоборот
def canellipse(x_center, y_center, frad, srad, color):
    dots = []
    limit = int(x_center + frad / sqrt(1 + srad ** 2 / frad ** 2))

    for x in range(x_center, limit + 1):
        y = sqrt(frad ** 2 * srad ** 2 - (x - x_center) ** 2 * srad ** 2) / frad + y_center
        dmirrored(dots, x, y, x_center, y_center, color)

    limit = int(y_center + srad / sqrt(1 + frad ** 2 / srad ** 2))

    for y in range(limit, y_center - 1, -1):
        x = sqrt(frad ** 2 * srad ** 2 - (y - y_center) ** 2 * frad ** 2) / srad + x_center
        dmirrored(dots, x, y, x_center, y_center, color)

    return dots


# Midpoint method circle
# анализируется средняя точка между двумя пикселями.
# Определяется, находится точка внутри или вне эллипса, и взависимости от этого делается выбор пикселя.
def midpcircle(x_center, y_center, radius, color):
    dots = []
    x = radius
    y = 0

    tmirrored(dots, x + x_center, y + y_center, x_center, y_center, color)
    delta = 1 - radius

    while x > y:
        y += 1
        if delta > 0:  # Функция - положительная, выбираем диагональный пиксел (ср точка вне окружности)
            x -= 1
            delta -= 2 * x - 2  # диагонильный шаг
        delta += 2 * y + 3  # при вертикальном шаге
        tmirrored(dots, x + x_center, y + y_center, x_center, y_center, color)

    return dots


# Midpoint method ellipse
# построение происходит1 / 4 части эллипса. Необходимо найти точку, в которой меняется динамика приращений координат.
def midpellipse(x_center, y_center, frad, srad, color):
    dots = []
    x = 0
    y = srad
    # первая точка (0, b), вторая (1,b), средняя точка (1, b-0.5)
    delta = srad ** 2 - frad ** 2 * srad + 0.25 * frad * frad # Вычисление пробной функции для начальной точки
    dx = 2 * srad ** 2 * x
    dy = 2 * frad ** 2 * y

    while dx < dy:
        dmirrored(dots, x + x_center, y + y_center, x_center, y_center, color)

        x += 1
        dx += 2 * srad ** 2 # dx = dx + bd (bd = 2 * srad^2)

        if delta >= 0:
            y -= 1
            dy -= 2 * frad ** 2
            delta -= dy

        delta += dx + srad ** 2

    delta = srad ** 2 * (x + 0.5) ** 2 + frad ** 2 * (y - 1) ** 2 - frad ** 2 * srad ** 2  # Значение пробной функции для средней точки:

    while y >= 0:
        dmirrored(dots, x + x_center, y + y_center, x_center, y_center, color)

        y -= 1
        dy -= 2 * frad ** 2

        if delta <= 0:
            x += 1
            dx += 2 * srad ** 2
            delta += dx

        delta -= dy - frad ** 2

    return dots


# Parametric equation circle
# Для изменения угла выбирается шаг равный 1/R. Даннный шаг выбран потому, что расстояние между рисуемыми пикселями пропорционально углу между ними
# находятся только точки 1/8 части окружности, затем найденные точки отражаются по трем направлениям.
def parcircle(x_center, y_center, radius, color):
    dots = []
    step = 1 / radius

    for t in np.arange(0, pi / 4 + step, step):
        x = x_center + radius * cos(t)  # парам-е уравнение x = a * cos(t)
        y = y_center + radius * sin(t)  # парам-е уравнение x = b * sin(t)
        tmirrored(dots, x, y, x_center, y_center, color)

    return dots


# Parametric equation ellipse
# # Строим ¼ часть эллипса и проводим отражение. параметр t = 1 / R, где R - радиус больше полуоси
def parellipse(x_center, y_center, frad, srad, color):
    dots = []
    if frad > srad:  # выбираем больший радиус 
        step = 1 / frad
    else:
        step = 1 / srad

    for t in np.arange(0, pi / 2 + step, step):
        x = x_center + frad * cos(t)  # парам-е уравнение x = a * cos(t)
        y = y_center + srad * sin(t)  # парам-е уравнение x = b * sin(t)
        dmirrored(dots, x, y, x_center, y_center, color)

    return dots
