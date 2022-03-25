import tkinter as tk
from tkinter import colorchooser
import tkinter.messagebox as mb
from functions import funcs
from math import sin, cos, pi
from numpy import arange

def clear_all():
    clear_canvas()

def clear_canvas():
    canvas_root.delete('all')

def change_color():
    global color, color_btn
    color = colorchooser.askcolor(title="select color")[1]
    color_btn.configure(background=color)

def draw_section(xb, yb, xe, ye, color):
    canvas_root.create_line(xb, yb, xe, ye, fill=color)

def rotate_trans_matrix(rotate_matrix):
    global trans_matrix
    res_matrix = [[0 for i in range(4)] for i in range(4)]

    for i in range(4):
        for j in range(4):
            for k in range(4):
                res_matrix[i][j] += trans_matrix[i][k] * rotate_matrix[k][j]

    trans_matrix = res_matrix

def trans_point(point):
    # point = (x, y, z)
    point.append(1)  # (x, y, z, 1)
    res_point = [0, 0, 0, 0]
    for i in range(4):
        for j in range(4):
            res_point[i] += point[j] * trans_matrix[j][i]

    for i in range(3):
        res_point[i] *= sf  # x, y, z ==> SF * x, SF * y, SF * z

    res_point[0] += FIELD_WIDTH / 2
    res_point[1] += FIELD_HEIGHT / 2

    return res_point[:3]

def rotate_x():
    try:
        value = float(x_entry.get()) / 180 * pi
    except ValueError:
        tk.messagebox.showerror("Ошибка ввода", "Невозможно получить число. Проверьте корректность ввода.")
        return
    rotate_matrix = [[1, 0, 0, 0],
                     [0, cos(value), sin(value), 0],
                     [0, -sin(value), cos(value), 0],
                     [0, 0, 0, 1]]
    rotate_trans_matrix(rotate_matrix)
    solve()


def rotate_y():
    try:
        value = float(y_entry.get()) / 180 * pi
    except ValueError:
        tk.messagebox.showerror("Ошибка ввода", "Невозможно получить число. Проверьте корректность ввода.")
        return
    rotate_matrix = [[cos(value), 0, -sin(value), 0],
                     [0, 1, 0, 0],
                     [sin(value), 0, cos(value), 0],
                     [0, 0, 0, 1]]
    rotate_trans_matrix(rotate_matrix)
    solve()


def rotate_z():
    try:
        value = float(z_entry.get()) / 180 * pi
    except ValueError:
        tk.messagebox.showerror("Ошибка ввода", "Невозможно получить число. Проверьте корректность ввода.")
        return
    rotate_matrix = [[cos(value), sin(value), 0, 0],
                     [-sin(value), cos(value), 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]]
    rotate_trans_matrix(rotate_matrix)
    solve()


def set_sf():
    global sf
    try:
        sf = float(scale_entry.get())
    except ValueError:
        tk.messagebox.showerror("Ошибка ввода", "Невозможно получить число. Проверьте корректность ввода.")
        return
    solve()


def set_meta():
    global x_from, x_step, x_to, z_from, z_step, z_to
    try:
        x_from = float(xfrom_entry.get())
        x_to = float(xto_entry.get())
        x_step = float(xstep_entry.get())
        z_from = float(zfrom_entry.get())
        z_to = float(zto_entry.get())
        z_step = float(zstep_entry.get())
    except ValueError:
        tk.messagebox.showerror("Ошибка ввода", "Невозможно получить число. Проверьте корректность ввода.")
        return
    solve()


def draw_pixel(x, y):
    canvas_root.create_line(x, y, x + 1, y + 1, fill=color)


def is_visible(point):
    return 0 <= point[0] < FIELD_WIDTH and 0 <= point[1] < FIELD_HEIGHT # Флаг видимости в 1, если точка видима сверху/снизу от верхнего/нижнего горизонта в 0

def draw_point(x, y, hh, lh):
    if not is_visible([x, y]):
        return False

    if y > hh[x]:
        hh[x] = y
        draw_pixel(x, y)

    elif y < lh[x]:
        lh[x] = y
        draw_pixel(x, y)

    return True

def draw_horizon_part(p1, p2, hh, lh):
    if p1[0] > p2[0]:  # x2 > x1
        p1, p2 = p2, p1

    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    l = dx if dx > dy else dy
    dx /= l
    dy /= l

    x, y = p1[0], p1[1]

    for i in range(int(l) + 1):
        if not draw_point(int(round(x)), y, hh, lh):
            return
        x += dx
        y += dy


def draw_horizon(func, hh, lh, fr, to, step, z):
    f = lambda x: func(x, z)  # f = f(x, z=const)
    prev = None
    for x in arange(fr, to + step, step):
        current = trans_point([x, f(x), z])  # Повернуть, масштабировать и сдвинуть в центр экрана
        if prev:  # Если это не первая точка (то есть если есть предыдущая)
            draw_horizon_part(prev, current, hh, lh)
        prev = current # Запоминаем текущий конец как предыдущий


