import copy
from math import sqrt, pi, cos, sin, atan, radians
from tkinter import *
from tkinter import messagebox, ttk

def create_texting(centers):		
	center_coordinates['text'] = "Текущий центр: " + '{:.3f}, {:.3f}'.format(centers[0] - 350, centers[1] - 350)

def coord():
	canvas_root.create_line(0, 3, hei_wed, 3)
	canvas_root.create_text(hei_wed - 10, 10, text = 'X')
	canvas_root.create_line(3, 0, 3, hei_wed)
	canvas_root.create_text(12, hei_wed - 10, text = 'Y')
	canvas_root.create_text(hei_wed / 2, 10, text = str(0))
	canvas_root.create_text(17, hei_wed / 2, text = str(0))
	canvas_root.create_oval(350, 350,350, 350, width = 0, fill = 'red')

	for i in range(0, hei_wed, 50):
		canvas_root.create_line(0, i, hei_wed, i, fill = '#d7d7d8')

	for i in range(0, hei_wed, 50):
		canvas_root.create_line(i, 0, i, hei_wed, fill = '#d7d7d8')

	#'''
	for i in range(0, hei_wed - 50, 50):
		canvas_root.create_text(i + 50, 10, text = str(i - 300))

	for i in range(0, hei_wed - 50,50):
		canvas_root.create_text(17, i + 50, text = str(i - 300))
	'''
	for i in range(0, hei_wed, 50):
		canvas_root.create_text(i + 50, 10, text = str((i - 300) * -1))

	for i in range(0, hei_wed - 50,50):
		canvas_root.create_text(17, i + 50, text = str((i - 300) * -1))
	'''
def add_line(x1, y1, x2, y2):
	global canvas_root
	canvas_root.create_line(x1 + c_0, y1 + c_0, x2 + c_0, y2 + c_0, activedash = (5, 4), fill = 'black')

def add_oval(x1, y1, x2, y2):
	global canvas_root
	canvas_root.create_oval(x1 + c_0, y1 + c_0, x2 + c_0, y2 + c_0, activedash = (5, 4), fill = 'orange')

def add_polygon(x1, y1, x2, y2, x3, y3):
	global canvas_root
	canvas_root.create_polygon(x1 + c_0, y1 + c_0, x2 + c_0, y2 + c_0, x3 + c_0, y3 + c_0,  fill='grey', outline='black')	

def clear_coordinate():
	global canvas_root
	canvas_root.delete('all')
	coord()

def get_randius(point_a, point_b):
	m = (point_b[1] - point_a[1]) / (point_b[0] - point_a[0])
	return atan(m) * 180 / pi

def return_to_start():
	global centers, back_center, begin_center, circle_arcs_head, line_arcs, circle_arcs_body, circle_arcs_eyes_f, circle_arcs_eyes_s, triangle_arcs
	
	clear_coordinate()

	line_arcs = [[-40, -100, 40, -100], [-40, -100 - 15, 40, -100 + 15], [-40, -100 + 15, 40, -100 - 15]] # Усы
	circle_arcs_body = create_ellipse([0,0], 50, 80) # Тело 
	circle_arcs_head = create_ellipse([0, -109], 30, 30) # Голова
	circle_arcs_eyes_f = create_ellipse([-12, -110], 5, 5) # Первый глаз
	circle_arcs_eyes_s = create_ellipse([12, -110], 5, 5) # Второй глаз
	triangle_arcs = [[-20, -132, -5, -138, -10, -158], [20, -132, 5, -138, 10, -158]] # Уши

	back_center.clear()
	back_center = copy.deepcopy(centers)
	centers.clear()
	centers = copy.deepcopy(begin_center)
	
	draw()
	create_texting([350, 350])

def discharge():
	global flag_global
	
	return_to_start()
	flag_global = 1

def step_back():
	global back_center, centers, old_points, line_arcs, circle_arcs_body, triangle_arcs, circle_arcs_head, circle_arcs_eyes_f, circle_arcs_eyes_s, flag_global
	
	if flag_global == 0:
		if len(old_points):
			line_arcs, triangle_arcs, circle_arcs_body, circle_arcs_head, circle_arcs_eyes_f, circle_arcs_eyes_s, back_center = old_points.pop()
			draw()
			create_texting(back_center)
			
			back_center.clear()
			back_center = copy.deepcopy(centers)
			centers.clear()
			centers = copy.deepcopy(begin_center)
	else:
		messagebox.showerror("Ошибка", "Шаг назад недоступен")
		return

