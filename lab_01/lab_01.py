import copy
import traceback
from math import fabs, degrees, acos, sqrt
from tkinter import *
from tkinter import messagebox, ttk

def add_line_to_canvas(x1, y1, x2, y2):
	global canvas_root
	canvas_root.create_line(x1 + hei_wed / 2, -y1 + hei_wed / 2, x2 + hei_wed / 2, -y2 + hei_wed / 2, activedash=(5, 4),
							fill='LightGoldenrod3')

def add_text_to_canvas(x, y):
	global canvas_root
	canvas_root.create_text(x * scale + hei_wed / 2, -(y * scale) + hei_wed / 2, text="({:.2f}, {:.2f})".format(x, y))

def add_oval_to_canvas(x1, y1, x2, y2):
	global canvas_root
	canvas_root.create_oval(x1 + hei_wed / 2, -y1 + hei_wed / 2, x2 + hei_wed / 2, -y2 + hei_wed / 2, activedash=(5, 4),
							fill='turquoise1')

def distance_between_points(first_point, second_point):
	x1, x2 = first_point[0], second_point[0]
	y1, y2 = first_point[1], second_point[1]
	return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def layout():
	canvas_root.create_line((hei_wed / 2, hei_wed), (hei_wed / 2, 0), width=1, arrow=LAST)
	canvas_root.create_line((0, hei_wed / 2), (hei_wed, hei_wed / 2), width=1, arrow=LAST)
	canvas_root.create_text((hei_wed - 20, hei_wed / 2 - 10), text='X_cord', font='Arial 10')
	canvas_root.create_text((hei_wed / 2 + 25, 10), text='Y_cord', font='Arial 10')
	canvas_root.create_text((hei_wed / 2 - 10, hei_wed / 2 + 10), text='0', font='Arial 10')

def zoom_in():
	global scale
	if scale < 40:
		scale += 0.5
		draw()

def zoom_out():
	global scale
	if scale > 1:
		scale -= 0.5
		draw()

number = 0

def add_dot():
	global number
	try:
		if [float(entry_x.get()), float(entry_y.get())] in points:  # Если точка была введена
			messagebox.showerror('Ошибка', 'Данная точка уже существует1')
			return

		points.append([float(entry_x.get()), float(entry_y.get())])
		entry_x.delete(0, END)  # Чистим ввод
		entry_y.delete(0, END)
		for i in range(number, len(points)):
			my_table.insert('', 0, text='№' + str(i + 1), values=(points[i][0], points[i][1]))  # Вставка обычной точки
		number += 1  # след точка
	except ValueError:
		messagebox.showerror('Ошибка', 'Некорректный ввод')

def clear_points():
	if not len(points):
		messagebox.showerror('Ошибка', 'Список точек пуст')
	elif messagebox.askyesno('Удаление точек', 'Вы точно хотите удалить все точки?') is True:
		for record in my_table.get_children():
			my_table.delete(record)
		points.clear()
		triangle.clear()
		main_arr.clear()
		triangle_coords.clear()
		coo.clear()
		areas.clear()
		entry_triangle_first_x.delete(0, END)
		entry_triangle_first_y.delete(0, END)
		entry_triangle_second_x.delete(0, END)
		entry_triangle_second_y.delete(0, END)
		entry_triangle_third_x.delete(0, END)
		entry_triangle_third_y.delete(0, END)
		entry_x.delete(0, END)
		entry_y.delete(0, END)
		points.clear()
		triangle.clear()
		main_arr.clear()
		triangle_coords.clear()
		coo.clear()
		areas.clear()
		canvas_root.delete("all")
		layout()
	return

def clear_dot():
	x = my_table.selection()
	for record in x:
		my_table.delete(x)

