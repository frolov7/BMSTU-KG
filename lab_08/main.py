import time
import tkinter as tk
from tkinter import colorchooser
import tkinter.messagebox as mb

def clear_all():
    clear_canvas() 
    sections.clear()
    verteces_list.clear()

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
    if len(verteces_list) < 3:
        return
    draw_section(*verteces_list[-1], *verteces_list[0], cutter_color)

def right_click(event):
    verteces_list.append([event.x, event.y])
    if len(verteces_list) >= 2:
        draw_section(*verteces_list[-1], *verteces_list[-2], cutter_color)

def read_cutter_vertex():
    try:
        x = int(cutter_x_entry.get())
        y = int(cutter_y_entry.get())
    except:
        mb.showerror("Неверный ввод", "Неверный ввод.")
    verteces_list.append([x, y])
    if len(verteces_list) >= 2:
        draw_section(*verteces_list[-1], *verteces_list[-2], cutter_color)

def draw_section(xb, yb, xe, ye, color):
    canvas_root.create_line(xb, yb, xe, ye, fill=color)

def read_vertex():
    if last_point[0]:
        sections.append([last_point[:], [int(x_entry.get()), int(y_entry.get())]])
        draw_section(*sections[-1][0], *sections[-1][1], sect_color)
        last_point[0] = None
    else:
        last_point[0], last_point[1] = int(x_entry.get()), int(y_entry.get())

def change_cutter_color(): # цвет регуярного отсекателя
    global cutter_color
    cutter_color = colorchooser.askcolor(title="select color")[1]
    cutter_color_btn.configure(background=cutter_color)

def change_sect_color(): # цвет отрезков
    global sect_color
    sect_color = colorchooser.askcolor(title="select color")[1]
    sect_color_btn.configure(background=sect_color)

def change_res_color(): #цвет результата
    global res_color
    res_color = colorchooser.askcolor(title="select color")[1]
    res_color_btn.configure(background=res_color)

# Получение свободного вектора по 2 точкам  
def get_vect(p1, p2): # (p1 - начало вектора, p2 - конец вектора)  
    return [p2[0] - p1[0], p2[1] - p1[1]]

# Расчет векторного произведения 2 векторов  
def vect_mul(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]

# Расчет скалярного произведения 2 векторов  
def scalar_mul(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]

# Проверка многоугольника (на выпуклость)  
def check_polygon():  
    if len(verteces_list) < 3:  # Если меньше трех вершин
        return False  
    # Знаки всех векторых произведений должны быть одинаковыми:  
    sign = 1 if vect_mul(get_vect(verteces_list[1], verteces_list[2]), get_vect(verteces_list[0], verteces_list[1])) > 0 else -1  # запоминаем знак первого векторного произведения 

    for i in range(3, len(verteces_list)): # проверяем совпадения знаков векторных произведений всех пар соседних ребер со знаком первого векторного произведения  
        if sign * vect_mul(get_vect(verteces_list[i - 1], verteces_list[i]), #При несовпадении знаков: прямоугольник невыпуклый  
                           get_vect(verteces_list[i - 2], verteces_list[i - 1])) < 0:    
            return False  
  
    if sign < 0: # если знак отрицательный, значит обход был по часовой стрелке.  
        # Работаем с обходом против часовой стрелке =>   
        verteces_list.reverse()  # переворачиваем список вершин
    return True  
 
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

# Cоставляем список векторов нормалей ко всем сторонам многоугольника  
def get_normals_list(verteces):  
    length = len(verteces_list)  
    normal_list = list()  
    for i in range(length):  
        normal_list.append(get_normal(verteces[i], verteces[(i + 1) % length], verteces[(i + 2) % length]))  
  
    return normal_list  
  
