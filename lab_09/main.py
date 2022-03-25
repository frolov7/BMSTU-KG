import time
import tkinter as tk
from tkinter import colorchooser
import tkinter.messagebox as mb

def clear_all():
    clear_canvas() 
    sections.clear()
    verteces_list.clear()
    figure_list.clear()

def clear_canvas():
    canvas_root.delete('all')

def left_click(event):
    figure_list.append([event.x, event.y])
    if len(figure_list) >= 2:
        draw_section(*figure_list[-1], *figure_list[-2], sect_color)
    
def return_click(event):
    if len(verteces_list) < 3:
        return
    draw_section(*verteces_list[-1], *verteces_list[0], cutter_color)

def c_click(event):
    if len(figure_list) < 3:
        return
    draw_section(*figure_list[-1], *figure_list[0], sect_color)

def right_click(event):
    verteces_list.append([event.x, event.y])
    if len(verteces_list) >= 2:
        draw_section(*verteces_list[-1], *verteces_list[-2], cutter_color)

def read_cutter_vertex():
    try:
        x = int(cutter_x_entry.get())
        y = int(cutter_y_entry.get())
    except:
        mb.showerror("Неверный ввод", "Не удалось считать коориданаты очередной вершины (учтите, что при работе с растром \nкоориданаты должны быть целыми)")
    verteces_list.append([x, y])
    if len(verteces_list) >= 2:
        draw_section(*verteces_list[-1], *verteces_list[-2], cutter_color)

def read_vertex():
    try:
        x = int(x_entry.get())
        y = int(y_entry.get())
    except:
        mb.showerror("Неверный ввод", "Не удалось считать коориданаты очередной вершины (учтите, что при работе с растром \nкоориданаты должны быть целыми)")
    figure_list.append([x, y])
    if len(figure_list) >= 2:
        draw_section(*figure_list[-1], *figure_list[-2], sect_color)

def change_cutter_color():
    global cutter_color
    cutter_color = colorchooser.askcolor(title="select color")[1]
    cutter_color_btn.configure(background=cutter_color)

def change_sect_color():
    global sect_color
    sect_color = colorchooser.askcolor(title="select color")[1]
    sect_color_btn.configure(background=sect_color)

def change_res_color():
    global res_color
    res_color = colorchooser.askcolor(title="select color")[1]
    res_color_btn.configure(background=res_color)

def get_vect(p1, p2):
    return [p2[0] - p1[0], p2[1] - p1[1]]

def draw_section(xb, yb, xe, ye, color):
    canvas_root.create_line(xb, yb, xe, ye, fill=CANVAS_COLOUR, width=2)
    canvas_root.create_line(xb, yb, xe, ye, fill=color)

# Функция, которая удаляет ложные ребра
def make_uniq(sections):
    for section in sections:
        section.sort()
    return list(filter(lambda x: (sections.count(x) % 2) == 1, sections))

# Функция проверки, принадлежит ли точка point отрезку section
def point_in_section(point, section):
    if abs(vect_mul(get_vect(point, section[0]), get_vect(*section))) <= 1e-6:
        if (section[0] < point < section[1] or section[1] < point < section[0]):
            return True
    return False

# Функция получения "элементарных" отрезков многоугольника
def get_sections(section, rest_points):
    points_list = [section[0], section[1]]
    for p in rest_points:
        if point_in_section(p, section): # Если точка принадлежит отрезку
            points_list.append(p) # то добавляем ее в список

    points_list.sort()

    sections_list = list()
    for i in range(len(points_list) - 1):
        sections_list.append([points_list[i], points_list[i + 1]])

    return sections_list

# Функция выброса ложных ребер из результирующего многоугольника
def get_uniq_sections(figure):
    all_sections = list()
    rest_points = figure[2:]
    for i in range(len(figure)):
        cur_section = [figure[i], figure[(i + 1) % len(figure)]]

        all_sections.extend(get_sections(cur_section, rest_points))

        rest_points.pop(0)
        rest_points.append(figure[i])

    return make_uniq(all_sections)

# Функция рисования результата (многоугольника)
def draw_figure(figure):
    for section in get_uniq_sections(figure):
        draw_section(round(section[0][0]), round(section[0][1]),
                     round(section[1][0]), round(section[1][1]), res_color)

# Функция вычисления векторного произведения
def vect_mul(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]

# Функция вычисления скалярного произведения
def scalar_mul(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]

# Функция проверки многоугольника на выпуклость
def check_polygon(verteces):
    if len(verteces) < 3:
        return False
    sign = 1 if vect_mul(get_vect(verteces[1], verteces[2]),
                         get_vect(verteces[0], verteces[1])) > 0 else -1
    for i in range(3, len(verteces)):
        if sign * vect_mul(get_vect(verteces[i - 1], verteces[i]),
                           get_vect(verteces[i - 2], verteces[i - 1])) < 0:
            return False

    if sign < 0:
        verteces.reverse()

    return True