def triangle_input():
	try:
		x1 = float(entry_triangle_first_x.get())
		y1 = float(entry_triangle_first_y.get())
		x2 = float(entry_triangle_second_x.get())
		y2 = float(entry_triangle_second_y.get())
		x3 = float(entry_triangle_third_x.get())
		y3 = float(entry_triangle_third_y.get())
		triangle.append([x1, y1])
		triangle.append([x2, y2])
		triangle.append([x3, y3])
	except ValueError:
		messagebox.showerror('Ошибка', 'Ошибка ввода')
		return

	if x1 == x2 and y1 == y2 or x2 == x3 and y2 == y3 or x1 == x3 and y1 == y3:  # Если точка была введена
		messagebox.showerror('Ошибка', 'Введенные точки совпадают')
		triangle.clear()
		return

def task():
	task = Tk()
	task.title("Задание")
	task.geometry('500x300+550+100')
	task.resizable(False, False)
	task.configure(background='light blue')
	task_text = Label(task, text="\n\nНа плоскости дано множество точек и треугольник (задан вершинами).\nНайти такую "
								 "окружность, которая проходит хотя бы через\n три различные точки множества и для которой хотя "
								 "бы одна из прямых,\nпроходящих через сторону треугольника, может быть касательной к "
								 "окружности.\nСреди полученных окружностей найти такую, для которой площадь \n треугольника, "
								 "образованного центрами треугольника, окружности\n и точкой касания, максимальна. \n Центр "
								 "треугольника - точка пересечения медиан.\n Сделать в графическом режиме вывод полученного "
								 "результата.\n\n\n", bg="light blue", font=('Arial Bold', 10),
					  fg='black')
	my_name = Label(task, text="Фролов Евгений\nИУ7-45Б", bg="light blue", font=('Arial Bold', 11), fg='black',
					relief='solid')
	task_text.place(x=7, y=10)
	my_name.place(x=200, y=220)
	task.mainloop()