def draw():
	global circle_arcs_head, line_arcs, circle_arcs_body, circle_arcs_eyes_f, circle_arcs_eyes_s, triangle_arcs
	
	clear_coordinate()

	canvas_root.create_oval(348,348, 352,352,fill = 'red')
	canvas_root.create_text(350, 358, text = '[0:0]')

	for i in range(len(circle_arcs_body)):
		add_line(circle_arcs_body[i][0][0], circle_arcs_body[i][0][1], circle_arcs_body[i][1][0], circle_arcs_body[i][1][1])

	for i in range(len(circle_arcs_head)):
		add_line(circle_arcs_head[i][0][0], circle_arcs_head[i][0][1], circle_arcs_head[i][1][0], circle_arcs_head[i][1][1])
	
	for i in range(len(circle_arcs_eyes_f)):
		add_line(circle_arcs_eyes_f[i][0][0], circle_arcs_eyes_f[i][0][1], circle_arcs_eyes_f[i][1][0], circle_arcs_eyes_f[i][1][1])
	
	for i in range(len(circle_arcs_eyes_s)):
		add_line(circle_arcs_eyes_s[i][0][0], circle_arcs_eyes_s[i][0][1], circle_arcs_eyes_s[i][1][0], circle_arcs_eyes_s[i][1][1])
	
	for i in range(len(line_arcs)):
		add_line(line_arcs[i][0], line_arcs[i][1], line_arcs[i][2], line_arcs[i][3])

	for i in range(len(triangle_arcs)):
		add_polygon(triangle_arcs[i][0], triangle_arcs[i][1], triangle_arcs[i][2], triangle_arcs[i][3], triangle_arcs[i][4], triangle_arcs[i][5])
	
def rotate_on_degree(x, y, xo, yo, theta):
	xr = cos(theta) * (x - xo) - sin(theta) * (y - yo) + xo
	yr = sin(theta) * (x - xo) + cos(theta) * (y - yo) + yo
	
	return (xr,yr)

def get_num(entry):
	try:
		x = float(entry.get())
	except ValueError:
		entry.delete(0, "end")
		return None
	
	return x

def radian_to_angle(degree):
	return degree * pi / 180

def shift_points(dx, dy): # Перенос
	global old_points, centers, back_center, flag_global
	
	flag_global = 0
	
	x = get_num(dx)
	y = get_num(dy)
	
	if x is None or y is None:
		messagebox.showerror("Ошибка", "Неправильный ввод")
		return
	else:
		back_center.clear()
		back_center = copy.deepcopy(centers)
		centers.clear()

		centers.append(back_center[0] + x)
		centers.append(back_center[1] + y)		

		old_points.append(last_points())
		for i in range(len(line_arcs)):
			line_arcs[i][0] += x
			line_arcs[i][1] += y
			line_arcs[i][2] += x
			line_arcs[i][3] += y
		
		for figure in circle_arcs_body:
			for coord in figure:
				coord[0] += x
				coord[1] += y
		
		for figure in circle_arcs_head:
			for coord in figure:
				coord[0] += x
				coord[1] += y

		for figure in circle_arcs_eyes_f:
			for coord in figure:
				coord[0] += x
				coord[1] += y

		for figure in circle_arcs_eyes_s:
			for coord in figure:
				coord[0] += x
				coord[1] += y				

		for i in range(len(triangle_arcs)):
			triangle_arcs[i][0] += x
			triangle_arcs[i][1] += y
			triangle_arcs[i][2] += x
			triangle_arcs[i][3] += y
			triangle_arcs[i][4] += x
			triangle_arcs[i][5] += y

		draw()
		create_texting(centers)

