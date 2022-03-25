import time
from math import fabs, degrees, acos, sqrt, pi, cos, sin, atan, radians
from tkinter import *
from tkinter import messagebox, ttk
from algorithm import *
import numpy as np
import matplotlib.pyplot as plt
from tkinter import colorchooser

def layout():
    for i in range(0, hei_wed, 50):
        canvas_root.create_line(0, i+5, hei_wed, i+5, fill = '#d7d7d8')

    for i in range(0, hei_wed, 50):
        canvas_root.create_line(i+5, 0, i+5, hei_wed, fill = '#d7d7d8')

    for i in range(0, hei_wed, 50):
        canvas_root.create_text(i + 55, 10, text = str(i - 350))

    for i in range(0, hei_wed, 50):
        canvas_root.create_text(17, i + 55, text = str((i - 350) * -1)) 
    
    canvas_root.create_oval(center - 1, center - 1, center + 1, center + 1, fill = 'black')

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
    x = ["ЦДА","Брезенхем (float)","Брезенхем (int)","Брезенхем (сглаживание)","ВУ","Библиотечная функция"]
    y = [26, 16, 13, 40, 55, 16]
    color = ['red', 'blue', 'yellow', 'green', 'purple', 'pink']
    fig, ax = plt.subplots()
    
    for i in range(len(x)):
        ax.bar(x[i], y[i], color = color[i], width = 0.7)

    ax.set_title("Сравнение алгоритмов по времени")
    ax.set_facecolor('seashell')
    fig.set_facecolor('floralwhite')
    fig.set_figwidth(14)
    fig.set_figheight(8)
    plt.ylabel('Затраченное время, единицы времени')
    plt.show()

def btn_quit():
    quit()
    root.mainloop()

def btn_clear():
    canvas_root.delete('all')
    canvas_root.create_oval(center - 1, center - 1, center + 1, center + 1, fill = 'black')

def set_pixel(x, y, color):
    canvas_root.create_line(x, y, x+1, y, fill=color)

def draw_line(line):
    for dot in line:
        set_pixel(dot[0], dot[1], dot[2])

def draw():
    global color_cu, flag_color
    dots = None
    x1, x2, y1, y2 = None, None, None, None

    if flag_color == 0:
        messagebox.showerror("Ошибка ввода", "Выберите цвет для построения отрезка.")
        return
   
    try:
        x1 = (int(x_start.get()) * scale) + center
        y1 = -((int(y_start.get()) * scale)) + center
        x2 = (int(x_end.get()) * scale) + center 
        y2 = -((int(y_end.get()) * scale)) + center
    except ValueError:
        messagebox.showerror("Ошибка ввода", "Невозможно получить целое число. Проверьте корректность ввода.")
    
    print(x1, x2, y1, y2)
    if x1 == x2 and y1 == y2:
        messagebox.showerror("Ошибка ввода", "Не удалось построить прямую. Точки равны.")
        return
    method = algorithm.get()
    flag = 1
    
    if method == 1:
        dots = cda(x1, y1, x2, y2, color_cu)

    elif method == 2:
        dots = bres_float(float(x1), float(y1), float(x2), float(y2), color_cu)

    elif method == 3:
        dots = bres_int(x1, y1, x2, y2, color_cu)

    elif method == 4:
        dots = bres_smooth(x1, y1, x2, y2, color_cu)

    elif method == 5:
        dots = wu(x1, y1, x2, y2, color_cu)
        
    elif method == 6:
        flag = 0
        canvas_root.create_line(x1, y1, x2, y2, fill=color_cu)

    else:
        messagebox.showerror("Ошибка ввода", "Выберите алгоритм построения отрезка.")
        return
    
    if flag == 1:
        draw_line(dots)