def draw():
	if not len(points):
		messagebox.showerror('Ошибка', 'Точки отсутствуют')
		return
	
	elif len(points) < 3:
		messagebox.showerror('Ошибка', 'Малое количество точек (<3)')
		return
	
	elif len(triangle) < 3:
		messagebox.showerror('Ошибка', 'Малое количество вершин для треугольника')
		return
	# Условие существования треугольника
	def trg(x1, y1, x2, y2, x3, y3):
		trg = (x1 - x3) * (y2 - y3) - (x2 - x3) * (y1 - y3) != 0
		return trg
	# Если оно не выполнилось - ошибка
	if not trg(triangle[0][0],triangle[0][1],triangle[1][0],triangle[1][1],triangle[2][0],triangle[2][1]):
		messagebox.showerror('Ошибка', 'Не выполнилось условие треугольника')
		return

	def chunks(arr, n):
		return [arr[i:i + n] for i in range(0, len(arr), n)]
	
	def triangle_area(x1, y1, x2, y2, x3, y3):
		return fabs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0

	def circ(x1, y1, x2, y2, x3, y3):  # поиск окружности по трем точкам
		if x1 == x2 == x3:  # три точки лежат на одной прямой
			return None
		if x2 == x1:  # случай, когда одна хорда вертикальная, ее коэф = int
			x2, x3 = x3, x2
			y2, y3 = y3, y2
		elif x2 == x3:
			x1, x2 = x2, x1
			y1, y2 = y2, y1
		ma = (y2 - y1) / (x2 - x1)  # наклонный коэф 1-ой хорды
		mb = (y3 - y2) / (x3 - x2)  # накл коэф 2-ой хорды
		if ma != mb:  # прямые совпадают
			x_centre = (ma * mb * (y1 - y3) + mb * (x1 + x2) - ma * (x2 + x3)) / (2 * (mb - ma))
			if ma == 0:
				y_centre = (-1 / mb) * (x_centre - (x2 + x3) / 2) + ((y2 + y3) / 2)
			else:
				y_centre = (-1 / ma) * (x_centre - (x1 + x2) / 2) + ((y1 + y2) / 2)

			res = [x_centre, y_centre]

			on_line = None

			# (y1 - y2)*x + (x2 - x1) * y + (x1y2 - x2y1)
			if ((triangle[0][1] - triangle[1][1]) * x1 + (triangle[1][0] - triangle[0][0]) * y1 + (
					triangle[0][0] * triangle[1][1] - triangle[1][0] * triangle[0][1])) == 0:
				on_line = True
				triangle_coords.append(x1)
				triangle_coords.append(y1)
			elif ((triangle[0][1] - triangle[1][1]) * x2 + (triangle[1][0] - triangle[0][0]) * y2 + (
					triangle[0][0] * triangle[1][1] - triangle[1][0] * triangle[0][1])) == 0:
				on_line = True
				triangle_coords.append(x2)
				triangle_coords.append(y2)
			elif ((triangle[0][1] - triangle[1][1]) * x3 + (triangle[1][0] - triangle[0][0]) * y3 + (
					triangle[0][0] * triangle[1][1] - triangle[1][0] * triangle[0][1])) == 0:
				on_line = True
				triangle_coords.append(x3)
				triangle_coords.append(y3)
			# (y2 - y3)*x + (x3 - x2) * y + (x2y3 - x3y2)
			elif ((triangle[1][1] - triangle[2][1]) * x1 + (triangle[2][0] - triangle[1][0]) * y1 + (
					triangle[1][0] * triangle[2][1] - triangle[2][0] * triangle[1][1])) == 0:
				on_line = True
				triangle_coords.append(x1)
				triangle_coords.append(y1)
			elif ((triangle[1][1] - triangle[2][1]) * x2 + (triangle[2][0] - triangle[1][0]) * y2 + (
					triangle[1][0] * triangle[2][1] - triangle[2][0] * triangle[1][1])) == 0:
				on_line = True
				triangle_coords.append(x2)
				triangle_coords.append(y2)
			elif ((triangle[1][1] - triangle[2][1]) * x3 + (triangle[2][0] - triangle[1][0]) * y3 + (
					triangle[1][0] * triangle[2][1] - triangle[2][0] * triangle[1][1])) == 0:
				on_line = True
				triangle_coords.append(x3)
				triangle_coords.append(y3)

			# (y1 - y3)*x + (x3 - x1) * y + (x1y3 - x3y1)
			elif ((triangle[0][1] - triangle[2][1]) * x1 + (triangle[2][0] - triangle[0][0]) * y1 + (
					triangle[0][0] * triangle[2][1] - triangle[2][0] * triangle[0][1])) == 0:
				on_line = True
				triangle_coords.append(x1)
				triangle_coords.append(y1)
			elif ((triangle[0][1] - triangle[2][1]) * x2 + (triangle[2][0] - triangle[0][0]) * y2 + (
					triangle[0][0] * triangle[2][1] - triangle[2][0] * triangle[0][1])) == 0:
				on_line = True
				triangle_coords.append(x2)
				triangle_coords.append(y2)
			elif ((triangle[0][1] - triangle[2][1]) * x3 + (triangle[2][0] - triangle[0][0]) * y3 + (
					triangle[0][0] * triangle[2][1] - triangle[2][0] * triangle[0][1])) == 0:
				on_line = True
				triangle_coords.append(x3)
				triangle_coords.append(y3)
			
			if on_line == True:
				triangle_center = center_triangle(triangle[0][0], triangle[1][0], triangle[2][0], triangle[0][1],
						triangle[1][1], triangle[2][1])  # Находим центр треугольника
				triangle_coords.append(triangle_center[0])
				triangle_coords.append(triangle_center[1])

				triangle_coords.append(res[0])
				triangle_coords.append(res[1])
				return triangle_coords
			else:
				return None

	def center_triangle(x1, x2, x3, y1, y2, y3):
		x0 = (x1 + x2 + x3) / 3
		y0 = (y1 + y2 + y3) / 3

		return [x0, y0]

	centre = hei_wed / 2

	# отрисовка треугольника 
	canvas_root.create_line((triangle[1][0] * scale) + centre, -(triangle[1][1] * scale) + centre,
							(triangle[2][0] * scale) + centre, -(triangle[2][1] * scale) + centre, fill='yellow')
	canvas_root.create_text(((triangle[1][0] * scale) + centre, -(triangle[1][1] * scale) + centre - 8), text='({:.1f} : {:.1f})'.format(triangle[1][0], triangle[1][1]), font='Arial 6')

	canvas_root.create_line((triangle[0][0] * scale) + centre, -(triangle[0][1] * scale) + centre,
							(triangle[1][0] * scale) + centre, -(triangle[1][1] * scale) + centre, fill='yellow')
	canvas_root.create_text(((triangle[0][0] * scale) + centre - 10, -(triangle[0][1] * scale) + centre + 8), text='({:.1f} : {:.1f})'.format(triangle[0][0], triangle[0][1]), font='Arial 6')
	
	canvas_root.create_line((triangle[2][0] * scale) + centre, -(triangle[2][1] * scale) + centre,
							(triangle[0][0] * scale) + centre, -(triangle[0][1] * scale) + centre, fill='yellow')
	canvas_root.create_text(((triangle[2][0] * scale) + centre + 10, -(triangle[2][1] * scale) + centre + 8), text='({:.1f} : {:.1f})'.format(triangle[2][0], triangle[2][1]), font='Arial 6')
	
	canvas_root.create_oval((triangle[0][0] * scale) + centre, -(triangle[0][1] * scale) + centre,
							(triangle[0][0] * scale) + centre, -(triangle[0][1] * scale) + centre, fill='red',
							outline='red')
	canvas_root.create_oval((triangle[1][0] * scale) + centre, -(triangle[1][1] * scale) + centre,
							(triangle[1][0] * scale) + centre, -(triangle[1][1] * scale) + centre, fill='red',
							outline='red')
	canvas_root.create_oval((triangle[2][0] * scale) + centre, -(triangle[2][1] * scale) + centre,
							(triangle[2][0] * scale) + centre, -(triangle[2][1] * scale) + centre, fill='red',
							outline='red')

	if len(points) < 3:
		messagebox.showinfo('Ошибка', 'Введено недостаточно точек')
		return
	else:
		no_circ = False
		for i in range(len(points) - 2):
			for j in range(i + 1, len(points) - 1):
				for k in range(j + 1, len(points)):
					is_circle = circ(points[i][0], points[i][1], points[j][0], points[j][1], points[k][0], points[k][1])
					if is_circle is not None:
						no_circ = True
					else:
						continue
		if no_circ == False:
			messagebox.showinfo('Ошибка', 'Ни одна из точек не принадлежит прямой')
			return
		else:
			ind = 0
			coo = chunks(triangle_coords, 6)

			for i in range(len(coo)):
				areas.append(triangle_area(coo[i][0],coo[i][1],coo[i][2],coo[i][3],coo[i][4],coo[i][5]))
			
			s_max = areas[0]
			for i in range(len(areas)):
				if (areas[i] > s_max):
					s_max = areas[i]
					ind = i
					
			main_arr = coo[ind]

			R = distance_between_points([main_arr[4], main_arr[5]],
										[main_arr[0], main_arr[1]])  # радиус для найденной окружности
			
			# отрисовка круга найденного
			canvas_root.create_oval(((main_arr[4] + R) * scale) + centre,
									-((main_arr[5] - R) * scale) + centre,
									((main_arr[4] - R) * scale) + centre,
									-((main_arr[5] + R) * scale) + centre, outline='red')
			
			# отрисовка треугольника найденного
			canvas_root.create_line((main_arr[0] * scale) + centre,
									-(main_arr[1] * scale) + centre,
									(main_arr[2] * scale) + centre,
									-(main_arr[3] * scale) + centre, fill='green')
			canvas_root.create_text((main_arr[0] * scale) + centre, -(main_arr[1] * scale) + centre + 10, text='({:.1f} : {:.1f})'.format(main_arr[0], main_arr[1]), font='Arial 6')
			canvas_root.create_oval((main_arr[0] * scale) + centre,
									-(main_arr[1] * scale) + centre,
									(main_arr[0] * scale) + centre,
									-(main_arr[1] * scale) + centre, width=2, fill="black", outline='black')
			
			canvas_root.create_line((main_arr[2] * scale) + centre,
									-(main_arr[3] * scale) + centre,
									(main_arr[4] * scale) + centre,
									-(main_arr[5] * scale) + centre, fill="green")
			canvas_root.create_text((main_arr[2] * scale) + centre, -(main_arr[3] * scale) + centre + 10, text='({:.1f} : {:.1f})'.format(main_arr[2], main_arr[3]), font='Arial 6')
			canvas_root.create_oval((main_arr[2] * scale) + centre,
									-(main_arr[3] * scale) + centre,
									(main_arr[2] * scale) + centre,
									-(main_arr[3] * scale) + centre, width=2, fill="black", outline='black')
			
			canvas_root.create_line((main_arr[0] * scale) + centre,
									-(main_arr[1] * scale) + centre,
									(main_arr[4] * scale) + centre,
									-(main_arr[5] * scale) + centre, fill='green')
			canvas_root.create_text((main_arr[4] * scale) + centre, -(main_arr[5] * scale) + centre + 10, text='({:.1f} : {:.1f})'.format(main_arr[4], main_arr[5]), font='Arial 6')
			canvas_root.create_oval((main_arr[4] * scale) + centre,
									-(main_arr[5] * scale) + centre,
									(main_arr[4] * scale) + centre,
									-(main_arr[5] * scale) + centre,  width=2, fill="black", outline='black')
	# Вывод введенных точек
	for i in range(len(points)):
		canvas_root.create_oval((points[i][0] * scale) + centre, -(points[i][1] * scale) + centre,
								(points[i][0] * scale) + centre, -(points[i][1] * scale) + centre, width=3,
								fill="black")

