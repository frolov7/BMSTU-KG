import time
import tkinter as tk
from tkinter import colorchooser
import tkinter.messagebox as mb

def clear_all():
    clear_canvas() 
    rect[LEFT] = None
    left_corner[0] = None
    sections.clear()
    last_point[0] = None

def erase_inside():
    canvas_root.create_rectangle(rect[LEFT], rect[TOP], rect[RIGHT], rect[BOTTOM], fill=CANVAS_COLOUR, outline=rect_color)

def clear_canvas():
    canvas_root.delete('all')

def left_click(event):
    if last_point[0]:
        sections.append([last_point[:], [event.x, event.y]])
        draw_section(*sections[-1][0], *sections[-1][1], sect_color)
        last_point[0] = None
    else:
        last_point[0], last_point[1] = event.x, event.y

def return_click(event):
    erase_inside()
    solve()

def right_click(event):
    if not left_corner[0]:
        left_corner[0], left_corner[1] = event.x, event.y
    else:
        new_rect(left_corner[0], event.y, event.x, left_corner[1])

def draw_rect():
    canvas_root.create_line(rect[LEFT], rect[TOP], rect[RIGHT], rect[TOP], fill=rect_color)
    canvas_root.create_line(rect[RIGHT], rect[TOP], rect[RIGHT], rect[BOTTOM], fill=rect_color)
    canvas_root.create_line(rect[RIGHT], rect[BOTTOM], rect[LEFT], rect[BOTTOM], fill=rect_color)
    canvas_root.create_line(rect[LEFT], rect[BOTTOM], rect[LEFT], rect[TOP], fill=rect_color)

def draw_section(xb, yb, xe, ye, color):
    canvas_root.create_line(xb, yb, xe, ye, fill=color)

def new_rect(left, top, right, bottom):
    rect[LEFT] = left
    rect[TOP] = top
    rect[RIGHT] = right
    rect[BOTTOM] = bottom

    clear_canvas()
    draw_rect()
    sections.clear()
    left_corner[0] = None
    last_point[0] = None

def read_rect():
    new_rect(int(rect_left_entry.get()), int(rect_up_entry.get()),
             int(rect_right_entry.get()), int(rect_down_entry.get()))

def read_vertex():
    if last_point[0]:
        sections.append([last_point[:], [int(x_entry.get()), int(y_entry.get())]])
        draw_section(*sections[-1][0], *sections[-1][1], sect_color)
        last_point[0] = None
    else:
        last_point[0], last_point[1] = int(x_entry.get()), int(y_entry.get())

def change_rect_color(): # Цвет регулярного отсекателя
    global rect_color
    rect_color = colorchooser.askcolor(title="select color")[1]
    btn_reg_cut.configure(background=rect_color)

def change_sect_color(): # Цвет отрезка
    global sect_color 
    sect_color = colorchooser.askcolor(title="select color")[1]
    btn_color_line.configure(background=sect_color)

def change_res_color(): # Результата
    global res_color
    res_color = colorchooser.askcolor(title="select color")[1]
    btn_color_result.configure(background=res_color)

def solve():
    for section in sections:
        cut_section(rect, section)

# Маски для установления битов в 4битовом коде
#T1 = 1 если точка лежит левее окна и 0 в противном случае
#T2 = 1 если точка лежит правее окна и 0 в противном случае
#T3 = 1 если точка лежит ниже окна и 0 в противном случае
#T4 = 1 если точка лежит выше окна и 0 в противном случае
MASK_LEFT =   0b0001
MASK_RIGHT =  0b0010
MASK_BOTTOM = 0b0100
MASK_TOP =    0b1000

# Функция установления битов. Если нужно установить бит то 
# происходит битовая дизьюнкция и бит становится единичным
def set_bits(point, rect_sides):
    bits = 0b0000 # Изначально все биты сброшены
    if point[0] < rect_sides[LEFT]:
        bits += MASK_LEFT
    if point[0] > rect_sides[RIGHT]:
        bits += MASK_RIGHT
    if point[1] < rect_sides[BOTTOM]:
        bits += MASK_BOTTOM
    if point[1] > rect_sides[TOP]:
        bits += MASK_TOP
    return bits