# Функция получения внутренней нормали к грани
# p1, p2 - вершины грани
# check_point - нужна для проверки, направлена ли нормаль внутрь многоугольника или же из многоугольника  
def get_normal(p1, p2, check_point): # p1, p2 - вершины многоугольника, check_point - следующая вершина в многоугольнике: 
    vect = get_vect(p1, p2)  

    if vect[0] == 0: # Если ищется нормаль к вертикальному вектору
        norm = [1, 0] #то это нормаль [1, 0]
    else:
        norm = [-vect[1] / vect[0], 1]  #вектор нормали находится из условия равенства 0 скалярного произведения исходного вектора и искомого вектора нормали  
 
    if scalar_mul(get_vect(p2, check_point), norm) < 0: # Если скалярное произведение найденного вектора нормали и вектора, совпадающего со следующей стороной многоугольника меньше нуля
        for i in range(len(norm)):  
            norm[i] = -norm[i]  #нормаль направлена из многоугольника, берем обратный вектор  
  
    return norm

# Функция нахождения нормалей ко всем граням многоугольника (отсекателя)
def get_normals_list(verteces):
    length = len(verteces_list)
    normal_list = list()
    for i in range(length):
        normal_list.append(get_normal(verteces[i], verteces[(i + 1) % length],
                                      verteces[(i + 2) % length]))

    return normal_list

# Функция проверки принадлежности точки point отсекателю относительно
# грани [p1, p2]
def check_point(point, p1, p2):
    return True if vect_mul(get_vect(p1, p2), get_vect(p1, point)) <= 0 else False

def find_intersection(section, edge, normal):
    wi = get_vect(edge[0], section[0]) # вектор соединяющий точку грани
    d = get_vect(section[0], section[1]) # вектор ориентации ребра многоугольника
    Wck = scalar_mul(wi, normal)
    Dck = scalar_mul(d, normal)

    diff = [section[1][0] - section[0][0], section[1][1] - section[0][1]] # (P2.x - P1.x) / (P2.y - P1.y)
    t = -Wck / Dck

    return [section[0][0] + diff[0] * t, section[0][1] + diff[1] * t]

# Функция отсечения многоугольника относительно одной грани отсекателя
def edgecut_figure(figure, edge, normal):
    res_figure = list()
    if len(figure) < 3:
        return []

    prev_check = check_point(figure[0], *edge) # принадлежит первая точка отсекателю относительно ребра
    print(prev_check)

    for i in range(1, len(figure) + 1):
        cur_check = check_point(figure[i % len(figure)], *edge) 

        if prev_check: # если не принадлежит 
            if cur_check:
                res_figure.append(figure[i % len(figure)])
            else:
                res_figure.append(find_intersection([figure[i - 1],
                                 figure[i % len(figure)]], edge, normal))
        else: # если принадлежит
            if cur_check: # a след не принадлежит
                res_figure.append(find_intersection([figure[i - 1], # то находим точку пересечения 
                                 figure[i % len(figure)]], edge, normal)) # заносим ее 
                res_figure.append(figure[i % len(figure)]) # и конечную вершину

        prev_check = cur_check

    return res_figure

# Функция отсечения фигуры
def cut_figure(figure, cutter_verteces, normals_list):
    res_figure = figure
    for i in range(len(cutter_verteces)):
        cur_edge = [cutter_verteces[i],
                    cutter_verteces[(i + 1) % len(cutter_verteces)]]
        res_figure = edgecut_figure(res_figure, cur_edge,
                                    normals_list[i])
        if len(res_figure) < 3:
            return []

    return res_figure

def solve():
    if not check_polygon(verteces_list):
        mb.showerror("Невыпуклый многоугольник", "Для осуществления отсечения отрезка алгоритмом Кируса-Бека \nпрямоугольник должен быть выпуклым")
        return
    normals_list = get_normals_list(verteces_list)
    cutted_figure = cut_figure(figure_list, verteces_list, normals_list)
    draw_figure(cutted_figure)


##############################
background_color = 'light grey'
DEFAULT_COLOUR = "#000000" 
CANVAS_COLOUR = "#FFFFFF"

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 780
FIELD_WIDTH = FIELD_HEIGHT = 740

cutter_color = DEFAULT_COLOUR
sect_color = DEFAULT_COLOUR
res_color = DEFAULT_COLOUR
verteces_list = []
sections = []
figure_list = []
###############################

root = tk.Tk()
mainmenu = tk.Menu(root) 
root.title("Lab #9")
root.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))
root.resizable(False, False)
root.configure(background = background_color, menu = mainmenu)

canvas_root = tk.Canvas(root, height = FIELD_WIDTH, width = FIELD_HEIGHT, bg = "white") # Канвас для ввода точек
canvas_root.place(x = 400, y = 15)

canvas_root.bind("<Button-1>", left_click) # добавить точку
root.bind("<Return>", return_click)
canvas_root.bind("<Button-3>", right_click)


taskmenu = tk.Menu(mainmenu, tearoff=0) # выпадающее меню с условием задачи
mainmenu.add_cascade(label="Алгоритм отсечения отрезка произвольным выпуклым отсекателем")

