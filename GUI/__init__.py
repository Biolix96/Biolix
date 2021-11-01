from tkinter import *
from PIL import Image, ImageTk


class CustomWindow(Tk):
    def __init__(self):
        super().__init__()

        pw = PanedWindow(self, orient=HORIZONTAL)
        pw.pack(side=TOP, expand=Y, fill=BOTH)

        # ----- Partie de gauche
        pw_left = PanedWindow(pw, orient=VERTICAL)
        pw_left.pack(side=RIGHT, expand=Y, fill=BOTH)
        pw.add(pw_left)

        # --- Gauche haut
        left_top = PumpTable(pw_left)
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
        right.pack()
        pw.add(right)
        # TODO 2 graphiques en bas


class PumpTable(Frame):
    def __init__(self, master, n_pumps=5):
        # Table on the upper left
        super().__init__(master, borderwidth=1, relief=RIDGE)

        Label(self, text="").grid(row=0, column=0)
        Label(self, text="ON").grid(row=0, column=1)
        Label(self, text="OFF").grid(row=0, column=2)
        Label(self, text="Auto").grid(row=0, column=3)
        Label(self, text="State").grid(row=0, column=4)

        self.pumps = list()
        for i_pump in range(n_pumps):
            self.pumps.append(StringVar())
            self.pumps[-1].set(1)
            for i_col in range(5):
                if i_col == 0:
                    Label(self, text='Pump %s' % (i_pump+1)).grid(row=i_pump+1, column=i_col)
                elif i_col == 4:
                    Label(self, text='State %s' % (i_pump+1)).grid(row=i_pump+1, column=i_col)
                else:
                    Radiobutton(self, variable=self.pumps[-1], value=i_col-1).grid(row=i_pump+1, column=i_col)

    def __getitem__(self, item):
        return self.pumps[item].get()


class MeasuresTable(Frame):
    # Table on the bottom left
    def __init__(self, master, n_measures=2):
        super().__init__(master, borderwidth=1, relief=RIDGE)

        Label(self, text="").grid(row=0, column=0)
        Label(self, text="Value").grid(row=0, column=1)

        self.ORP = [4] * n_measures
        self.pH = [7] * n_measures

        for i, measure_type in enumerate(("ORP", "pH")):
            for i_measure in range(n_measures):
                Label(self, text="{} {}".format(measure_type, i_measure+1)).grid(row=i*n_measures+i_measure+1, column=0)
                value = self.ORP[i_measure] if measure_type == "ORP" else self.pH[i_measure]
                Label(self, text=value).grid(row=i*n_measures+i_measure+1, column=1)


class Graphes(Frame):
    def __init__(self, master):
        super().__init__(master)

        plan = Image.open("picture 1.PNG")  # TODO mettre le plan
        plan = ImageTk.PhotoImage(plan)
        image = Label(self, image=plan)
        image.image = plan
        image.pack()