# Нахождение границы отсечения отрезка в случае вертикального расположения
# arr_p – массив из 2 точек вершины отрезка
# index – 0/1 – индекс рассматриваемой вершины
# rect – массив из 4 элементов, содержащий границы окна
def find_vertical(arr_p, index, rect):
    if arr_p[index][1] > rect[TOP]:# если вершина выше верхней границы отсекателя
        return [arr_p[index][0], rect[TOP]]  #то верхняя часть (пересечения с верхней границей отсекателя) отсекается
    elif arr_p[index][1] < rect[BOTTOM]: # относительно нижней границы
        return [arr_p[index][0], rect[BOTTOM]]
    else: #  рассматриваемая вершина внутри границ, оставляем, как есть
        return arr_p[index]

# rect – Массив из 4 элементов, являющихся границами окна 
# arr_p – массив из 2 точек – вершины отрезка
def cut_section(rect, arr_p):
    # Выставляем биты в коде (находим положение точек относительно окна)
    s = list()
    for i in range(2):
        s.append(set_bits(arr_p[i], rect)) # s[0] – для 1ой точки, s[1] – для 2ой

    if s[0] == 0 and s[1] == 0: # Полностью видимый отрезок, то есть обе точки внутри границ
        draw_section(arr_p[0][0], arr_p[0][1], arr_p[1][0], arr_p[1][1], res_color) # рисуем отрезок целиком и выходим из функции. 
        return
    
    if s[0] == 1 and s[1] == 1: # Если полностью невидимый отрезок
        return

    cur_index = 0 # индекс текущей обрабатываемой вершины
    res = list() # массив для записи вершин,получающихся после отсечения.

    if s[0] == 0: # Проверка, нет ли одной точки внутри отсекателя c индексом 0
        cur_index = 1 # ставим ее на первое место и работаем с другой
        res.append(arr_p[0])
    # смена мест нужна, чтобы в начале была обработанная точка, а за ней - нет
    elif s[1] == 0: # c индексом 1
        res.append(arr_p[1])
        cur_index = 1 # ставим ее на первое место и работаем с другой

        arr_p.reverse() # Вторая вершина уже внутри области, поменяем местами вершины, чтобы работать с необработанной
        s.reverse() # на 2 месте


    # cur_index – индекс рассматриваемой точки 0 или 1 => идем до 2х
    while cur_index < 2:
        if arr_p[0][0] == arr_p[1][0]: # х совпадают
            res.append(find_vertical(arr_p, cur_index, rect)) # то прямая вертикальная
            cur_index += 1
            continue

        m = (arr_p[1][1] - arr_p[0][1]) / (arr_p[1][0] - arr_p[0][0])# Нахождение наклона прямой

        # Если логическое И кодов конечных точек не равно 0, то отрезок целиком вне окна
        if s[cur_index] & MASK_LEFT: # если вершина находится левее границы (находим пересечение с левой границей)
            y = round(m * (rect[LEFT] - arr_p[cur_index][0]) + arr_p[cur_index][1]) # уравнение бесконечной прямой через две точки
            if y <= rect[TOP] and y >= rect[BOTTOM]:  # Проверяем: если произошло пересечение 
                res.append([rect[LEFT], y]) # с границей окна, то отсекаем 
                cur_index += 1 # и переходим к рассмотрению след вершины
                continue # анализируем дальше.

        # Нахождение пересечения с правой границей 
        elif s[cur_index] & MASK_RIGHT:
            y = round(m * (rect[RIGHT] - arr_p[cur_index][0]) + arr_p[cur_index][1])
            if y <= rect[TOP] and y >= rect[BOTTOM]:
                res.append([rect[RIGHT], y])
                cur_index += 1
                continue

        if m == 0: # Если прямая горизонтальна
            cur_index += 1 # пересечения с верхней и нижней границей быть не может
            continue

        if s[cur_index] & MASK_TOP: # Нахождение пересечений с верхней границей
            x = round((rect[TOP] - arr_p[cur_index][1]) / m + arr_p[cur_index][0]) 
            if x <= rect[RIGHT] and x >= rect[LEFT]: # Проверка: пересечение с границей окна или же с продолжением 
                res.append([x, rect[TOP]])
                cur_index += 1
                continue

        elif s[cur_index] & MASK_BOTTOM: # Нахождение пересечений с нижней границей
            x = round((rect[BOTTOM] - arr_p[cur_index][1]) / m + arr_p[cur_index][0])
            if x <= rect[RIGHT] and x >= rect[LEFT]:
                res.append([x, rect[BOTTOM]])
                cur_index += 1
                continue

        cur_index += 1

    if res: # Если отсеченный отрезок найден (изначальный отрезок не являлся полностью невидимым)
        draw_section(res[0][0], res[0][1], res[1][0], res[1][1], res_color)# чертим его