def rotate_points(degree, center_coordinates): 
	for i in range(len(line_arcs)):
		line_arcs[i][0], line_arcs[i][1] = rotate_on_degree(line_arcs[i][0], line_arcs[i][1], center_coordinates[0], center_coordinates[1], radian_to_angle(degree)) 
		line_arcs[i][2], line_arcs[i][3] = rotate_on_degree(line_arcs[i][2], line_arcs[i][3], center_coordinates[0], center_coordinates[1], radian_to_angle(degree))

	for figure in circle_arcs_body:
		for coord in figure:
			coord[0], coord[1] = rotate_on_degree(coord[0], coord[1], center_coordinates[0], center_coordinates[1], radian_to_angle(degree))

	for figure in circle_arcs_head:
		for coord in figure:
			coord[0], coord[1] = rotate_on_degree(coord[0], coord[1], center_coordinates[0], center_coordinates[1], radian_to_angle(degree))

	for figure in circle_arcs_eyes_f:
		for coord in figure:
			coord[0], coord[1] = rotate_on_degree(coord[0], coord[1], center_coordinates[0], center_coordinates[1], radian_to_angle(degree))

	for figure in circle_arcs_eyes_s:
		for coord in figure:
			coord[0], coord[1] = rotate_on_degree(coord[0], coord[1], center_coordinates[0], center_coordinates[1], radian_to_angle(degree))		

	for i in range(len(triangle_arcs)):
		triangle_arcs[i][0], triangle_arcs[i][1] = rotate_on_degree(triangle_arcs[i][0], triangle_arcs[i][1], center_coordinates[0], center_coordinates[1], radian_to_angle(degree))
		triangle_arcs[i][2], triangle_arcs[i][3] = rotate_on_degree(triangle_arcs[i][2], triangle_arcs[i][3], center_coordinates[0], center_coordinates[1], radian_to_angle(degree))
		triangle_arcs[i][4], triangle_arcs[i][5] = rotate_on_degree(triangle_arcs[i][4], triangle_arcs[i][5], center_coordinates[0], center_coordinates[1], radian_to_angle(degree))

def last_points():
	global line_arcs, circle_arcs_body, triangle_arcs, circle_arcs_head, circle_arcs_eyes_f, circle_arcs_eyes_s, back_center
	return (copy.deepcopy(line_arcs), copy.deepcopy(triangle_arcs), copy.deepcopy(circle_arcs_body), copy.deepcopy(circle_arcs_head), copy.deepcopy(circle_arcs_eyes_f), copy.deepcopy(circle_arcs_eyes_s), copy.deepcopy(back_center))

def turn_dots(degree, center_x, center_y):# Поворот
	global zoom_x1, zoom_y1, old_points, centers, back_center, flag_global
	
	flag_global = 0
	radius = get_num(degree)
	x_center = get_num(center_x)
	y_center = get_num(center_y)
	
	if x_center is None or y_center is None or radius is None:
		messagebox.showerror("Ошибка", "Неправильный ввод")
		return

	if radius != None and x_center != None and y_center != None:
		old_points.append(last_points())

		back_center.clear()
		back_center = copy.deepcopy(centers)
		centers.clear()

		teta = radians(radius)
		centers.append(x_center + (back_center[0] - x_center) * cos(teta) + (back_center[1] - y_center) * sin(teta))
		centers.append(y_center - (back_center[0] - x_center) * sin(teta) + (back_center[1] - y_center) * cos(teta))
		
		rotate_points(radius, [x_center, y_center])

		draw()
		create_texting(centers)
		
	else:
		messagebox.showerror("Ошибка", "Неправильный ввод")
		return

