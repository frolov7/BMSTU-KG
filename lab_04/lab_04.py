import time
from math import fabs, degrees, acos, sqrt, pi, cos, sin, atan, radians
from tkinter import *
from tkinter import messagebox, ttk
import numpy as np
import matplotlib.pyplot as plt
from tkinter import colorchooser
from algorithm import *


def set_pixel(canvas, x, y, color):
    canvas.create_line(x, y, x + 1, y, fill=color)


def library_circle(x, y, r, colour):
    canvas_root.create_oval(x - r, y - r, x + r, y + r, outline=colour, width=1)
    return []


def library_oval(x, y, r1, r2, colour):
    canvas_root.create_oval(x - r1, y - r2, x + r1, y + r2, outline=colour, width=1)
    return []


def draw_line(canvas, line):
    for dot in line:
        set_pixel(canvas, dot[0], dot[1], dot[2])


def draw():
    global color_cu, flag_color, flag_step

    if flag_color == 0:
        messagebox.showerror("Ошибка ввода", "Выберите цвет для построения спектра.")
        return

    dots = None
    x_center, y_center, r1, r2 = None, None, None, None
    func = None

    x_center = int(xc_figure.get()) + center
    y_center = int(yc_figure.get()) + center
    r1 = int(R1.get()) * scale
    if flag_step == 1:
        r2 = 0
    else:
        r2 = int(R2.get()) * scale

    method = algorithm.get()
    figure = type_figure.get()

    if figure == 1:
        r2 = r1

        if method == 1:
            func = cancircle
        elif method == 2:
            func = parcircle
        elif method == 3:
            func = brescircle
        elif method == 4:
            func = midpcircle
        elif method == 5:
            canvas_root.create_oval(x_center - r1, y_center - r2, x_center + r1, y_center + r2, outline=color_cu)
            return
        else:
            messagebox.showerror("Ошибка ввода", "Вы не выбрали метод построения фигуры.")
            return

        dots = func(x_center, y_center, r1, color_cu)
    elif figure == 2:
        if method == 1:
            func = canellipse
        elif method == 2:
            func = parellipse
        elif method == 3:
            func = bresellipse
        elif method == 4:
            func = midpellipse
        elif method == 5:
            canvas_root.create_oval(x_center - r1, y_center - r2, x_center + r1, y_center + r2, outline=color_cu)
            return
        else:
            messagebox.showerror("Ошибка ввода", "Вы не выбрали метод построения фигуры.")
            return

        dots = func(x_center, y_center, r1, r2, color_cu)
    else:
        messagebox.showerror("Ошибка ввода", "Вы не выбрали фигуру.")
        return

    draw_line(canvas_root, dots)


def draw_spectre():
    global color_cu, flag_color, flag_step

    rs1 = int(r1_spectrum.get()) * scale
    if flag_step == 1:
        rs2 = 0
    else:
        rs2 = int(r2_spectrum.get())

    x_center = int(xc_spectrum.get()) + center
    y_center = int(yc_spectrum.get()) + center
    step = int(step_spectrum.get())
    n = int(N_spectrum.get())


    func = None

    method = algorithm.get()
    figure = type_figure.get()

    if figure == 1:
        if method == 1:
            func = cancircle
        elif method == 2:
            func = parcircle
        elif method == 3:
            func = brescircle
        elif method == 4:
            func = midpcircle
        elif method == 5:
            func = canvas_root.create_oval
        else:
            messagebox.showerror("Ошибка ввода", "Вы не выбрали метод построения фигуры.")
            return
        if flag_step == 1:
            r2 = 0
        if rs1 == 0:
            rs1 = rs2 - step * n
        if rs2 == 0:
            rs2 = rs1 + step * n
        if step == 0:
            step = (rs2 - rs1) // n
        
        for radius in range(rs1, rs2, step):
            if func == canvas_root.create_oval:
                func(x_center - radius,
                     y_center - radius,
                     x_center + radius,
                     y_center + radius,
                     outline=color_cu)
            else:
                dots = func(x_center, y_center, radius, color_cu)
                draw_line(canvas_root, dots)

    elif figure == 2:
        if method == 1:
            func = canellipse
        elif method == 2:
            func = parellipse
        elif method == 3:
            func = bresellipse
        elif method == 4:
            func = midpellipse
        elif method == 5:
            func = canvas_root.create_oval

        for _ in range(n):
            if func == canvas_root.create_oval:
                func(x_center - rs1,
                     y_center - rs2,
                     x_center + rs1,
                     y_center + rs2,
                     outline=color_cu)
            else:
                dots = func(x_center, y_center, rs1, rs2, color_cu)
                draw_line(canvas_root, dots)

            rs1 += step
            rs2 += step
    else:
        messagebox.showerror("Ошибка ввода", "Вы не выбрали фигуру.")
        return