def draw_bunch():
    global color_cu, flag_color
    if flag_color == 0:
        messagebox.showerror("Ошибка ввода", "Выберите цвет для построения спектра.")
        return
    
    try:
        radius = int(len_line.get())
        step = int(degree.get())
    except ValueError:
        messagebox.showerror("Ошибка ввода", "Невозможно получить число. Проверьте корректность ввода.")
        return

    lines = 360 // step

    x_start = center
    y_start = center - radius
    x_end = center
    y_end = center

    x_rotate = center
    y_rotate = center

    dots = [(x_start, y_start, x_end, y_end)]
    fixed_step = step

    for _ in range(1, lines):
        x_s = x_rotate + (y_start - y_rotate) * sin(radians(step))
        x_e = x_rotate + (y_end - y_rotate) * sin(radians(step))
        y_s = y_rotate + (y_start - y_rotate) * cos(radians(step))
        y_e = y_rotate + (y_end - y_rotate) * cos(radians(step))
        step += fixed_step

        dots.append((int(x_s), int(y_s), int(x_e), int(y_e)))
    
    method = algorithm.get()
    
    for pair in dots:
        if method == 1:
            dots = cda(pair[0], pair[1], pair[2], pair[3], color_cu)
            draw_line(dots)
        elif method == 2:
            dots = bres_float(float(pair[0]), float(pair[1]), float(pair[2]), float(pair[3]), color_cu)
            draw_line(dots)
        elif method == 3:
            dots = bres_int(pair[0], pair[1], pair[2], pair[3], color_cu)
            draw_line(dots)            
        elif method == 4:
            dots = bres_smooth(pair[0], pair[1], pair[2], pair[3], color_cu)
            draw_line(dots)            
        elif method == 5:
            dots = wu(pair[0], pair[1], pair[2], pair[3], color_cu)
            draw_line(dots)            
        elif method == 6:
            canvas_root.create_line(pair[0], pair[1], pair[2], pair[3], fill=color_cu)
        else:
            messagebox.showerror("Ошибка ввода", "Выберите алгоритм построения спектра.")
            return

background_color = 'light grey'
hei_wed = 810
center = 405
scale = 1
flag_color = 0
color_height = 50

root = Tk()
root.title("Lab #3")
root.geometry("1250x860")
root.resizable(False, False)
root.configure(background = background_color)
canvas_root = Canvas(root, height = hei_wed, width = hei_wed, bg = "white")

canvas_color = Canvas(root, height = color_height, width = color_height, bg = "white")
canvas_color.create_line(0, 0, color_height, color_height, fill = 'black')
canvas_color.create_line(color_height, 0, 0, color_height, fill = 'black')

# -- Метод построения
pick_label = ttk.Label(root, text = "Выбор алгоритма", font = ('Lucida Console', '13', 'bold'), background = background_color)
pick_label.place(x = 30, y = 20) # надпись выбор алгоритма

algorithm = IntVar()

btn_cda = Radiobutton(text="Цда", value=1, variable=algorithm, padx=15, pady=10,background = background_color)
btn_brezenhem_float = Radiobutton(text="Брезенхем (float)", value=2, variable=algorithm, padx=15, pady=10,background = background_color)
btn_brezenhem_int = Radiobutton(text="Брезенхем (int)", value=3, variable=algorithm, padx=15, pady=10,background = background_color)
btn_brezenhem = Radiobutton(text="Брезенхем сглаживание", value=4, variable=algorithm, padx=15, pady=10,background = background_color)
btn_by = Radiobutton(text="Ву", value=5, variable=algorithm, padx=15, pady=10,background = background_color)
btn_library = Radiobutton(text="Библиотечная функция", value=6, variable=algorithm, padx=15, pady=10,background = background_color)

btn_cda.place(x = 30, y = 45)
btn_brezenhem_float.place(x = 30, y = 75)
btn_brezenhem_int.place(x = 30, y = 105)
btn_brezenhem.place(x = 30, y = 135)
btn_by.place(x = 30, y = 165)
btn_library.place(x = 30, y = 195)

# -- цвет построения
pick_color = ttk.Label(root, text = "Цвет построения", font = ('Lucida Console', '13', 'bold'), background = background_color)
pick_color.place(x = 30, y = 240) # надпись Цвет построения

btn_red = Button(root, text = "Выбор цвета",  font = ('Lucida Console', '10'), relief=GROOVE , command = lambda: color_tick(2))
btn_red.place(x = 100, y = 270, width = 150)

btn_white = Button(root, text = "Цвет фона",  font = ('Lucida Console', '10'), relief=GROOVE , command = lambda: color_tick(1))
btn_white.place(x = 100, y =300, width = 150)