def zoom_in():
	global scale
	scale += 5
	canvas_root.delete('all')
	draw()
	layout()

def zoom_out():
	global scale
	scale -= 5
	canvas_root.delete('all')
	draw()
	layout()

hei_wed = 600
scale = 40
#points = [[5, 1], [7, 3], [3, 3],[1,5], [2,6],[3,5]]  # Массив точек  ,[1,5], [2,6],[3,5]
points = []
triangle = []  # Массив вершин
triangle_coords = []  # точка касательной, центр треугольника, центр окружности
coo = [] 
areas = [] # массив площадей треугольника
main_arr = [] # массив с координатами точек треугольника с s_Max

background_color = 'light grey'
root = Tk()
root.title("Lab #1")
root.geometry("1000x770")
root.resizable(False, False)
root.configure(background=background_color)

container = ttk.Frame(root)

canvas_root = Canvas(container, height=hei_wed, width=hei_wed, bg="white")
################
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas_root.yview)
scrollable_frame = ttk.Frame(canvas_root)
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas_root.configure(
        scrollregion=canvas_root.bbox("all")
    )
)

canvas_root.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill="y")

################
scrollbar1 = ttk.Scrollbar(container, orient="horizontal", command=canvas_root.xview)
scrollable_frame = ttk.Frame(canvas_root)
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas_root.configure(
        scrollregion=canvas_root.bbox("all")
    )
)