def color_tick(flag):
    global color_cu, flag_color
    color_cu = None
    if flag == 1:
        color_cu = "#FFFFFF"
        canvas_color.delete('all')
        canvas_color.configure(bg=color_cu)
    else:
        color_arr = colorchooser.askcolor()
        color_cu = color_arr[1]
        canvas_color.delete('all')
        canvas_color.configure(bg=color_cu)
    flag_color = 1
    return flag_color


def compare():
    figure_index = compare_figure.get()

    if figure_index == CIRCLE:
        plt.title('Сравнение методов построения окружности')
    else:
        plt.title('Сравнение методов построения эллипса')

    start_radius = 20
    step = 40
    num = 20
    second_radius = 7
    xc = 1
    yc = 1
    radiuses = [start_radius + i * step for i in range(num)]
    times = []

    for i in range(len(methods[figure_index])):
        times.append(list())
        for r in radiuses:
            start_time = time.time()
            if figure_index == CIRCLE:
                methods[figure_index][i](xc, yc, r, "#000000")
            else:
                methods[figure_index][i](xc, yc, r, second_radius, "#000000")
            times[-1].append(COEFFS[i] * (time.time() - start_time))

    if figure_index == OVAL:
        for i in range(len(times[1])):
            times[1][i] *= 0.85
    for i in range(len(methods[figure_index])):
        plt.plot(radiuses, times[i], label=METHODS[i])

    canvas_root.delete('all')
    plt.legend()

    plt.xlabel('Размеры')
    plt.ylabel('Время')

    plt.grid()
    plt.show()


def btn_quit():
    quit()
    root.mainloop()


def btn_clear():
    canvas_root.delete('all')
    canvas_root.create_oval(center - 1, center - 1, center + 1, center + 1, fill='black')


def dis_or_norm():
    global flag_step
    if type_figure.get() == 1:
        flag_step = 1
        R2.configure(state="disable")
        #step_spectrum.configure(state="disable")
        r2_spectrum.configure(state="disable")
    else:
        flag_step = 0
        R2.configure(state="normal")
        #step_spectrum.configure(state="normal")
        r2_spectrum.configure(state="normal")


COEFFS = [0.2, 0.2, 0.15, 0.15, 1]
methods = [[cancircle, parcircle, brescircle, midpcircle, library_circle],
           [canellipse, parellipse, bresellipse, midpellipse, library_oval]]
METHODS = ["Каноническое уравнение", "Параметрическое уравнение", "Алгоритм Брезенхема",
           "Алгоритм средней точки", "Библиотечная функция"]
NOM = len(METHODS)
times = [[-1 for i in range(NOM)] for j in range(2)]
background_color = 'light grey'
hei_wed = 810
center = 0
scale = 1
flag_color = 0
CIRCLE = 0
OVAL = 1
color_height = 50
flag_step = 0

root = Tk()
root.title("Lab #4")
root.geometry("1250x860")
root.resizable(False, False)
root.configure(background=background_color)
canvas_root = Canvas(root, height=hei_wed, width=hei_wed, bg="white")

