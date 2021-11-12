import json
import os
from tkinter import *

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from GUI.Observ import Observer

SAVE_PATH = "save.json"


class ScrollableFrame(Frame):
    """Ref: https://blog.teclado.com/tkinter-scrollable-frames/"""
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = Canvas(self)
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Enter>", self._bound_to_mousewheel)
        self.canvas.bind("<Leave>", self._unbound_to_mousewheel)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")


class Vue(Tk, Observer):
    def __init__(self, controler):
        super().__init__()
        self.controler = controler

        if not os.path.exists(SAVE_PATH):
            with open(SAVE_PATH, "w") as save_file:
                json.dump(dict(), save_file)

        self.pump_table = None
        self.measures_table = None
        self.graphes = None

        self.init_components()
        self.controler.model.add_observer(self.measures_table)
        self.controler.model.add_observer(self.graphes)

    def init_components(self):

        pw = PanedWindow(self, orient=HORIZONTAL)
        pw.pack(side=TOP, expand=Y, fill=BOTH)

        # ----- Partie de gauche
        pw_left = PanedWindow(pw, orient=VERTICAL)
        pw_left.pack(side=RIGHT, expand=Y, fill=BOTH)
        pw.add(pw_left)

        # --- Gauche haut
        left_top = PumpTable(self, pw_left)
        self.pump_table = left_top
        left_top.pack(side=LEFT)
        pw_left.add(left_top)

        # --- Gauche bas
        left_bot = MeasuresTable(pw_left)
        self.measures_table = left_bot
        left_bot.pack(side=LEFT)
        pw_left.add(left_bot)

        # ----- Partie de droite
        right = Graphes(pw)
        self.graphes = right
        right.pack()
        pw.add(right)

    def obs_update(self, item):
        pass


class PumpTable(Frame, Observer):
    def __init__(self, vue, master, n_pumps=5):
        # Table on the upper left
        super().__init__(master, borderwidth=1, relief=RIDGE)
        self.vue = vue
        self.master = master

        Label(self, text="").grid(row=0, column=0)
        Label(self, text="ON").grid(row=0, column=1)
        Label(self, text="OFF").grid(row=0, column=2)
        Label(self, text="Auto").grid(row=0, column=3)

        with open("save.json", "r") as save_file:
            pump_state_dict = json.load(save_file).get("pump_state", dict())

        self.pumps = list()
        for i_pump in range(n_pumps):
            self.pumps.append(StringVar())
            self.pumps[-1].set(pump_state_dict.get(str(i_pump), 1))
            self.pumps[-1].trace("w", self.control)
            for i_col in range(4):
                if i_col == 0:
                    Label(self, text='Pump %s' % i_pump).grid(row=i_pump+1, column=i_col)
                else:
                    Radiobutton(self, variable=self.pumps[-1], value=i_col-1).grid(row=i_pump+1, column=i_col)

    def control(self, *args):
        pump_num = args[0][6:]
        changed_state = self.pumps[int(pump_num)].get()
        self.vue.controler.control_pump(pump_num, changed_state)


class MeasuresTable(Frame, Observer):
    # Table on the bottom left
    def __init__(self, master):
        super().__init__(master, borderwidth=1, relief=RIDGE)

        Label(self, text="").grid(row=0, column=0)
        Label(self, text="Value").grid(row=0, column=1)

        self.measures = list()
        for _ in range(5):
            str_var = StringVar()
            str_var.set(0)
            self.measures.append(str_var)
        self.names = ["pH 1", "pH 2", "ORP 1", "ORP 2", "Cu²\u207A"]

        for i, (name, measure) in enumerate(zip(self.names, self.measures)):
            Label(self, text=name).grid(row=i+1, column=0)
            Label(self, textvariable=self.measures[i]).grid(row=i+1, column=1)

    def obs_update(self, item: dict) -> None:
        for k, v in item.items():
            if k in self.names:
                i = self.names.index(k)
                self.measures[i].set(v)


class Graphes(ScrollableFrame):
    def __init__(self, master):
        super().__init__(master)

        plan = Image.open("picture 1.PNG")  # TODO mettre le plan
        plan = ImageTk.PhotoImage(plan)
        image = Label(self.scrollable_frame, image=plan)
        image.image = plan
        image.pack()

        fig, self.ax_grap1 = plt.subplots()
        self.ax_grap1.plot([0], [0])
        self.canvas1 = FigureCanvasTkAgg(fig, master=self.scrollable_frame)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().pack(side=TOP, expand=1)

    def obs_update(self, item: dict) -> None:
        for k, v in item.items():
            if k == "graph 1":
                self.ax_grap1.clear()
                self.ax_grap1.plot(v)
                self.canvas1.draw()
