import time
import tkinter as tk
from tkinter import messagebox, colorchooser
import numpy as np

# Флаги расставлены черным цветом. В программе мы проверяем на цвет закраски и контура. 
# Если они черные, то цвет флага меняется.
def get_mark_color(): # если выбрали черный, то границы красные, в другом случае черные
	return DEFAULT_COLOUR if draw_color != DEFAULT_COLOUR else "#FF0000"

def black_or_red(): # если выбрали черный - то границы черные, в другом случае - красные
	return DARK if draw_color != DEFAULT_COLOUR else RED

def reset():
	global vertex_list, extrems
	vertex_list = [[]]
	extrems = [[]]
	p_max.x, p_max.y = 0, 0
	p_min.x, p_min.y = FIELD_WIDTH, FIELD_HEIGHT

def reset_image():
	img.put("#FFFFFF", to=(0, 0, FIELD_WIDTH, FIELD_HEIGHT))

def color_pick():
	global draw_color
	color_arr = colorchooser.askcolor()
	draw_color = color_arr[1]
	btn_color.config(bg=draw_color)

def clear_all():
	reset()
	reset_image()

def draw_section(section):
	for p in section:
		img.put(p.colour, (p.x, p.y))

def update_max_area(event):
	if event.x > p_max.x:
		p_max.x = event.x
	if event.x < p_min.x:
		p_min.x = event.x
	if event.y > p_max.y:
		p_max.y = event.y
	if event.y < p_min.y:
		p_min.y = event.y

def update_extrems(vertex_list, i, extrems):
	if vertex_list[i].y < vertex_list[i - 1].y and vertex_list[i].y < vertex_list[i + 1].y or vertex_list[i].y > vertex_list[i - 1].y and vertex_list[i].y > vertex_list[i + 1].y:
		extrems.append(i if i >= 0 else len(vertex_list) - i)

def put_point():
	try:
		x = int(x_figure.get())
		y = int(y_figure.get())
	except ValueError:
		messagebox.showerror("Ошибка ввода", "Невозможно получить число. Проверьте корректность ввода.")
		return
	dot = Point(x, y) # точка 
	left_click(dot)

def left_click(event):
	if mode.get() == 1 or mode.get() == 2:
		update_max_area(event) # Обновляем p_max p_min
		vertex_list[-1].append(Point(event.x, event.y, draw_color)) # Добавляем p_max p_min

		if len(vertex_list[-1]) > 1:
			section = brezenham_int(draw_color, vertex_list[-1][-2].x, vertex_list[-1][-2].y, vertex_list[-1][-1].x, vertex_list[-1][-1].y)

			if len(vertex_list[-1]) > 2:
				update_extrems(vertex_list[-1], len(vertex_list[-1]) - 2, extrems[-1])

			draw_section(section)   
	else:
		messagebox.showerror("Ошибка", "Выберите режим")
		return

def right_click(event):
	if len(vertex_list[-1]) > 1:
		for i in range(-1, 1):
			update_extrems(vertex_list[-1], i, extrems[-1])

		section = brezenham_int(draw_color, vertex_list[-1][-1].x, vertex_list[-1][-1].y, vertex_list[-1][0].x, vertex_list[-1][0].y)
		draw_section(section)
		vertex_list.append(list())
		extrems.append(list())

def brezenham_int(colour, xb, yb, xe, ye):
	section = list()
	x, y = xb, yb
	dx = xe - xb
	dy = ye - yb
	sx = int(np.sign(dx))
	sy = int(np.sign(dy))
	dx, dy = abs(dx), abs(dy)

	if dx > dy:
		is_change = 0
	else:
		is_change = 1
		dx, dy = dy, dx

	e = dy + dy - dx

	if not is_change:
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

def solve_time():
	canvas_time.delete('draw_time')
	start_time = time.time()
	solve()
	real_time = time.time() - start_time
	canvas_time.create_text(150, 35, text = f"Время построения: {real_time: 8.7f}", font=("Consolas", 14), tag='draw_time')