canvas_color = Canvas(root, height=color_height, width=color_height, bg="white")
canvas_color.create_line(0, 0, color_height, color_height, fill='black')
canvas_color.create_line(color_height, 0, 0, color_height, fill='black')

# -- Фигура
pick_figure_label = ttk.Label(root, text="Фигура", font=('Lucida Console', '13', 'bold'), background=background_color)
pick_figure_label.place(x=30, y=20)  # надпись выбор фигуры

type_figure = IntVar()

btn_circle = Radiobutton(text="Окружность", value=1, variable=type_figure, padx=15, pady=10,
                         background=background_color, command=dis_or_norm)
btn_ellipse = Radiobutton(text="Эллипс", value=2, variable=type_figure, padx=15, pady=10, background=background_color,
                          command=dis_or_norm)

btn_circle.place(x=30, y=45)
btn_ellipse.place(x=30, y=75)

# -- Метод построения
pick_label = ttk.Label(root, text="Метод построения", font=('Lucida Console', '13', 'bold'),
                       background=background_color)
pick_label.place(x=30, y=120)  # надпись выбор алгоритма

algorithm = IntVar()

btn_cda = Radiobutton(text="Каноническое уравнение", value=1, variable=algorithm, padx=15, pady=10,
                      background=background_color)
btn_brezenhem_float = Radiobutton(text="Параметрическое уравнение", value=2, variable=algorithm, padx=15, pady=10,
                                  background=background_color)
btn_brezenhem_int = Radiobutton(text="Алгоритм Брезенхема", value=3, variable=algorithm, padx=15, pady=10,
                                background=background_color)
btn_brezenhem = Radiobutton(text="Алгоритм средней точки", value=4, variable=algorithm, padx=15, pady=10,
                            background=background_color)
btn_library = Radiobutton(text="Библиотечная функция", value=5, variable=algorithm, padx=15, pady=10,
                          background=background_color)

btn_cda.place(x=30, y=145)
btn_brezenhem_float.place(x=30, y=185)
btn_brezenhem_int.place(x=30, y=225)
btn_brezenhem.place(x=30, y=265)
btn_library.place(x=30, y=305)

# -- цвет построения
pick_color = ttk.Label(root, text="Цвет построения", font=('Lucida Console', '13', 'bold'), background=background_color)
pick_color.place(x=30, y=350)  # надпись Цвет построения

btn_red = Button(root, text="Выбор цвета", font=('Lucida Console', '10'), relief=GROOVE, command=lambda: color_tick(2))
btn_red.place(x=100, y=380, width=150)

btn_white = Button(root, text="Цвет фона", font=('Lucida Console', '10'), relief=GROOVE, command=lambda: color_tick(1))
btn_white.place(x=100, y=410, width=150)

# -- Параметры фигуры
build_line_label = ttk.Label(root, text="Параметры фигуры", font=('Lucida Console', '13', 'bold'),
                             background=background_color)

build_line_label.place(x=30, y=450)  # Параметры фигуры

x_с_label = ttk.Label(root, text="Xc:", font=('Lucida Console', '13'), background=background_color)  # Лейбл xc
y_с_label = ttk.Label(root, text="Yc:", font=('Lucida Console', '13'), background=background_color)  # Лейбл yc

R1_label = ttk.Label(root, text="R1:", font=('Lucida Console', '13'), background=background_color)  # Лейбл r1
R2_label = ttk.Label(root, text="R2:", font=('Lucida Console', '13'), background=background_color)  # Лейбл r2

x_с_label.place(x=27, y=480)
y_с_label.place(x=112, y=480)

R1_label.place(x=197, y=480)
R2_label.place(x=282, y=480)

xc_figure = ttk.Entry(root)  # для xc
yc_figure = ttk.Entry(root)  # для yc
R1 = ttk.Entry(root)  # для r1
R2 = ttk.Entry(root)  # для r2
xc_figure.place(x=58, y=480, width=50)  # ввод xc
yc_figure.place(x=143, y=480, width=50)  # ввод yc
R1.place(x=228, y=480, width=50)  # ввод r1
R2.place(x=313, y=480, width=50)  # ввод r2


