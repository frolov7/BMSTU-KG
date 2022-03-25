import copy
import traceback
from math import fabs, degrees, acos, sqrt, pi, cos, sin, atan
from tkinter import messagebox, ttk

# Алгоритм ЦДА
def cda(x_start, y_start, x_end, y_end, color):
    dx = x_end - x_start
    dy = y_end - y_start

    if abs(dx) > abs(dy):
        l = abs(dx) 
    else: 
        l = abs(dy)
    
    dx /= l
    dy /= l

    x = x_start
    y = y_start

    dots = [[x, y, color]]

    for _ in range(l):
        x += dx
        y += dy
        dots.extend([[x, y, color]])

    return dots

# Алгоритм Брезенхема с int 
def bres_int(x_start, y_start, x_end, y_end, color):
    dx = x_end - x_start
    dy = y_end - y_start

    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0

    e = 2*dy - dx
    y = 0

    dots = []

    for x in range(dx + 1):
        dots.extend([[x_start + x*xx + y*yx, y_start + x*xy + y*yy, color]])
        if e >= 0:
            y += 1
            e -= 2*dx
        e += 2*dy

    return dots

# Алгоритм брезенхема с float
def bres_float(x_start, y_start, x_end, y_end, color):
    dx = x_end - x_start
    dy = y_end - y_start

    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0

    m = dy / dx
    e = m - 0.5
    y = 0

    dots = []

    for x in range(int(dx) + 1):
        dots.extend([[x_start + x*xx + y*yx, y_start + x*xy + y*yy, color]])
        if e >= 0:
            y += 1
            e -= 1
        e += m

    return dots

# Алгоритм брезенхема сглаживание
def bres_smooth(x_start, y_start, x_end, y_end, color):
    dx = x_end - x_start
    dy = y_end - y_start

    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0

    m = dy / dx
    e = 0.5
    w = 1
    y = 0

    dots = []

    for x in range(dx + 1):
        dots.extend([[x_start + x*xx + y*yx, y_start + x*xy + y*yy, color]])
        if e >= w - m:
            y += 1
            e -= w
        e += m

    return dots

def fpart(x):
    return x - int(x)

def rfpart(x):
    return 1 - fpart(x)

# Алгоритм ВУ
def wu(x_start, y_start, x_end, y_end, color):
    dx = x_end - x_start
    dy = y_end - y_start

    steep = abs(dx) < abs(dy)

    def p(px, py):
        return ([px, py], [py, px])[steep]

    if steep:
        x_start, y_start, x_end, y_end, dx, dy = y_start, x_start, y_end, x_end, dy, dx
    if x_end < x_start:
        x_start, x_end, y_start, y_end = x_end, x_start, y_end, y_start

    m = dy / dx
    intery = y_start + rfpart(x_start) * m

    dots = []

    def get_endpoint(x_s, y_s):
        x_e = round(x_s)
        y_e = y_s + (x_e - x_s) * m
        x_gap = rfpart(x_s + 0.5)

        px, py = int(x_e), int(y_e)

        dens1 = rfpart(y_e) * x_gap
        dens2 = fpart(y_e) * x_gap

        dots.extend([[*p(px, py), color]])
        dots.extend([[*p(px, py), color]])

        return px

    x_s = get_endpoint(x_start, y_start) + 1
    x_e = get_endpoint(x_end, y_end)

    for x in range(x_s, x_e):
        y = int(intery)

        dens1 = rfpart(intery)
        dens2 = fpart(intery)

        dots.extend([[*p(x, y), color]])
        dots.extend([[*p(x, y+1), color]])

        intery += m

    return dots