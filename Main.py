from GUI import CustomWindow

if __name__ == "__main__":
    window = CustomWindow()

    pump_positions = [window.pump_table[i] for i in range(5)]
    print("Pumps buttons:", pump_positions)

    print("ORPs:", window.measures_table.ORP)
    print("pHs:", window.measures_table.pH)

    window.mainloop()