def solve():
    clear_canvas()
    f = funcs[func_var.get()]
    high_horizon = [0 for i in range(FIELD_WIDTH)]
    low_horizon = [FIELD_HEIGHT for i in range(FIELD_WIDTH)]

    for z in arange(z_from, z_to + z_step, z_step):  # Идём в сторону увеличения расстояния
        draw_horizon(f, high_horizon, low_horizon, x_from, x_to, x_step, z)

    for z in arange(z_from, z_to, z_step): 
        p1 = trans_point([x_from, f(x_from, z), z])
        p2 = trans_point([x_from, f(x_from, z + z_step), z + z_step])
        canvas_root.create_line(p1[0], p1[1], p2[0], p2[1], fill=color)
        p1 = trans_point([x_to, f(x_to, z), z])
        p2 = trans_point([x_to, f(x_to, z + z_step), z + z_step])
        canvas_root.create_line(p1[0], p1[1], p2[0], p2[1], fill=color)


##############################
background_color = 'light grey'
DEFAULT_COLOUR = "#000000"

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 780
FIELD_WIDTH = FIELD_HEIGHT = 740

color = DEFAULT_COLOUR

sf = 48
x_from = -10
x_to = 10
x_step = 0.1

z_from = -10
z_to = 10
z_step = 0.1

trans_matrix = [[int(i == j) for i in range(4)] for j in range(4)]

FUNCS = ["sin(x) * sin(z)", "sin(cos(x)) * sin(z)", "cos(x) * z / 3"]
###############################

root = tk.Tk()
mainmenu = tk.Menu(root)
root.title("Lab #10")
root.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))
root.resizable(False, False)
root.configure(background=background_color, menu=mainmenu)

canvas_root = tk.Canvas(root, height=FIELD_WIDTH, width=FIELD_HEIGHT, bg="white")  # Канвас для ввода точек
canvas_root.place(x=400, y=15)

root.bind("<Return>", lambda x: solve())

taskmenu = tk.Menu(mainmenu, tearoff=0)  # выпадающее меню с условием задачи
mainmenu.add_cascade(label="Алгоритм отсечения отрезка произвольным выпуклым отсекателем")

color_label = tk.Label(root, text="Цвет", font=('Lucida Console', '13', 'bold'), relief=tk.GROOVE,
                       background=background_color).place(x=30, y=15, width=310, height=30)
color_btn = tk.Button(root, relief=tk.GROOVE, command=change_color, background='black').place(x=30, y=43, width=310,
                                                                                              height=30)

func_label = tk.Label(root, text="Функция", font=('Lucida Console', '13', 'bold'), relief=tk.GROOVE,
                      background=background_color).place(x=30, y=90, width=310, height=30)
func_var = tk.IntVar()
func_var.set(0)
func_radios = list()
for i in range(len(FUNCS)):
    func_radios.append(
        tk.Radiobutton(root, text=FUNCS[i], relief=tk.GROOVE, background=background_color, variable=func_var,
                       value=i))

func_radios[0].place(x=30, y=120, width=310, height=30)
func_radios[1].place(x=30, y=150, width=310, height=30)
func_radios[2].place(x=30, y=180, width=310, height=30)

empty_label = tk.Label(root, text="", font=('Lucida Console', '13', 'bold'), relief=tk.GROOVE,
                       background=background_color).place(x=30, y=250, width=77.5, height=30)
from_label = tk.Label(root, text="От", font=('Lucida Console', '13', 'bold'), relief=tk.GROOVE,
                      background=background_color).place(x=107.5, y=250, width=77.5, height=30)
to_label = tk.Label(root, text="До", font=('Lucida Console', '13', 'bold'), relief=tk.GROOVE,
                    background=background_color).place(x=185, y=250, width=77.5, height=30)
step_label = tk.Label(root, text="Шаг", font=('Lucida Console', '13', 'bold'), relief=tk.GROOVE,
                      background=background_color).place(x=262.5, y=250, width=77.5, height=30)

xlabel = tk.Label(root, text="x", font=('Lucida Console', '13', 'bold'), relief=tk.GROOVE,
                  background=background_color).place(x=30, y=280, width=77.5, height=30)
xfrom_entry = tk.Entry(root, justify=tk.CENTER, font=('Lucida Console', '15'), relief=tk.GROOVE)
xfrom_entry.place(x=107.5, y=280, width=77.5, height=30)

