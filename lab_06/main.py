import time
import numpy as np
import tkinter as tk
from tkinter import colorchooser
import tkinter.messagebox as mb

class Point:
    def __init__(self, x=0, y=0, colour="#FFFFFF"):
        self.x = x
        self.y = y
        self.colour = colour

def draw_section(section):
    for p in section:
        img.put(p.colour, (p.x, p.y))

def put_point():
    try:
        p = Point(int(x_entry.get()), int(y_entry.get()))
    except ValueError:
        tk.messagebox.showerror("Ошибка ввода", "Невозможно получить число. Проверьте корректность ввода.")
        return
    left_click(p)

def add_pix():
    global flag_add
    flag_add = 1
    try:
        p = Point(int(x_entry_pix.get()), int(y_entry_pix.get()))
    except ValueError:
        tk.messagebox.showerror("Ошибка ввода", "Невозможно получить число. Проверьте корректность ввода.")
        return
    return_click(p)

def left_click(event):
    vertex_list.append(Point(event.x, event.y))
    if len(vertex_list) > 1:
        section = brezenham_int(draw_color, vertex_list[-2].x, vertex_list[-2].y,
                                vertex_list[-1].x, vertex_list[-1].y)
        draw_section(section)

def right_click(event):
    if len(vertex_list) > 2:
        section = brezenham_int(draw_color, vertex_list[-1].x, vertex_list[-1].y,
                                vertex_list[0].x, vertex_list[0].y)
        draw_section(section)
        vertex_list.clear()

def return_click(event):
    global start_pixel, flag_add, flag_pix
    flag_pix = 1
    if flag_add == 0:
        if start_pixel:
            img.put(CANVAS_COLOUR, (start_pixel[0], start_pixel[1]))
        start_pixel = [event.x, event.y]
        img.put(fill_color, (event.x, event.y))
    elif flag_add == 1:
        start_pixel = [event.x, event.y]
        img.put(CANVAS_COLOUR, (start_pixel[0], start_pixel[1]))
        img.put(fill_color, (event.x, event.y))

def brezenham_int(colour, xb, yb, xe, ye):
    section = list()
    x, y = xb, yb
    dx = xe - xb
    dy = ye - yb
    sx = int(np.sign(dx))
    sy = int(np.sign(dy))
    dx, dy = abs(dx), abs(dy)

    if dx > dy:
        change = 0
    else:
        change = 1
        dx, dy = dy, dx

    e = dy + dy - dx

    if not change:
        for i in range(dx):
            section.append(Point(x, y, colour))
            if e >= 0:
                y += sy
                e -= dx + dx
            x += sx
            e += dy + dy
    else:
        for i in range(dx):
            section.append(Point(x, y, colour))
            if e >= 0:
                x += sx
                e -= dx + dx
            y += sy
            e += dy + dy

    return section

def change_color(): # граница
    global draw_color
    draw_color = colorchooser.askcolor()
    draw_color = draw_color[1]
    btn_color.config(bg=draw_color)

def change_fill_color(): # цвет заливки
    global fill_color
    fill_color = colorchooser.askcolor()
    fill_color = fill_color[1]
    btn_color_fill.config(bg=fill_color)

def solve_time():
    start_time = time.time()
    solve()
    mb.showinfo("Время", f"Время построения: {time.time() - start_time : 8.7f}")

def clear_all():
    img.put("#FFFFFF", to=(0, 0, FIELD_WIDTH, FIELD_HEIGHT))

def solve():
    pause = mode.get()
    stack = [start_pixel]

    fill_area(stack, pause)

def get_color_tuple(color):
    return (int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16))

