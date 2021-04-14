import tkinter as tk
from random import randint
from inspect import getmembers, isfunction
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import Rules as Rules


class Controller:
    def __init__(self):
        self.simulation = Simulation()
        self.main_view = MainView(simulation=self.simulation, controller=self)
        self.animation_reset = False
        self.figure, self.ax = self.main_view.initialize_figure()
        self.anime = FuncAnimation(self.figure, self.animate_figure,
                                   init_func=self.init_animate_figure, blit=True, interval=500)
        self.main_view.mainloop()

    def animate_figure(self, event):
        chaos_point_cords = self.simulation.chaos_points.get_point_cords()
        shape_cords = self.simulation.shape.get_point_cords()
        if self.animation_reset >= 100:
            self.shape_outline = self.ax.plot(*shape_cords, alpha=0.2)
            self.shape_points = self.ax.scatter(*shape_cords, alpha=0.5)
            self.scat = self.ax.scatter(*chaos_point_cords, s=(500/((len(chaos_point_cords[0]) // 3) + 1)))
            self.animation_reset = 0

        delta_chaos_point_cords = []
        for i in range(self.simulation.speed):
            self.simulation.iterate()
            try:
                new_point = (chaos_point_cords[0][-1],
                             chaos_point_cords[1][-1])
            except IndexError:
                new_point = False
            if new_point:
                delta_chaos_point_cords.append(new_point)
        if delta_chaos_point_cords:
            updated_list_of_cords = list(self.scat.get_offsets()) + delta_chaos_point_cords
            self.scat.set_offsets(updated_list_of_cords)
            self.scat.set_sizes([(500/((len(updated_list_of_cords) // 3) + 1))
                                 for _ in range(len(updated_list_of_cords))])

        try:
            self.ax.set_xlim(min(chaos_point_cords[0] + shape_cords[0]) - 1, max(chaos_point_cords[0] + shape_cords[0]) + 1)
            self.ax.set_ylim(min(chaos_point_cords[1] + shape_cords[1]) - 1, max(chaos_point_cords[1] + shape_cords[1]) + 1)
        except ValueError:
            pass

        self.artists = (self.shape_outline[0], self.shape_points, self.scat)
        return self.artists

    def init_animate_figure(self):
        self.ax.clear()
        shape_cords = self.simulation.shape.get_point_cords()
        self.shape_outline = self.ax.plot(*shape_cords, alpha=0.2)
        self.shape_points = self.ax.scatter(*shape_cords, alpha=0.5)
        chaos_point_cords = self.simulation.chaos_points.get_point_cords()
        self.scat = self.ax.scatter(*chaos_point_cords, s=(500/((len(chaos_point_cords[0]) // 3) + 1)))
        self.artists = (self.shape_outline[0], self.shape_points, self.scat)
        return self.artists

    def change_speed(self, speed: int):
        speed_equivalent = [500, 250, 100, 10, 1]
        self.anime.event_source.interval = speed_equivalent[speed]
        self.simulation.change_speed(speed)
        self.update_speed()

    def increase_speed(self):
        self.change_speed(self.simulation.speed_no + 1)

    def decrease_speed(self):
        self.change_speed(self.simulation.speed_no - 1)

    def update_speed(self):
        self.main_view.update_speed_button_states()
        self.main_view.update_speed_label_text()

    def add_shape_point(self):
        self.simulation.add_shape_point()
        self.update_shape()
        self.animation_reset = 100

    def less_shape_point(self):
        self.simulation.less_shape_point()
        self.update_shape()
        self.animation_reset = 100

    def update_shape(self):
        self.main_view.update_shape_label_text()
        self.main_view.update_shape_button_states()

    def rule_trace_callback(self, *args, **kwargs):
        rule = self.main_view.controls_view.rule
        rule_no = self.main_view.controls_view.rules_name_list.index(rule.get())
        self.change_rule(rule_no)
        self.animation_reset = 100

    def distance_trace_callback(self, *args, **kwargs):
        distance = self.main_view.controls_view.distance.get()
        self.simulation.change_jump_distance(distance)
        self.animation_reset = 100

    def change_rule(self, rule_no: int):
        self.simulation.change_rule(rule_no)

    def show_rules_help(self):
        rules_help = RulesHelp(self.main_view)
        rules_help.mainloop()

    def toggle_run(self):
        self.simulation.start_flag = not self.simulation.start_flag
        self.main_view.update_run_button_text()

    def reset(self):
        self.simulation.reset()
        self.update_speed()
        self.update_shape()
        self.main_view.update_run_button_text()
        self.animation_reset = 100


class Points:
    def __init__(self, list_of_tuple_cords=None):
        if list_of_tuple_cords is None:
            list_of_tuple_cords = []
        elif isinstance(list_of_tuple_cords, tuple):
            list_of_tuple_cords = [list_of_tuple_cords]
        self.x_list, self.y_list = self.unpack_to_2_lists(list_of_tuple_cords)

    @staticmethod
    def unpack_to_2_lists(list_of_tuple_cords):
        x_list = []
        y_list = []
        for tuple_coordinate in list_of_tuple_cords:
            x_list.append(tuple_coordinate[0])
            y_list.append(tuple_coordinate[1])
        return x_list, y_list

    def get_point_cords(self):
        return self.x_list, self.y_list

    def add_point(self, x, y):
        self.x_list.append(x)
        self.y_list.append(y)

    def empty(self):
        self.x_list = []
        self.y_list = []


class Shape:
    default_number_of_points = 3
    dict_of_shapes = {3: Points([(10, 15),
                                 (1, 0),
                                 (19, 0),
                                 (10, 15)]),
                      4: Points([(17, 3),
                                 (3, 3),
                                 (3, 17),
                                 (17, 17),
                                 (17, 3)]),
                      5: Points([(10, 0),
                                 (0, 7),
                                 (4, 18),
                                 (16, 18),
                                 (20, 7),
                                 (10, 0)]),
                      6: Points([(15, 1),
                                 (5, 1),
                                 (0, 10),
                                 (5, 19),
                                 (15, 19),
                                 (20, 10),
                                 (15, 1)]),
                      7: Points([(10, 0),
                                 (2, 4),
                                 (0, 12),
                                 (6, 19),
                                 (14, 19),
                                 (20, 12),
                                 (18, 4),
                                 (10, 0)]),
                      8: Points([(14, 1),
                                 (6, 1),
                                 (1, 6),
                                 (1, 14),
                                 (6, 19),
                                 (14, 19),
                                 (19, 14),
                                 (19, 6),
                                 (14, 1)])}

    def __init__(self):
        self.number_of_points = Shape.default_number_of_points
        self.vertices: Points = self.generate_shape(self.number_of_points)

    def get_point_cords(self):
        return self.vertices.get_point_cords()

    def add_shape_point(self):
        self.number_of_points += 1
        self.vertices = self.generate_shape(self.number_of_points)

    def less_shape_point(self):
        self.number_of_points -= 1
        self.vertices = self.generate_shape(self.number_of_points)

    @staticmethod
    def generate_shape(number_of_points):
        return Shape.dict_of_shapes[number_of_points]

    def reset(self):
        self.number_of_points = Shape.default_number_of_points
        self.vertices: Points = self.generate_shape(self.number_of_points)


class InitPoint:
    def __init__(self):
        self.point = Points((randint(5, 12), randint(5, 12)))

    def get_point_cords(self):
        return self.point.get_point_cords()

    def reset(self):
        self.point = Points((randint(5, 12), randint(5, 12)))


class ChaosPoints:
    def __init__(self, init_point: InitPoint, shape: Shape, rule_method, distance):
        self.init_point = init_point
        self.latest_point_xy_cords = (init_point.get_point_cords()[0][0],
                                      init_point.get_point_cords()[1][0])
        self.shape = shape
        self.distance = distance
        self.latest_chosen_vertex = None
        self.points = Points()
        self.rule = rule_method

    def get_point_cords(self):
        return self.points.get_point_cords()

    def generate_point(self):
        new_point_xy_cords, chosen_vertex = self.rule(self.shape,
                                                      self.latest_point_xy_cords,
                                                      self.latest_chosen_vertex,
                                                      self.distance)
        self.latest_point_xy_cords = new_point_xy_cords
        self.latest_chosen_vertex = chosen_vertex
        self.points.add_point(*new_point_xy_cords)

    def reset(self):
        self.latest_point_xy_cords = (self.init_point.get_point_cords()[0][0],
                                      self.init_point.get_point_cords()[1][0])
        self.latest_chosen_vertex = None
        self.points = Points()


class Simulation:
    def __init__(self):
        self.list_of_rules = [el[1] for el in getmembers(Rules, isfunction)]
        self.speed_equivalent = [1, 1, 2, 8, 64]
        self.default_speed = 0
        self.speed_no = self.default_speed
        self.speed = self.speed_equivalent[self.default_speed]
        self.shape = Shape()
        self.init_point = InitPoint()
        self.distance = 0.5
        self.chaos_points = ChaosPoints(init_point=self.init_point,
                                        shape=self.shape,
                                        rule_method=self.list_of_rules[0],
                                        distance=self.distance)
        self.start_flag = False

    def change_speed(self, speed: int):
        self.speed_no = speed
        self.speed = self.speed_equivalent[speed]

    def change_jump_distance(self, distance):
        self.distance = distance
        self.chaos_points.distance = distance
        self.chaos_points.reset()

    def add_shape_point(self):
        self.shape.add_shape_point()
        self.chaos_points.reset()

    def less_shape_point(self):
        self.shape.less_shape_point()
        self.chaos_points.reset()

    def change_rule(self, rule_no: int):
        self.chaos_points.rule = self.list_of_rules[rule_no]
        self.chaos_points.reset()

    def reset(self):
        self.start_flag = False
        self.init_point.reset()
        self.chaos_points.reset()

    def iterate(self):
        if not self.start_flag:
            pass
        else:
            self.chaos_points.generate_point()


class MainView(tk.Tk):
    def __init__(self, simulation: Simulation, controller: Controller, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.simulation = simulation
        self.controller = controller

        self.title('Interactive Live Chaos Game Sim')
        self.configure(bg='#E8E8E8')
        self.geometry("700x700")

        self.graph_view = GraphView(self.simulation, self.controller)
        self.controls_view = ControlsView(self.simulation, self.controller)

        self.graph_view.place(relwidth=1, relheight=0.5)
        self.controls_view.place(rely=0.5, relwidth=1, relheight=0.5)

        def protocol_close():
            self.destroy()
            exit()

        self.protocol('WM_DELETE_WINDOW', protocol_close)

    def update_speed_button_states(self):
        speed = self.simulation.speed_no
        self.controls_view.slower_button.configure(state='normal')
        self.controls_view.faster_button.configure(state='normal')
        if speed == 0:
            self.controls_view.slower_button.configure(state='disabled')
        if speed == 4:
            self.controls_view.faster_button.configure(state='disabled')

    def update_speed_label_text(self):
        self.controls_view.speed_label_text_var.set(self.simulation.speed_no + 1)

    def update_shape_button_states(self):
        no_of_points = self.simulation.shape.number_of_points
        self.controls_view.less_button.configure(state='normal')
        self.controls_view.add_button.configure(state='normal')
        if no_of_points == 3:
            self.controls_view.less_button.configure(state='disabled')
        if no_of_points == 8:
            self.controls_view.add_button.configure(state='disabled')

    def update_shape_label_text(self):
        self.controls_view.shape_label_text_var.set(self.simulation.shape.number_of_points)

    def update_run_button_text(self):
        if self.simulation.start_flag:
            self.controls_view.run_button_text_var.set("STOP")
        else:
            self.controls_view.run_button_text_var.set("RUN")

    def initialize_figure(self):
        return self.graph_view.initialize_figure()


class GraphView(tk.Frame):
    def __init__(self, simulation: Simulation, controller: Controller, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.simulation = simulation
        self.controller = controller
        self.configure(bg='#E8E8E8')

    def initialize_figure(self):
        figure = plt.figure()
        ax1 = figure.add_axes([0, 0, 1, 1])
        ax1.axes.xaxis.set_visible(False)
        ax1.axes.yaxis.set_visible(False)
        ax1.set_frame_on(False)
        canvas = FigureCanvasTkAgg(figure, master=self)
        self.graph_canvas = canvas.get_tk_widget()
        self.graph_canvas.pack()
        return figure, ax1


class ControlsView(tk.Frame):
    def __init__(self, simulation, controller, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.simulation = simulation
        self.controller = controller
        self.configure(bg='#E8E8E8')

        self.run_button_text_var = tk.StringVar()
        self.run_button_text_var.set("RUN")
        self.run_button = tk.Button(master=self,
                                    textvariable=self.run_button_text_var,
                                    command=self.controller.toggle_run)
        self.run_button.place(anchor="nw", rely=0.05, relx=0.25, relwidth=0.5, relheight=0.10)

        self.rule = tk.StringVar()
        rules_func_list = [el[1] for el in getmembers(Rules, isfunction)]
        self.rules_name_list = [rule_func(getinfo='name') for rule_func in rules_func_list]
        self.rule.set(self.rules_name_list[0])
        self.rule.trace("w", callback=self.controller.rule_trace_callback)

        self.rules_menu = tk.OptionMenu(self, self.rule, *self.rules_name_list)
        self.rules_menu.place(anchor="ne", rely=0.20, relx=0.75, relwidth=0.4, relheight=0.10)

        self.qmark_image = Image.open('qmark.png').resize((20, 20), Image.ANTIALIAS)
        self.qmark_image = ImageTk.PhotoImage(self.qmark_image)
        self.qmark_button = tk.Button(self, image=self.qmark_image, command=controller.show_rules_help)
        self.qmark_button.place(anchor="nw", rely=0.20, relx=0.25, relwidth=0.075, relheight=0.10)

        self.distance = tk.DoubleVar()
        self.distance.set(0.5)
        self.distance_scale = tk.Scale(self,
                                       from_=0,
                                       to=2,
                                       orient="horizontal",
                                       digits=3,
                                       resolution=0.01,
                                       variable=self.distance)
        self.distance_scale.place(anchor="ne", rely=0.35, relx=0.75, relwidth=0.5, relheight=0.10)
        self.distance.trace("w", callback=self.controller.distance_trace_callback)

        self.speed_label_text_var = tk.StringVar()
        self.speed_label_text_var.set(self.simulation.speed_no + 1)
        self.speed_label = tk.Label(master=self,
                                    textvariable=self.speed_label_text_var,
                                    bg='#E8E8E8')
        self.faster_button = tk.Button(master=self,
                                       text="FASTER",
                                       command=self.controller.increase_speed)
        self.slower_button = tk.Button(master=self,
                                       text="SLOWER",
                                       command=self.controller.decrease_speed,
                                       state="disabled")
        self.speed_label.place(anchor="n", rely=0.50, relx=0.5, relheight=0.10)
        self.slower_button.place(anchor="nw", rely=0.50, relx=0.25, relwidth=0.2, relheight=0.10)
        self.faster_button.place(anchor="ne", rely=0.50, relx=0.75, relwidth=0.2, relheight=0.10)

        self.shape_label_text_var = tk.StringVar()
        self.shape_label_text_var.set(self.simulation.shape.number_of_points)
        self.shape_label = tk.Label(master=self,
                                    textvariable=self.shape_label_text_var,
                                    bg='#E8E8E8')
        self.add_button = tk.Button(master=self,
                                    text="ADD",
                                    command=self.controller.add_shape_point)
        self.less_button = tk.Button(master=self,
                                     text="LESS",
                                     command=self.controller.less_shape_point,
                                     state="disabled")
        self.shape_label.place(anchor="n", rely=0.65, relx=0.5, relheight=0.10)
        self.less_button.place(anchor="nw", rely=0.65, relx=0.25, relwidth=0.2, relheight=0.10)
        self.add_button.place(anchor="ne", rely=0.65, relx=0.75, relwidth=0.2, relheight=0.10)

        self.reset_button = tk.Button(master=self,
                                      text="RESET",
                                      command=self.controller.reset)

        self.reset_button.place(anchor="ne", rely=0.80, relx=0.75, relwidth=0.5, relheight=0.10)


class RulesHelp(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.title('Info on Rules')
        self.resizable(False, False)
        self.geometry('510x300')

        self.canvas = tk.Canvas(master=self, bg='#E8E8E8')

        self.frame = tk.Frame(master=self.canvas, bg='#E8E8E8')

        self.scrollbar = tk.Scrollbar(master=self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side='right', fill='y')
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw", tags="self.frame")

        self.frame.bind("<Configure>", self.on_frame_configure)

        self.populate()
        self.canvas.bind_all("<Button-4>", self.on_mousewheel_up)
        self.canvas.bind_all("<Button-5>", self.on_mousewheel_down)

    def populate(self):
        intro = tk.Label(master=self.frame,
                         justify='left',
                         anchor='w',
                         wraplength=480,
                         bg='#E8E8E8',
                         font='Helvetica 12 bold',
                         text='        In mathematics, the term chaos game originally referred '
                              "to a method of creating a fractal, "
                              "using a polygon and an initial point selected at random inside it. "
                              "The fractal is created by iteratively creating a sequence of points, "
                              "starting with the initial random point, "
                              "in which each point in the sequence is a given fraction of the distance "
                              "between the previous point and one of the vertices of the polygon; "
                              'the vertex is chosen at random in each iteration.')
        intro.pack(fill='both', padx=5, pady=10)

        rules_func_list = [el[1] for el in getmembers(Rules, isfunction)]
        for rule in rules_func_list:
            rule_label = tk.Label(master=self.frame,
                                  justify='left',
                                  anchor='w',
                                  wraplength=480,
                                  bg='#E8E8E8',
                                  font='Helvetica 12 bold',
                                  text=f"{rule(getinfo='name')} \n     {rule(getinfo='description')}")
            rule_label.pack(fill='both', padx=5, pady=10)

    def on_mousewheel_up(self, event):
        self.canvas.yview_scroll(-1, "units")

    def on_mousewheel_down(self, event):
        self.canvas.yview_scroll(1, "units")

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


if __name__ == '__main__':
    Controller()