##############################
background_color = 'light grey'
DEFAULT_COLOUR = "#000000" 
CANVAS_COLOUR = "#FFFFFF"

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 780
FIELD_WIDTH = FIELD_HEIGHT = 740

LEFT = 0
RIGHT = 1
TOP = 2
BOTTOM = 3

rect_color = DEFAULT_COLOUR
sect_color = DEFAULT_COLOUR
res_color = DEFAULT_COLOUR
left_corner = [None, None]
rect = [None, None, None, None]
sections = []
last_point = [None, None]
###############################

root = tk.Tk()
mainmenu = tk.Menu(root) 
root.title("Lab #6")
root.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))
root.resizable(False, False)
root.configure(background = background_color, menu = mainmenu)

canvas_root = tk.Canvas(root, height = FIELD_WIDTH, width = FIELD_HEIGHT, bg = "white") # Канвас для ввода точек
canvas_root.place(x = 400, y = 15)

canvas_root.bind("<Button-1>", left_click) # добавить точку
root.bind("<Return>", return_click)
canvas_root.bind("<Button-3>", right_click)


taskmenu = tk.Menu(mainmenu, tearoff=0) # выпадающее меню с условием задачи
mainmenu.add_cascade(label="Алгоритм отсечения отрезка регулярным отсекателем")

# -- Цвет
pick_color_cut = tk.Label(root, text = "Цвет регулярного отсекателя", font = ('Lucida Console', '13', 'bold'), relief = tk.GROOVE, background = background_color)
pick_color_cut.place(x = 30, y = 33, width=310, height=30) # надпись Цвет ругулярного отсекателя

btn_reg_cut = tk.Button(root, relief=tk.GROOVE, command = change_rect_color, background = 'black')
btn_reg_cut.place(x = 30, y = 60, width = 310, height = 30)

pick_color_line = tk.Label(root, text = "Цвет отрезков", font = ('Lucida Console', '13', 'bold'), relief = tk.GROOVE, background = background_color)
pick_color_line.place(x = 30, y = 93, width=310, height=30) # надпись цвет отрезков

btn_color_line = tk.Button(root, relief=tk.GROOVE, command = change_sect_color, background = 'black')
btn_color_line.place(x = 30, y = 120, width = 310, height = 30)

pick_color_result = tk.Label(root, text = "Цвет результата", font = ('Lucida Console', '13', 'bold'), relief = tk.GROOVE, background = background_color)
pick_color_result.place(x = 30, y = 153, width=310, height=30) # надпись цвет результата

btn_color_result = tk.Button(root, relief=tk.GROOVE, command = change_res_color, background = 'black')
btn_color_result.place(x = 30, y = 180, width = 310, height = 30)

# -- координаты точки
coord_cut_label = tk.Label(root, text = "Ввод границ отсекателя", font = ('Lucida Console', '13', 'bold'), relief = tk.GROOVE, background = background_color)
coord_cut_label.place(x = 30, y = 260, width = 310, height = 30) # Координаты точки

left_label = tk.Label(root, text = "Левая", font = ('Lucida Console', '13'), relief = tk.GROOVE, background = background_color).place(x = 30, y = 290, width = 155, height = 30) # Лейбл xc
right_label = tk.Label(root, text = "Правая", font = ('Lucida Console', '13'), relief=tk.GROOVE, background = background_color).place(x = 185, y = 290, width = 155, height = 30) # Лейбл yc

rect_left_entry = tk.Entry(root, justify = tk.CENTER, font = ('Lucida Console', '15'), relief = tk.GROOVE,) # для x
rect_left_entry.place(x = 30, y = 320, width = 155, height = 30)

rect_right_entry = tk.Entry(root, justify = tk.CENTER, font = ('Lucida Console', '15'), relief = tk.GROOVE,) # для y
rect_right_entry.place(x = 185, y = 320, width = 155, height = 30)