def scale_dots(zoom_x1, zoom_y1, zoom_x2, zoom_y2): # Масштаб
	global flag_global, back_center, centers, old_points

	flag_global = 0
	xc, kx = get_num(zoom_x1), get_num(zoom_x2)
	yc, ky = get_num(zoom_y1), get_num(zoom_y2)

	if ky is None or kx is None or xc is None or yc is None:
		messagebox.showerror("Ошибка", "Неправильный ввод")
		return
	else:
		back_center.clear()
		back_center = copy.deepcopy(centers)
		centers.clear()
		centers.append(kx * back_center[0] + xc * (1 - kx))
		centers.append(ky * back_center[1] + yc * (1 - ky))

		old_points.append(last_points())

		for i in range(len(line_arcs)):
			line_arcs[i][0] = line_arcs[i][0] * kx + (1 - kx) * xc
			line_arcs[i][1] = line_arcs[i][1] * ky + (1 - ky) * yc
			line_arcs[i][2] = line_arcs[i][2] * kx + (1 - kx) * xc
			line_arcs[i][3] = line_arcs[i][3] * ky + (1 - ky) * yc

		for figrue in circle_arcs_body:
			for coord in figrue:
				coord[0] = coord[0] * kx + (1 - kx) * xc
				coord[1] = coord[1] * ky + (1 - ky) * yc
		
		for figrue in circle_arcs_head:
			for coord in figrue:
				coord[0] = coord[0] * kx + (1 - kx) * xc
				coord[1] = coord[1] * ky + (1 - ky) * yc

		for figrue in circle_arcs_eyes_f:
			for coord in figrue:
				coord[0] = coord[0] * kx + (1 - kx) * xc
				coord[1] = coord[1] * ky + (1 - ky) * yc
		
		for figrue in circle_arcs_eyes_s:
			for coord in figrue:
				coord[0] = coord[0] * kx + (1 - kx) * xc
				coord[1] = coord[1] * ky + (1 - ky) * yc

		for i in range(len(triangle_arcs)):
			triangle_arcs[i][0] = triangle_arcs[i][0] * kx + (1 - kx) * xc
			triangle_arcs[i][1] = triangle_arcs[i][1] * ky + (1 - ky) * yc
			triangle_arcs[i][2] = triangle_arcs[i][2] * kx + (1 - kx) * xc
			triangle_arcs[i][3] = triangle_arcs[i][3] * ky + (1 - ky) * yc
			triangle_arcs[i][4] = triangle_arcs[i][4] * kx + (1 - kx) * xc
			triangle_arcs[i][5] = triangle_arcs[i][5] * ky + (1 - ky) * yc

		draw()
		create_texting(centers)

def create_ellipse(centre, a, b):
	circle = []
	num = 60
	step = abs(a) * 2 / num

	for i in range(num):
		x = -a + step * i
		y = sqrt((1 - (x ** 2) / (a ** 2)) * b ** 2)
		x1 = -a + step * (i + 1)
		y1 = sqrt((1 - (x1 ** 2) / (a ** 2)) * b ** 2)
		circle.append([[x + centre[0], y + centre[1]], [x1 + centre[0], y1 + centre[1]]])
	
	for i in range(num):
		x = -a + step * i
		y = -sqrt((1 - (x ** 2) / (a ** 2)) * b ** 2)
		x1 = -a + step * (i + 1)
		y1 = -sqrt((1 - (x1 ** 2) / (a ** 2)) * b ** 2)
		circle.append([[x + centre[0], y + centre[1]], [x1 + centre[0], y1 + centre[1]]])

	return circle

def create():
	global centers, circle_arcs_head, begin_center, line_arcs, circle_arcs_body, circle_arcs_eyes_f, circle_arcs_eyes_s, triangle_arcs
	
	centers.append(350)
	centers.append(350)
	
	begin_center = copy.deepcopy(centers)

	line_arcs = [[-40, -100, 40, -100], [-40, -100 - 15, 40, -100 + 15], [-40, -100 + 15, 40, -100 - 15]] # Усы
	circle_arcs_body = create_ellipse([0,0], 50, 80) # Тело 
	circle_arcs_head = create_ellipse([0, -109], 30, 30) # Голова
	circle_arcs_eyes_f = create_ellipse([-12, -110], 5, 5) # Первый глаз
	circle_arcs_eyes_s = create_ellipse([12, -110], 5, 5) # Второй глаз
	triangle_arcs = [[-20, -132, -5, -138, -10, -158], [20, -132, 5, -138, 10, -158]] # Уши

hei_wed = 700
centre = [0, 0]
c_0 = hei_wed / 2
background_color = 'light grey'
flag_global = 1
centers = []
back_center = []
begin_center = []

root = Tk()
root.title("Lab #2")
root.geometry("950x730")
root.resizable(False, False)
root.configure(background = background_color)
canvas_root = Canvas(root, height = hei_wed, width = hei_wed, bg = "white")

old_points = []
# -- Label
center_coordinates = ttk.Label(root, text = "Текущий центр:", background = background_color)
input_move = ttk.Label(root, text="Перенос", font = ('Arial', '13', 'bold'), background = background_color)
input_dx = ttk.Label(root, text="dx", font = ('Arial', '12'), background = background_color)
input_dy = ttk.Label(root, text="dy", font = ('Arial', '12'), background = background_color)

input_scale = ttk.Label(root, text="Масштабирование", font = ('Arial', '13', 'bold'), background = background_color)
input_xc_scale = ttk.Label(root, text="XC", font = ('Arial', '12'), background = background_color)
input_yc_scale = ttk.Label(root, text="YC", font = ('Arial', '12'), background = background_color)
input_kx_scale = ttk.Label(root, text="KX", font = ('Arial', '12'), background = background_color)
input_kc_scale = ttk.Label(root, text="KY", font = ('Arial', '12'), background = background_color)