def solve():
	global delay_time
	pause = mode.get()
	mark_part(vertex_list, extrems)
	if pause == 1:
		try:
			delay_time = float(delay_entry.get())
		except ValueError:
			messagebox.showerror("Ошибка ввода", "Невозможно получить число. Проверьте корректность ввода.")
			return

		canvas_root.update()
		time.sleep(delay_time)
		fill(pause=True)
	else:
		fill()
	reset()

def mark_part(vertex_list, extrems):
	tmp_arr = vertex_list
	for j in range(len(tmp_arr) - 1):
		for i in range(len(tmp_arr[j])):
			mark_borders([[tmp_arr[j][i].x, tmp_arr[j][i].y], [tmp_arr[j][(i + 1) % len(tmp_arr[j])].x, tmp_arr[j][(i + 1) % len(tmp_arr[j])].y]], [i in extrems[j], (i + 1) % len(tmp_arr[j]) in extrems[j]])

def mark_borders(verteces, extrems_bool=(0, 0)): # отметьте все границы
	global draw_color
	if verteces[0][1] == verteces[1][1]: # если вершины равны 
		return
	if verteces[0][1] > verteces[1][1]:
		verteces.reverse()
		extrems_bool.reverse()

	dy = 1
	mark_tuple = black_or_red()
	dx = (verteces[1][0] - verteces[0][0]) / (verteces[1][1] - verteces[0][1])

	if extrems_bool[0]:
		verteces[0][1] += dy
		verteces[0][0] += dx
	if extrems_bool[1]:
		verteces[1][1] -= dy
		verteces[1][0] -= dx

	current_vertex = verteces[0]
	mark_color = get_mark_color()
	while current_vertex[1] < verteces[1][1]:
		if img.get(int(current_vertex[0]) + 1, current_vertex[1]) != mark_tuple: # Еслли мы находим границу
			img.put(mark_color, (int(current_vertex[0]) + 1, current_vertex[1])) # то красим
		else:
			img.put("black", (int(current_vertex[0]) + 1, current_vertex[1]))
		current_vertex[0] += dx
		current_vertex[1] += dy

def invert_color(color): # инвертируем цвет
	return draw_color if color != draw_color else CANVAS_COLOUR

def fill(pause=False):
	global delay_time
	cur_color = CANVAS_COLOUR # Цвет фоновый
	mark_color = black_or_red()
	for y in range(p_max.y, p_min.y, -1): # для y в интвервале [ymin, ymax]
		start_area = p_min.x - 1
		for x in range(p_min.x - 1, p_max.x + 2): # для х в интервале [xmin, xmax]
			if img.get(x, y) == mark_color: # если пиксель в точке х иммеет граниченое значение
				img.put(cur_color, (start_area, y, x, y + 1)) # тогда инвертируем цвет внутри (флаг)
				cur_color = invert_color(cur_color)
				start_area = x
		img.put(cur_color, (start_area, y, x, y + 1)) # окрашеваем пиксел в точке х у новым цветом 
		if pause:
			time.sleep(delay_time)
			canvas_root.update()

def dis_or_norm():
	if mode.get() == 2:
		delay_entry.configure(state="disable")
	else:
		delay_entry.configure(state="normal")

###############################################
background_color = 'light grey'
CANVAS_COLOUR = "#FFFFFF" # белый
DEFAULT_COLOUR = "#000000" # черный 
RED = (255, 0, 0)
DARK = (0, 0, 0)

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 780
FIELD_WIDTH = FIELD_HEIGHT = 740
center = 370

class Point:
    def __init__(self, x=0, y=0, colour="#FFFFFF"):
        self.x = x
        self.y = y
        self.colour = colour

vertex_list = [[]] # вершины
extrems = [[]] # края
p_max = Point()
p_min = Point(FIELD_WIDTH, FIELD_HEIGHT)
draw_color = DEFAULT_COLOUR
##############################################

root = tk.Tk()
mainmenu = tk.Menu(root) 
root.title("Lab #5")
root.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))
root.resizable(False, False)
root.configure(background = background_color, menu = mainmenu)

