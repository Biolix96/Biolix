from tkinter import *
from tkinter.messagebox import showinfo

if __name__ == "__main__":
    window = Tk()

    # ----- Partie de droite
    pw = PanedWindow(window, orient=HORIZONTAL)
    pw.pack(side=TOP, expand=Y, fill=BOTH)

    # ----- Partie de gauche
    pw_left = PanedWindow(pw, orient=VERTICAL)
    pw_left.pack(side=RIGHT, expand=Y, fill=BOTH)
    pw.add(pw_left)

    # --- Gauche haut
    pw_left_top = Frame(pw_left)
    pw_left_top.pack(side=LEFT)
    # TODO tableau pompe avec les boutons
    radio_values = [0]*5
    for i_row in range(1, 6):
        for i_col in range(5):
            if i_col == 0:
                Label(pw_left_top, text='Pompe %s' % i_row).grid(row=i_row, column=i_col)
            elif i_col == 4:
                Label(pw_left_top, text='État  %s' % i_row).grid(row=i_row, column=i_col)
            else:
                print(i_row+i_row*i_col)
                Radiobutton(pw_left_top, variable=radio_values[i_row-1], value=(i_row-1)*5+i_col).grid(row=i_row, column=i_col)
    pw_left.add(pw_left_top)

    # --- Gauche bas
    pw_left_bot = PanedWindow(pw_left, orient=HORIZONTAL)
    pw_left_bot.pack(side=TOP, expand=Y, fill=BOTH)
    pw_left.add(pw_left_bot)

    # Valeurs gauche
    pw_value_left = PanedWindow(pw_left_bot, orient=VERTICAL)
    pw_value_left.pack(side=TOP, expand=Y, fill=BOTH)
    pw_value_left.add(Label(pw_value_left, text="", anchor=E))
    pw_value_left.add(Label(pw_value_left, text="ORP 1", anchor=E))
    pw_value_left.add(Label(pw_value_left, text="ORP 2", anchor=E))
    pw_value_left.add(Label(pw_value_left, text="pH 1", anchor=E))
    pw_value_left.add(Label(pw_value_left, text="pH 2", anchor=E))
    pw_value_left.add(Label(pw_value_left, text="", anchor=E))
    pw_left_bot.add(pw_value_left)

    # Valeurs droite
    pw_value_right = PanedWindow(pw_left_bot, orient=VERTICAL)
    pw_value_right.pack(side=TOP, expand=Y, fill=BOTH)
    pw_value_right.add(Label(pw_value_right, text="Value", anchor=W))
    # TODO Utiliser les vrais valeurs à afficher
    pw_value_right.add(Label(pw_value_right, text="7", anchor=W))
    pw_value_right.add(Label(pw_value_right, text="14", anchor=W))
    pw_value_right.add(Label(pw_value_right, text="3", anchor=W))
    pw_value_right.add(Label(pw_value_right, text="4", anchor=W))
    pw_value_right.add(Label(pw_value_right, text="", anchor=W))
    pw_left_bot.add(pw_value_right)


    # ----- Partie de droite
    plan = PhotoImage(file="picture 1.PNG")  # TODO mettre le plan
    canvas = Canvas(pw, width=plan.width(), height=plan.height())
    canvas.create_image(0, 0, anchor=NW, image=plan)
    canvas.pack()
    pw.add(canvas)
    # TODO 2 graphiques en bas

    window.mainloop()