def fill_area(stack, pause):
    if flag_pix == 0:
        tk.messagebox.showerror("Ошибка ввода", "Установите затравочный пиксел внутри фигуры")
        return
    draw_tuple = get_color_tuple(draw_color) # цвет границы 
    fill_tuple = get_color_tuple(fill_color) # цвет внутренней облатси

    while stack: # Пока стек не пуст
        current_point = stack.pop() # Pop координат затравочного пиксела из стека.
        img.put(fill_color, current_point)

        x = current_point[0] + 1
        y = current_point[1] # Получение координат затравочного пиксела.

        while img.get(x, y) != draw_tuple and img.get(x, y) != fill_tuple: # Цикл пока цвет пиксела отличен от цвета грани.
            x += 1 # Движемся вправо.
        x_right  = x - 1  # Запомнили правую границу.
        img.put(fill_color, (current_point[0] + 1, y, x_right  + 1, y + 1))

        x = current_point[0] - 1 # заполняем интервал слева от затравки
        while img.get(x, y) != draw_tuple and img.get(x, y) != fill_tuple: # Цикл пока цвет пиксела отличен от цвета грани.
            x -= 1 # Движемся влево.
        x_left  = x + 1 # Запомнили левую границу.
        img.put(fill_color, (x_left , y, current_point[0], y + 1))

        for i in [1, -1]: # Переходим на строку выше в левую границу.
            x = x_left  
            y = current_point[1] + i 

            while x <= x_right : # Цикл до правой границы.
                flag = 0 # ищем затравку на строке выше
                while img.get(x, y) != draw_tuple and img.get(x, y) != fill_tuple and x <= x_right :   # Цикл пока цвет пиксела отличен от цвета грани и не дошли до правой границе (пока пиксел пуст.)
                    flag = 1 
                    x += 1 # Движемся вправо.

                if flag == 1: # помещаем в стек крайний справа пиксел
                    stack.append([x - 1, y])  # Заносим пиксел в стек.
                    flag = 0

                x_buff = x # Сохраняем текущий X.
                while (img.get(x, y) == draw_tuple or img.get(x, y) == fill_tuple) and x < x_right : # Пока встречены заполненные пикселы.
                    x += 1 # Движемся вправо.

                if x == x_buff: # Если X не изменился.
                    x += 1 # Сдвигаемся вправо.
        if pause:
            try:
                delay_time = float(delay_entry.get())
            except ValueError:
                tk.messagebox.showerror("Ошибка ввода", "Невозможно получить число. Проверьте корректность ввода.")
                return
            canvas_root.update() # Обновление изображения
            time.sleep(delay_time)

def dis_or_norm():
	if mode.get() == 0:
		delay_entry.configure(state="disable")
	else:
		delay_entry.configure(state="normal")

##############################
background_color = 'light grey'
DEFAULT_COLOUR = "#000000" 
CANVAS_COLOUR = "#FFFFFF"

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 780
FIELD_WIDTH = FIELD_HEIGHT = 740

MODES = ["Без задержки", "С задержкой"]
###############################
vertex_list = list()
draw_color = DEFAULT_COLOUR
fill_color = DEFAULT_COLOUR
flag_add = 0
start_pixel = None
flag_pix = 0

root = tk.Tk()
mainmenu = tk.Menu(root) 
root.title("Lab #6")
root.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))
root.resizable(False, False)
root.configure(background = background_color, menu = mainmenu)

canvas_root = tk.Canvas(root, height = FIELD_WIDTH, width = FIELD_HEIGHT, bg = "white") # Канвас для ввода точек
canvas_root.place(x = 400, y = 15)

canvas_root.bind("<Button-1>", left_click) # добавить точку
canvas_root.bind("<Button-2>", return_click) # поставить пиксел
root.bind("<Button-3>", right_click) # замкнуть