canvas_root = tk.Canvas(root, height = FIELD_WIDTH, width = FIELD_HEIGHT, bg = "white") # Канвас для ввода точек
canvas_root.bind("<Button-1>", left_click)
canvas_root.bind("<Button-3>", right_click)

img = tk.PhotoImage(width=FIELD_WIDTH, height=FIELD_HEIGHT)
canvas_root.create_image((FIELD_WIDTH // 2, FIELD_HEIGHT // 2), image=img, state='normal')
reset()
reset_image()

canvas_root.place(x = 400, y = 15)

taskmenu = tk.Menu(mainmenu, tearoff=0) # выпадающее меню с условием задачи
taskmenu.add_command(label="Алгоритм заполнения со списком ребер и флагом")
mainmenu.add_cascade(label="Вариант задания", menu=taskmenu)

# -- Режим
mode_label = tk.Label(root, text = "Режим", font = ('Lucida Console', '15', 'bold'), background = background_color)
mode_label.place(x = 150, y = 25) # надпись выбор режим

mode = tk.IntVar()

btn_delay = tk.Radiobutton(text="С задержкой", font = ('Lucida Console', '13'), value=1, variable=mode, padx=15, pady=10,background = background_color, command = dis_or_norm)
btn_no_delay = tk.Radiobutton(text="Без задержки", font = ('Lucida Console', '13'), value=2, variable=mode, padx=15, pady=10,background = background_color, command = dis_or_norm)

btn_delay.place(x = 30, y = 60)
btn_no_delay.place(x = 30, y = 115)

delay_entry = tk.Entry(root, justify = tk.CENTER, font = ('Lucida Console', '15'), background = background_color) # для задержки
delay_entry.configure(state="disable")
delay_entry.place(x = 200, y = 65, width = 80, height = 30)

# -- Цвет
pick_color = tk.Label(root, text = "Цвет", font = ('Lucida Console', '13', 'bold'), background = background_color)
pick_color.place(x = 150, y = 175) # надпись цвет

btn_color = tk.Button(root, relief=tk.GROOVE , command = color_pick, background = 'black')
btn_color.place(x = 30, y = 215, width = 310, height = 30)

# -- координаты точки
coord_dot_label = tk.Label(root, text = "Координаты точки", font = ('Lucida Console', '13', 'bold'), background = background_color)
coord_dot_label.place(x = 100, y = 300) # Координаты точки

x_label = tk.Label(root, text = "X", font = ('Lucida Console', '15'), background = background_color) # Лейбл xc
y_label = tk.Label(root, text = "Y", font = ('Lucida Console', '15'), background = background_color) # Лейбл yc

x_label.place(x = 90, y = 350)
y_label.place(x = 260, y = 350)

x_figure = tk.Entry(root, justify = tk.CENTER, font = ('Lucida Console', '15')) # для x
x_figure.place(x = 30, y = 380, width = 150, height = 30)

y_figure = tk.Entry(root, justify = tk.CENTER, font = ('Lucida Console', '15')) # для y
y_figure.place(x = 190, y = 380, width = 150, height = 30)

btn_add_dot = tk.Button(root, text = "Добавить точку",  font = ('Lucida Console', '11'), relief=tk.RAISED, command = put_point)
btn_add_dot.place(x = 30, y = 420, width = 310, height = 30)

btn_time = tk.Button(root, text = "Замерить время",  font = ('Lucida Console', '11'), relief=tk.RAISED, command = solve_time)
btn_time.place(x = 30, y = 470, width = 310, height = 30)

canvas_time = tk.Canvas(root, height = 70, width = 310, bg = "white")
canvas_time.create_rectangle(1.5,1.5,311,71, outline="black", fill = "#e9e9e9")
canvas_time.place(x = 30, y = 510)

#-- Кнопки выполнить закраску, замерить время, очистить экран, выход
btn_draw = tk.Button(root, text = "Выполнить закраску",  font = ('Lucida Console', '11'), relief=tk.RAISED, command = solve)
btn_draw.place(x = 30, y = 620, width = 310, height = 30)

btn_clear = tk.Button(root, text = "Очистить экран",  font = ('Lucida Console', '11'), relief=tk.RAISED, command = clear_all)
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