# -- Цвет
pick_color_cut = tk.Label(root, text = "Цвет регулярного отсекателя", font = ('Lucida Console', '13', 'bold'), relief = tk.GROOVE, background = background_color)
pick_color_cut.place(x = 30, y = 33, width=310, height=30) # надпись Цвет ругулярного отсекателя

cutter_color_btn = tk.Button(root, relief=tk.GROOVE, command = change_cutter_color, background = 'black')
cutter_color_btn.place(x = 30, y = 60, width = 310, height = 30)

pick_color_line = tk.Label(root, text = "Цвет отрезков", font = ('Lucida Console', '13', 'bold'), relief = tk.GROOVE, background = background_color)
pick_color_line.place(x = 30, y = 93, width=310, height=30) # надпись цвет отрезков

sect_color_btn = tk.Button(root, relief=tk.GROOVE, command = change_sect_color, background = 'black')
sect_color_btn.place(x = 30, y = 120, width = 310, height = 30)

pick_color_result = tk.Label(root, text = "Цвет результата", font = ('Lucida Console', '13', 'bold'), relief = tk.GROOVE, background = background_color)
pick_color_result.place(x = 30, y = 153, width=310, height=30) # надпись цвет результата

res_color_btn = tk.Button(root, relief=tk.GROOVE, command = change_res_color, background = 'black')
res_color_btn.place(x = 30, y = 180, width = 310, height = 30)

# -- координаты точки
coord_cut_label = tk.Label(root, text = "Ввод вершины отсекателя П", font = ('Lucida Console', '13', 'bold'), relief = tk.GROOVE, background = background_color)
coord_cut_label.place(x = 30, y = 240, width = 310, height = 30) # Координаты точки

left_label = tk.Label(root, text = "x", font = ('Lucida Console', '13'), relief = tk.GROOVE, background = background_color).place(x = 30, y = 270, width = 155, height = 30) # Лейбл xc
right_label = tk.Label(root, text = "y", font = ('Lucida Console', '13'), relief=tk.GROOVE, background = background_color).place(x = 185, y = 270, width = 155, height = 30) # Лейбл yc

cutter_x_entry = tk.Entry(root, justify = tk.CENTER, font = ('Lucida Console', '15'), relief = tk.GROOVE) # для x
cutter_x_entry.place(x = 30, y = 300, width = 155, height = 30)

cutter_y_entry = tk.Entry(root, justify = tk.CENTER, font = ('Lucida Console', '15'), relief = tk.GROOVE) # для y
cutter_y_entry.place(x = 185, y = 300, width = 155, height = 30)


cutter_btn = tk.Button(root, text = "Добавить вершину", font = ('Lucida Console', '13', 'bold'), relief=tk.RAISED, background = background_color, command=read_cutter_vertex)
cutter_btn.place(x = 30, y = 330, width = 310, height = 30) # Координаты точки

close_cutter_btn = tk.Button(root, text = "Замкнуть отсекатель", font = ('Lucida Console', '13', 'bold'), relief=tk.RAISED, background = background_color, command=lambda: return_click(0))
close_cutter_btn.place(x = 30, y = 380, width = 310, height = 30) # Координаты точки

input_lowels_label = tk.Label(root, text = "Ввод вершины многоугольника", font = ('Lucida Console', '13', 'bold'), relief = tk.GROOVE, background = background_color)
input_lowels_label.place(x = 30, y = 450, width = 310, height = 30) # Координаты точки

x_label = tk.Label(root, text = "x", font = ('Lucida Console', '13'), relief = tk.GROOVE, background = background_color).place(x = 30, y = 480, width = 77.5, height = 30) # Лейбл xc
y_label = tk.Label(root, text = "y", font = ('Lucida Console', '13'), relief=tk.GROOVE, background = background_color).place(x = 185, y = 480, width = 77.5, height = 30) # Лейбл yc

x_entry = tk.Entry(root, justify = tk.CENTER, font = ('Lucida Console', '15'), relief = tk.GROOVE,) # для x
x_entry.place(x = 107, y = 480, width = 77.5, height = 30)

y_entry = tk.Entry(root, justify = tk.CENTER, font = ('Lucida Console', '15'), relief = tk.GROOVE,) # для y
y_entry.place(x = 262, y = 480, width = 77.5, height = 30)

vertex_btn = tk.Button(root, text = "Применить", font = ('Lucida Console', '13', 'bold'), relief=tk.RAISED, background = background_color, command = read_vertex)
vertex_btn.place(x = 30, y = 510.5, width = 310, height = 30) # Координаты точки

close_btn = tk.Button(root, text = "Замкнуть многоугольник", font = ('Lucida Console', '13', 'bold'), relief=tk.RAISED, background = background_color, command=lambda: c_click(0))
close_btn.place(x = 30, y = 560, width = 310, height = 30) # Координаты точки
#-- Кнопки выполнить закраску, замерить время, очистить экран, выход
solve_btn = tk.Button(root, text = "Отсечь",  font = ('Lucida Console', '11'), relief=tk.RAISED, command=solve)
solve_btn.place(x = 30, y = 620, width = 310, height = 30)

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

root.mainloop()