# Отсекаеи отрезок и рисует полученный новый отрезок  
def cut(section, verteces_list, normals_list):
	# section - Р
	# verteces_list - вершины многоугольника 
	# normals_list - нормали для всех граней многоугольника
    t_start_list = [0] # параметры t отрезка при которых он пересекает ребро и входит в многоугольник  <= 0
    t_end_list = [1]   # выходит из многоугольника <= 1
  
    d = get_vect(section[0], section[1])  # Вектор направления отрезка - дирректриса (вектор = [P2 - P1])
  
    for i in range(len(verteces_list)): # идем по всем граням многоугольника и ищем параметры t точек пересечения
        # точка многоугольника - начальная вершина этой грани
        if verteces_list[i] != section[0]: # если она совпадает с точкой начала отрезка
            wi = get_vect(verteces_list[i], section[0]) # вычисляем вектор wi от "точки многоугольника" до начала отрезка
        else:  
            wi = get_vect(verteces_list[(i + 1) % len(verteces_list)], section[0]) #берется начальная вершина этой грани
  
        Dck = scalar_mul(d, normals_list[i])  # Скалярное произведение вектора нормали и вектора ориентации
        Wck = scalar_mul(wi, normals_list[i])  # Скалярное произведение вектора нормали и вектора от "точки многоугольника" до начала отрезка
        
        #если оно = 0, то начало отрезка лежит на рассматриваемой грани многоугольника
        # либо отрезок параллелен грани, и лежит вне многоугольника - выход  
        if Dck == 0: # вектор параллелен стороне многоугольника
			#Проверка видимости точки, в которую выродился отрезок, или проверка видимости произвольной 
			#точки отрезка в случае его параллельности стороне отсекателя
            if scalar_mul(wi, normals_list[i]) < 0: #то отрезок (точка) невидимы
                return  
            else: #то отрезок (точка) видимы относительно текущей стороны отсекател
                continue  
  
        t = -Wck / Dck  # Параметр t, соответствующий точке пересечения рассматриваемого отрезка  с очередной гранью 

        #Делим на две группы верхнюю и нижнюю
        if Dck > 0:  # точка входа в многоугольник  
            t_start_list.append(t)  #точка расположена ближе к началу отрезка.
        else:  
            t_end_list.append(t)  # точка расположена ближе к концу отрезка.

    # Видимый отрезок находится между "последним" входом и "первым" выходом
    # Среди всех нижних - наибольшее, среди верхних - наименьшее
    t_start = max(t_start_list)
    t_end = min(t_end_list)
  
    if t_start < t_end:  # Если "входной" t < "выходной" t, то отрезок видимый  
        p1 = [round(section[0][0] + d[0] * t_start), round(section[0][1] + d[1] * t_start)]  
        p2 = [round(section[0][0] + d[0] * t_end), round(section[0][1] + d[1] * t_end)]  
        draw_section(*p1, *p2, res_color)  #чертим его

def solve():
    # Проверка многоугольника на выпуклость  
    if not check_polygon():
        mb.showerror("Невыпуклый многоугольник", "Для осуществления отсечения отрезка алгоритмом Кируса-Бека\nпрямоугольник должен быть выпуклым")
        return

    big_list = list()
    for vertex in verteces_list:
        big_list.extend(vertex)
    canvas_root.create_polygon(*big_list, outline=cutter_color, fill=CANVAS_COLOUR)
    
    normals_list = get_normals_list(verteces_list) # Получение нормалей для всех граней многоугольника  
    
    for section in sections:  
        cut(section, verteces_list, normals_list)  # Отсечение всех отрезков из списка отрезков  

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
last_point = [None, None]
###############################

root = tk.Tk()
mainmenu = tk.Menu(root) 
root.title("Lab #8")
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
coord_cut_label = tk.Label(root, text = "Ввод вершины отсекателя", font = ('Lucida Console', '13', 'bold'), relief = tk.GROOVE, background = background_color)
coord_cut_label.place(x = 30, y = 260, width = 310, height = 30) # Координаты точки

left_label = tk.Label(root, text = "x", font = ('Lucida Console', '13'), relief = tk.GROOVE, background = background_color).place(x = 30, y = 290, width = 155, height = 30) # Лейбл xc
right_label = tk.Label(root, text = "y", font = ('Lucida Console', '13'), relief=tk.GROOVE, background = background_color).place(x = 185, y = 290, width = 155, height = 30) # Лейбл yc

cutter_x_entry = tk.Entry(root, justify = tk.CENTER, font = ('Lucida Console', '15'), relief = tk.GROOVE,) # для x
cutter_x_entry.place(x = 30, y = 320, width = 155, height = 30)

cutter_y_entry = tk.Entry(root, justify = tk.CENTER, font = ('Lucida Console', '15'), relief = tk.GROOVE,) # для y
cutter_y_entry.place(x = 185, y = 320, width = 155, height = 30)


btn_add_lowels = tk.Button(root, text = "Добавить вершину", font = ('Lucida Console', '13', 'bold'), relief = tk.GROOVE, background = background_color, command=read_cutter_vertex)
btn_add_lowels.place(x = 30, y = 350, width = 310, height = 30) # Координаты точки

close_btn = tk.Button(root, text = "Замкнуть отсекатель", font = ('Lucida Console', '13', 'bold'), relief = tk.GROOVE, background = background_color, command=lambda: return_click(0))
close_btn.place(x = 30, y = 420, width = 310, height = 30) # Координаты точки

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
info_center.place(x = 100, y = 580)
root.mainloop()