img = tk.PhotoImage(width=FIELD_WIDTH, height=FIELD_HEIGHT)
canvas_root.create_image((FIELD_WIDTH // 2, FIELD_HEIGHT // 2), image=img, state='normal') 
clear_all()

taskmenu = tk.Menu(mainmenu, tearoff=0) # выпадающее меню с условием задачи
mainmenu.add_cascade(label="Алгоритм построчного затравочного заполнения")

# -- Режим
mode_label = tk.Label(root, text = "Режим", font = ('Lucida Console', '15', 'bold'), background = background_color)
mode_label.place(x = 150, y = 25) # надпись выбор режим

mode = tk.IntVar()
mode.set(0)
mode_radios = list()
for i in range(len(MODES)):
    mode_radios.append(tk.Radiobutton(root, text=MODES[i], font = ('Lucida Console', '13'), value=i, variable=mode, padx=15, pady=10,background = background_color, command = dis_or_norm))

mode_radios[0].place(x = 30, y = 60)
mode_radios[1].place(x = 30, y = 115)

delay_entry = tk.Entry(root, justify = tk.CENTER, font = ('Lucida Console', '15'), background = "white") # для задержки
delay_entry.configure(state="disable")
delay_entry.place(x = 200, y = 120, width = 80, height = 30)

# -- Цвет
pick_color = tk.Label(root, text = "Цвет заполнения", font = ('Lucida Console', '13', 'bold'), background = background_color)
pick_color.place(x = 150, y = 155) # надпись цвет заполнения

btn_color_fill = tk.Button(root, relief=tk.GROOVE , command = change_fill_color, background = 'black')
btn_color_fill.place(x = 30, y = 195, width = 310, height = 30)

pick_color_line = tk.Label(root, text = "Цвет граней", font = ('Lucida Console', '13', 'bold'), background = background_color)
pick_color_line.place(x = 150, y = 235) # надпись цвет граней

btn_color = tk.Button(root, relief=tk.GROOVE , command = change_color, background = 'black')
btn_color.place(x = 30, y = 275, width = 310, height = 30)

# -- координаты точки
coord_dot_label = tk.Label(root, text = "Координаты точки", font = ('Lucida Console', '13', 'bold'), background = background_color)
coord_dot_label.place(x = 100, y = 320) # Координаты точки

x_label = tk.Label(root, text = "X", font = ('Lucida Console', '15'), background = background_color) # Лейбл xc
y_label = tk.Label(root, text = "Y", font = ('Lucida Console', '15'), background = background_color) # Лейбл yc

x_label.place(x = 90, y = 350)
y_label.place(x = 260, y = 350)

x_entry = tk.Entry(root, justify = tk.CENTER, font = ('Lucida Console', '15')) # для x
x_entry.place(x = 30, y = 380, width = 150, height = 30)

y_entry = tk.Entry(root, justify = tk.CENTER, font = ('Lucida Console', '15')) # для y
y_entry.place(x = 190, y = 380, width = 150, height = 30)

btn_add_dot = tk.Button(root, text = "Добавить точку",  font = ('Lucida Console', '11'), relief=tk.RAISED, command=put_point)
btn_add_dot.place(x = 30, y = 420, width = 310, height = 30)

coord_dot_label = tk.Label(root, text = "Координаты затравочного пиксела", font = ('Lucida Console', '13', 'bold'), background = background_color)
coord_dot_label.place(x = 30, y = 470) # Координаты точки

x_label = tk.Label(root, text = "X", font = ('Lucida Console', '15'), background = background_color) # Лейбл xc
y_label = tk.Label(root, text = "Y", font = ('Lucida Console', '15'), background = background_color) # Лейбл yc

x_label.place(x = 90, y = 500)
y_label.place(x = 260, y = 500)

x_entry_pix = tk.Entry(root, justify = tk.CENTER, font = ('Lucida Console', '15')) # для x
x_entry_pix.place(x = 30, y = 530, width = 150, height = 30)

y_entry_pix = tk.Entry(root, justify = tk.CENTER, font = ('Lucida Console', '15')) # для y
y_entry_pix.place(x = 190, y = 530, width = 150, height = 30)

btn_pixel_add = tk.Button(root, text = "Добавить точку затр пиксела",  font = ('Lucida Console', '11'), relief=tk.RAISED, command=add_pix)
btn_pixel_add.place(x = 30, y = 580, width = 310, height = 30)

#-- Кнопки выполнить закраску, замерить время, очистить экран, выход
btn_draw = tk.Button(root, text = "Выполнить закраску",  font = ('Lucida Console', '11'), relief=tk.RAISED, command=solve)
btn_draw.place(x = 30, y = 660, width = 310, height = 30)

btn_clear = tk.Button(root, text = "Очистить экран",  font = ('Lucida Console', '11'), relief=tk.RAISED, command=clear_all)
btn_clear.place(x = 30, y = 700, width = 310, height = 30)

btn_exit = tk.Button(root, text = "Замерить время",  font = ('Lucida Console', '11'), relief=tk.RAISED, command = solve_time)
btn_exit.place(x = 30, y = 740, width = 310, height = 30)

info_x = tk.Label(root, text = str(FIELD_WIDTH), font = ('Lucida Console', '8'), background = background_color) # Лейбл yc
info_x.place(x = 1150, y = 1)
info_x_0 = tk.Label(root, text = "0", font = ('Lucida Console', '8'), background = background_color) # Лейбл yc
info_x_0.place(x = 385, y = 1)
info_y = tk.Label(root, text = str(FIELD_HEIGHT), font = ('Lucida Console', '8'), background = background_color) # Лейбл yc
info_y.place(x = 1150, y = 750)

info_center = tk.Label(root, text = "Center: " + str(FIELD_HEIGHT / 2) + " : " + str(FIELD_HEIGHT / 2),relief=tk.GROOVE, font = ('Lucida Console', '8'), background = "light pink") # Лейбл yc
info_center.place(x = 100, y = 625)

root.mainloop()