upper_label = tk.Label(root, text = "Верхняя", font = ('Lucida Console', '13'), relief = tk.GROOVE, background = background_color).place(x = 30, y = 350, width = 155, height = 30) # Лейбл xc
lower_label = tk.Label(root, text = "Нижняя", font = ('Lucida Console', '13'), relief=tk.GROOVE, background = background_color).place(x = 185, y = 350, width = 155, height = 30) # Лейбл yc

rect_up_entry = tk.Entry(root, justify = tk.CENTER, font = ('Lucida Console', '15'), relief = tk.GROOVE,) # для x
rect_up_entry.place(x = 30, y = 380, width = 155, height = 30)

rect_down_entry = tk.Entry(root, justify = tk.CENTER, font = ('Lucida Console', '15'), relief = tk.GROOVE,) # для y
rect_down_entry.place(x = 185, y = 380, width = 155, height = 30)

btn_input_rect = tk.Button(root, text = "Применить", font = ('Lucida Console', '13', 'bold'), relief = tk.GROOVE, background = background_color, command = read_rect)
btn_input_rect.place(x = 30, y = 410.5, width = 310, height = 30) # Координаты точки


input_lowels_label = tk.Label(root, text = "Ввод вершины", font = ('Lucida Console', '13', 'bold'), relief = tk.GROOVE, background = background_color)
input_lowels_label.place(x = 30, y = 480, width = 310, height = 30) # Координаты точки

x_label = tk.Label(root, text = "x", font = ('Lucida Console', '13'), relief = tk.GROOVE, background = background_color).place(x = 30, y = 510, width = 77.5, height = 30) # Лейбл xc
y_label = tk.Label(root, text = "y", font = ('Lucida Console', '13'), relief=tk.GROOVE, background = background_color).place(x = 185, y = 510, width = 77.5, height = 30) # Лейбл yc

x_entry = tk.Entry(root, justify = tk.CENTER, font = ('Lucida Console', '15'), relief = tk.GROOVE,) # для x
x_entry.place(x = 107, y = 510, width = 77.5, height = 30)

y_entry = tk.Entry(root, justify = tk.CENTER, font = ('Lucida Console', '15'), relief = tk.GROOVE,) # для y
y_entry.place(x = 262, y = 510, width = 77.5, height = 30)

btn_input_vertex = tk.Button(root, text = "Применить", font = ('Lucida Console', '13', 'bold'), relief = tk.GROOVE, background = background_color, command = read_vertex)
btn_input_vertex.place(x = 30, y = 540.5, width = 310, height = 30) # Координаты точки
#-- Кнопки выполнить закраску, замерить время, очистить экран, выход

btn_clear = tk.Button(root, text = "Отсечь",  font = ('Lucida Console', '11'), relief=tk.RAISED, command=solve)
btn_clear.place(x = 30, y = 620, width = 310, height = 30)

btn_clear = tk.Button(root, text = "Очистить экран",  font = ('Lucida Console', '11'), relief=tk.RAISED, command=clear_all)
btn_clear.place(x = 30, y = 660, width = 310, height = 30)

btn_exit = tk.Button(root, text = "Выход",  font = ('Lucida Console', '11'), relief=tk.RAISED, command = quit)
btn_exit.place(x = 30, y = 700, width = 310, height = 30)

info_x = tk.Label(root, text = str(FIELD_WIDTH), font = ('Lucida Console', '8'), background = background_color) # Лейбл yc
info_x.place(x = 1150, y = 1)
info_x_0 = tk.Label(root, text = "0", font = ('Lucida Console', '8'), background = background_color) # Лейбл yc
info_x_0.place(x = 385, y = 1)
info_y = tk.Label(root, text = str(FIELD_HEIGHT), font = ('Lucida Console', '8'), background = background_color) # Лейбл yc
info_y.place(x = 1150, y = 750)
info_center = tk.Label(root, text = "Center: " + str(FIELD_HEIGHT / 2) + " : " + str(FIELD_HEIGHT / 2),relief=tk.GROOVE, font = ('Lucida Console', '8'), background = "light pink") # Лейбл yc
info_center.place(x = 100, y = 585)

root.mainloop()