canvas_root.configure(xscrollcommand=scrollbar1.set)
scrollbar1.pack(side=BOTTOM, fill="x")

canvas_root.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas_root.pack(side=RIGHT, fill="both", expand=True)
container.pack(side = RIGHT)

# --table
my_table = ttk.Treeview(root)
my_table['columns'] = ('one', 'two')
my_table.column('one', width=80, stretch=True, anchor='c')
my_table.column('two', width=80, stretch=True, anchor='c')
my_table.heading('one', text='X', anchor='w')
my_table.heading('two', text='Y', anchor='w')

for i in range(len(points)):
	my_table.insert('', 0, text='№' + str(i + 1), values=(points[i][0], points[i][1]))

# -- Label
input_welcom = ttk.Label(root, text="Ввод данных", font=('Arial', '15', 'bold'), background=background_color)
input_x_y = ttk.Label(root, text="Ввод точек (x,y):", font=('Arial', '12'), background=background_color)
triangle_welcome = ttk.Label(root, text="Ввод треугольника:", font=('Arial', '12'), background=background_color)

input_triangle_first = ttk.Label(root, text="1-я точка (x, y):", font=('Arial', '12'), background=background_color)
input_triangle_second = ttk.Label(root, text="2-я точка (x, y):", font=('Arial', '12'), background=background_color)
input_triangle_third = ttk.Label(root, text="3-я точка (x, y):", font=('Arial', '12'), background=background_color)