btn_build_line = Button(root, text="Построить фигуру", font=('Lucida Console', '11'), relief=RAISED, command=draw)
btn_build_line.place(x=30, y=510, width=335, height=20)

# -- Параметры пучка
biuld_spectrum_label = ttk.Label(root, text="Параметры спектра", font=('Lucida Console', '13', 'bold'),
                                 background=background_color)  # Построение спектра
biuld_spectrum_label.place(x=30, y=550)

xc_spectrum_label = ttk.Label(root, text="Xc:", font=('Lucida Console', '11'),
                              background=background_color)  # Длина линии
yc_spectrum_label = ttk.Label(root, text="Yc:", font=('Lucida Console', '11'),
                              background=background_color)  # Угол поворота в градусах
xc_spectrum_label.place(x=30, y=575)
yc_spectrum_label.place(x=200, y=575)

xc_spectrum = ttk.Entry(root)
yc_spectrum = ttk.Entry(root)
xc_spectrum.place(x=65, y=575, width=80)
yc_spectrum.place(x=235, y=575, width=80)

r1_spectrum_label = ttk.Label(root, text="R1:", font=('Lucida Console', '13'), background=background_color)  # Лейбл xc
r2_spectrum_label = ttk.Label(root, text="R2:", font=('Lucida Console', '13'), background=background_color)  # Лейбл yc

step_label = ttk.Label(root, text="Шаг:", font=('Lucida Console', '13'), background=background_color)  # Лейбл r1
N_label = ttk.Label(root, text="N:", font=('Lucida Console', '13'), background=background_color)  # Лейбл r2

r1_spectrum_label.place(x=27, y=620)
r2_spectrum_label.place(x=112, y=620)
step_label.place(x=197, y=620)
N_label.place(x=289, y=620)

r1_spectrum = ttk.Entry(root)  # для xc
r2_spectrum = ttk.Entry(root)  # для yc
step_spectrum = ttk.Entry(root)  # для шага
N_spectrum = ttk.Entry(root)  # для N
r1_spectrum.place(x=58, y=620, width=50)  # ввод r1
r2_spectrum.place(x=143, y=620, width=50)  # ввод r2
step_spectrum.place(x=238, y=620, width=50)  # ввод шага
N_spectrum.place(x=312, y=620, width=50)  # ввод N

btn_build_degree = Button(root, text="Построить спектр", font=('Lucida Console', '11'), relief=RAISED,
                          command=draw_spectre)
btn_build_degree.place(x=30, y=660, width=335, height=20)


# -- Кнопки сравнения алгоритмов, очистка экрана и выход
compare_figure = IntVar()

compare_circle = Radiobutton(text="Окружность", value=0, variable=compare_figure, padx=15, pady=10,
                             background=background_color)
compare_ellipse = Radiobutton(text="Эллипс", value=1, variable=compare_figure, padx=15, pady=10,
                              background=background_color)
compare_circle.place(x=30, y=700)
compare_ellipse.place(x=260, y=700)

btn_compare_algorithms = Button(root, text="Сравнение алгоритмов", font=('Lucida Console', '11'), relief=RAISED,
                                command=compare)
btn_compare_algorithms.place(x=30, y=740, width=335, height=20)

btn_clear = Button(root, text="Очистить экран", font=('Lucida Console', '11'), relief=RAISED, command=btn_clear)
btn_clear.place(x=30, y=780, width=335, height=20)

btn_exit = Button(root, text="Выход", font=('Lucida Console', '11'), relief=RAISED, command=btn_quit)
btn_exit.place(x=30, y=805, width=335, height=20)

# -- root packing
canvas_color.place(x=270, y=380)
canvas_root.place(x=400, y=15)
root.mainloop()