# -- Построение  отрезка
build_line_label = ttk.Label(root, text = "Построение отрезка", font = ('Lucida Console', '13', 'bold'), background = background_color)
start_line_label = ttk.Label(root, text = "Начало отрезка", font = ('Lucida Console', '10'), relief=RIDGE , background = background_color)
end_line_label = ttk.Label(root, text = "Конец отрезка", font = ('Lucida Console', '10'), relief=RIDGE , background = background_color)

build_line_label.place(x = 30, y = 350) # Построение отрезка
start_line_label.place(x = 60, y = 380) # Начало отрезка
end_line_label.place(x = 230, y = 380) # Конец отрезка

x_start_label = ttk.Label(root, text = "Xн:", font = ('Lucida Console', '13'), background = background_color) # Ввод икса для начала отрезка
y_start_label = ttk.Label(root, text = "Yн:", font = ('Lucida Console', '13'), background = background_color) # Ввод игрика для начала отрезка

x_end_label = ttk.Label(root, text = "Xк:", font = ('Lucida Console', '13'), background = background_color) # Ввод игрика для конца отрезкак
y_end_label = ttk.Label(root, text = "Yк:", font = ('Lucida Console', '13'), background = background_color)# Ввод игрика для конца отрезкак

x_start_label.place(x = 27, y = 410)
y_start_label.place(x = 112, y = 410)

x_end_label.place(x = 197, y = 410)
y_end_label.place(x = 282, y = 410)

x_start = ttk.Entry(root) # для x начало отрезка
y_start = ttk.Entry(root) # для y начало отрезка

x_end = ttk.Entry(root) # для x конец отрезка
y_end = ttk.Entry(root) # для y конец отрезка

x_start.place(x = 58, y = 410, width = 50) # ввод x
y_start.place(x = 143, y = 410, width = 50) # ввод y

x_end.place(x = 228, y = 410, width = 50) # ввод x
y_end.place(x = 313, y = 410, width = 50) # ввод y
'''
x_start.insert(0, int(1))
y_start.insert(0, int(2))
x_end.insert(0, int(3))
y_end.insert(0, int(4))
'''
btn_build_line = Button(root, text = "Нарисовать линию",  font = ('Lucida Console', '11'), relief=RAISED, command = draw)
btn_build_line.place(x = 30, y = 450, width = 335, height = 20)

# -- Параметры пучка
biuld_spectrum_label = ttk.Label(root, text = "Параметры спектра", font = ('Lucida Console', '13', 'bold'), background = background_color) # Построение спектра
biuld_spectrum_label.place(x = 30, y = 495)

radius_label = ttk.Label(root, text = "Шаг,°", font = ('Lucida Console', '11'), background = background_color) # Длина линии
degreee_label = ttk.Label(root, text = "Радиус", font = ('Lucida Console', '11'), background = background_color) # Угол поворота в градусах

degreee_label.place(x = 180, y = 525)
radius_label.place(x = 30, y = 525)

degree = ttk.Entry(root) # Угол поворота в градусах
len_line = ttk.Entry(root) # Длина линии ввод
degree.place(x = 90, y = 525, width = 80)
len_line.place(x = 245, y = 525, width = 80)

btn_build_degree = Button(root, text = "Построить спектр",  font = ('Lucida Console', '11'), relief=RAISED, command = draw_bunch)
btn_build_degree.place(x = 30, y = 555,width = 335, height = 20)
'''
degree.insert(0, int(20))
len_line.insert(0, int(250))
'''
#-- Кнопки сравнения алгоритмов, очистка экрана и выход
btn_compare_algorithms = Button(root, text = "Сравнение алгоритмов",  font = ('Lucida Console', '11'), relief=RAISED, command = compare)
btn_compare_algorithms.place(x = 30, y = 620, width = 335, height = 20)

btn_clear = Button(root, text = "Очистить экран",  font = ('Lucida Console', '11'), relief=RAISED, command = btn_clear)
btn_clear.place(x = 30, y = 645, width = 335, height = 20)

btn_exit = Button(root, text = "Выход",  font = ('Lucida Console', '11'), relief=RAISED, command = btn_quit)
btn_exit.place(x = 30, y = 700, width = 335, height = 20)

#-- root packing
canvas_color.place(x = 270, y = 270)
canvas_root.place(x = 400, y = 15)
#layout()
root.mainloop()