# -- Entry
entry_x = ttk.Entry(root)  # для точки новой
entry_y = ttk.Entry(root)

entry_triangle_first_x = ttk.Entry(root)  # точка x для треугольника 1
entry_triangle_second_x = ttk.Entry(root)  # 2
entry_triangle_third_x = ttk.Entry(root)  # 3

entry_triangle_first_y = ttk.Entry(root)  # точка x для треугольника 1
entry_triangle_second_y = ttk.Entry(root)  # 2
entry_triangle_third_y = ttk.Entry(root)  # 3

'''
entry_triangle_first_x.insert(0, int(1))
entry_triangle_second_x.insert(0, int(2))
entry_triangle_third_x.insert(0, int(3))

entry_triangle_first_y.insert(0, int(1))
entry_triangle_second_y.insert(0, int(3))
entry_triangle_third_y.insert(0, int(1))
'''

# --Buttons
btn_add_dot = Button(root, text="Добавить точку", font=('Arial', '8'), command=add_dot)
btn_input_triangle = Button(root, text="Ввод треугольника", font=('Arial', '8'), command=triangle_input)
btn_delete_dot = Button(root, text="Удалить точку", font=('Arial', '8'), command=clear_dot)
btn_clear = Button(root, text="Очистить", font=('Arial', '8'), command=clear_points)
btn_task = Button(root, text="Условие задачи", font=('Arial', '8'), command=task)
btn_exit = Button(root, text="Выход", font=('Arial', '8'), command=exit)
btn_start = Button(root, text="Построить", font=('Arial', '12'),background='light grey', foreground="red", command=draw)
btn_zoom_in = Button(root, text = "Zoom in", font = ('Arial', '12'), command=zoom_in)
btn_zoom_out = Button(root, text = "Zoom out", font = ('Arial', '12'), command=zoom_out)

# --Label packing
input_welcom.place(x=70, y=30)  # Ввод данных
input_x_y.place(x=30, y=80)  # Ввод нового х у
triangle_welcome.place(x=70, y=120)  # Ввод треугольника:
input_triangle_first.place(x=30, y=160)  # 1 точка треугольника
input_triangle_second.place(x=30, y=190)  # 2
input_triangle_third.place(x=30, y=220)  # 3

# --Entry packing
entry_x.place(x=160, y=80, width=60)  # ввод нового х
entry_y.place(x=230, y=80, width=60)  # ввод нового у

entry_triangle_first_x.place(x=160, y=160, width=50)  # ввод х для 1 точки треугольника
entry_triangle_second_x.place(x=160, y=190, width=50)  # 2
entry_triangle_third_x.place(x=160, y=220, width=50)  # 3

entry_triangle_first_y.place(x=225, y=160, width=50)  # ввод y для 1 точки треугольника
entry_triangle_second_y.place(x=225, y=190, width=50)  # 2
entry_triangle_third_y.place(x=225, y=220, width=50)  # 3

# --Button packing
btn_add_dot.place(x=30, y=270, width=120)
btn_input_triangle.place(x=155, y=270, width=120)
btn_delete_dot.place(x=30, y=310, width=120)
btn_clear.place(x=155, y=310, width=120)
btn_task.place(x=80, y=575)
btn_exit.place(x=230, y=575)
btn_start.place(x=378, y=10, width=250, height=60)
btn_zoom_in.place(x=628, y = 10, height=60, width=125)
btn_zoom_out.place(x = 753, y = 10, height=60, width=125)

layout()

# --canvas root packing
my_table.place(x=5, y=345)
#canvas_root.place(x=350, y=80)
root.mainloop()