xto_entry = tk.Entry(root, justify=tk.CENTER, font=('Lucida Console', '15'), relief=tk.GROOVE)
xto_entry.place(x=185, y=280, width=77.5, height=30)
xstep_entry = tk.Entry(root, justify=tk.CENTER, font=('Lucida Console', '15'), relief=tk.GROOVE)
xstep_entry.place(x=262.5, y=280, width=77.5, height=30)

zlabel = tk.Label(root, text="z", font=('Lucida Console', '13', 'bold'), relief=tk.GROOVE,
                  background=background_color).place(x=30, y=310, width=77.5, height=30)
zfrom_entry = tk.Entry(root, justify=tk.CENTER, font=('Lucida Console', '15'), relief=tk.GROOVE)
zfrom_entry.place(x=107.5, y=310, width=77.5, height=30)
zto_entry = tk.Entry(root, justify=tk.CENTER, font=('Lucida Console', '15'), relief=tk.GROOVE)
zto_entry.place(x=185, y=310, width=77.5, height=30)
zstep_entry = tk.Entry(root, justify=tk.CENTER, font=('Lucida Console', '15'), relief=tk.GROOVE)
zstep_entry.place(x=262.5, y=310, width=77.5, height=30)

confirm_btn = tk.Button(root, text="Применить", relief=tk.GROOVE, font=('Lucida Console', '13', 'bold'),
                        command=set_meta, background=background_color).place(x=30, y=340, width=310, height=30)

scale_label = tk.Label(root, text="Коэф-т\n   масштабирования", font=('Lucida Console', '10', 'bold'), relief=tk.GROOVE,
                       background=background_color).place(x=30, y=400, width=115, height=45)
scale_entry = tk.Entry(root, justify=tk.CENTER, font=('Lucida Console', '15'), relief=tk.GROOVE)
scale_entry.place(x=144, y=400, width=80, height=45)
scale_button = tk.Button(root, text="Изменить", font=('Lucida Console', '13', 'bold'), relief=tk.GROOVE,
                         background=background_color, command=set_sf).place(x=225, y=400, width=115, height=45)

x_label = tk.Label(root, text="x", font=('Lucida Console', '13', 'bold'), relief=tk.GROOVE,
                   background=background_color).place(x=30, y=445, width=115, height=30)
x_entry = tk.Entry(root, justify=tk.CENTER, font=('Lucida Console', '15'), relief=tk.GROOVE)
x_entry.place(x=144, y=445, width=80, height=30)

x_btn = tk.Button(root, text="Вращать", font=('Lucida Console', '13', 'bold'), relief=tk.GROOVE,
                  background=background_color, command=rotate_x).place(x=225, y=445, width=115, height=30)

y_label = tk.Label(root, text="y", font=('Lucida Console', '13', 'bold'), relief=tk.GROOVE,
                   background=background_color).place(x=30, y=475, width=115, height=30)
y_entry = tk.Entry(root, justify=tk.CENTER, font=('Lucida Console', '15'), relief=tk.GROOVE)
y_entry.place(x=144, y=475, width=80, height=30)
y_btn = tk.Button(root, text="Вращать", font=('Lucida Console', '13', 'bold'), relief=tk.GROOVE,
                  background=background_color, command=rotate_y).place(x=225, y=475, width=115, height=30)

z_label = tk.Label(root, text="z", font=('Lucida Console', '13', 'bold'), relief=tk.GROOVE,
                   background=background_color).place(x=30, y=505, width=115, height=30)
z_entry = tk.Entry(root, justify=tk.CENTER, font=('Lucida Console', '15'), relief=tk.GROOVE)
z_entry.place(x=144, y=505, width=80, height=30)
z_btn = tk.Button(root, text="Вращать", font=('Lucida Console', '13', 'bold'), relief=tk.GROOVE,
                  background=background_color, command=rotate_z).place(x=225, y=505, width=115, height=30)

res_btn = tk.Button(root, text="Нарисовать", font=('Lucida Console', '13', 'bold'), relief=tk.GROOVE,
                    background=background_color, command=solve).place(x=30, y=650, width=310, height=30)
clear_btn = tk.Button(root, text="Очистить поле", font=('Lucida Console', '13', 'bold'), relief=tk.GROOVE,
                      background=background_color, command=clear_all).place(x=30, y=690, width=310, height=30)
exit_btn = tk.Button(root, text="Выход", font=('Lucida Console', '13', 'bold'), relief=tk.GROOVE,
                     background=background_color, command=quit).place(x=30, y=730, width=310, height=30)

x_entry.insert(0, "20")
y_entry.insert(0, "20")
z_entry.insert(0, "20")
xfrom_entry.insert(0, str(x_from))
xto_entry.insert(0, str(x_to))
xstep_entry.insert(0, str(x_step))
zfrom_entry.insert(0, str(z_from))
zto_entry.insert(0, str(z_to))
zstep_entry.insert(0, str(z_step))
scale_entry.insert(0, str(sf))

root.mainloop()