input_turn = ttk.Label(root, text="Поворот", font = ('Arial', '13', 'bold'), background = background_color)
input_x_turn = ttk.Label(root, text="X", font = ('Arial', '12'), background = background_color)
input_y_turn = ttk.Label(root, text="Y", font = ('Arial', '12'), background = background_color)
input_degree_turn = ttk.Label(root, text="Угол", font = ('Arial', '12'), background = background_color)

#-- Entry
dx = ttk.Entry(root) # для точки новой x
dy = ttk.Entry(root) # для точки новой y

zoom_x1 = ttk.Entry(root) # xc для массштабирования
zoom_y1 = ttk.Entry(root) # yc для массштабирования
zoom_x2 = ttk.Entry(root) # kx для массштабирования
zoom_y2 = ttk.Entry(root) # ky для массштабирования

center_x = ttk.Entry(root) # x для поворота
center_y = ttk.Entry(root) # y для поворота
degree = ttk.Entry(root) # угол для поворота

#--Buttons
btn_move = Button(root, text = "Перенос", font = ('Arial', '12'), command = lambda: shift_points(dx, dy))
btn_scale = Button(root, text = "Масштаб", font = ('Arial', '12'), command = lambda: scale_dots(zoom_x1, zoom_y1, zoom_x2, zoom_y2))
btn_turn = Button(root, text = "Поворот", font = ('Arial', '12'), command = lambda: turn_dots(degree, center_x, center_y))
btn_step_back = Button(root, text = "Шаг назад", font = ('Arial', '12'), command = step_back)
btn_to_start = Button(root, text = "В начало", font = ('Arial', '12'), command = return_to_start)
btn_discharge = Button(root, text = "Сброс", font = ('Arial', '12'), command = discharge)
btn_quit = Button(root, text = "Выход", font = ('Arial', '12'), command = quit)

#--Label packing
center_coordinates.place(x = 20, y = 20)
input_move.place(x = 75, y = 50) # надпись Перенос
input_dx.place(x = 30, y = 80) # dx
input_dy.place(x = 110, y = 80) # dy

input_scale.place(x = 40, y = 150) # надпись масштабирование
input_xc_scale.place(x = 30, y = 180, width = 50)# надпись 
input_yc_scale.place(x = 120, y = 180, width = 50)# надпись 
input_kx_scale.place(x = 30, y = 200, width = 50)# надпись 
input_kc_scale.place(x = 120, y = 200, width = 50)# надпись 

input_turn.place(x = 75, y = 270) # надпись поворота
input_x_turn.place(x = 30, y = 300)# надпись x для поворота
input_y_turn.place(x = 120, y = 300)# надпись y для поворота
input_degree_turn.place(x = 30, y = 330)# надпись угол для поворота

#--Entry packing
dx.place(x = 50, y = 80, width = 50) # ввод dx для переноса
dy.place(x = 130, y = 80, width = 50) # ввод dy для переноса

zoom_x1.place(x = 60, y = 180, width = 50) # ввод xc для масштаба
zoom_y1.place(x = 150, y = 180, width = 50)# ввод yc для масштаба

zoom_x2.place(x = 60, y = 200, width = 50)# ввод kx для масштаба
zoom_y2.place(x = 150, y = 200, width = 50)# ввод ky для масштаба

center_x.place(x = 55, y = 300, width = 60) # ввод x для поворота
center_y.place(x = 145, y = 300, width = 60)# ввод x для поворота
degree.place(x = 70, y = 330, width = 80)# ввод угла для поворота

#--Button packing
btn_move.place(x = 50, y = 110, width = 130) # Перенос
btn_scale.place(x = 50, y = 230, width = 130) # масштаб
btn_turn.place(x = 50, y = 360, width = 130) # Поворот
btn_step_back.place(x = 50, y = 470, width = 130) # щаг назад
btn_to_start.place(x = 50, y = 510, width = 130) # в начало
btn_discharge.place(x = 50, y = 550, width = 130) # сброс
btn_quit.place(x = 50, y = 685, width = 130) # выход)

coord()
create()
draw()
create_texting([350, 350])
#--canvas root packing
canvas_root.place(x = 220, y = 15)
root.mainloop()