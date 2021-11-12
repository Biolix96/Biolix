import json

SAVE_PATH = "save.json"


class Controler:

    def __init__(self, model):
        self.model = model

    def control_pump(self, pump_num, changed_state):
        with open(SAVE_PATH, "r") as save_file:
            saved_data = json.load(save_file)

        if "pump_state" not in saved_data:
            saved_data["pump_state"] = dict()
        saved_data["pump_state"][pump_num] = changed_state

        with open(SAVE_PATH, "w") as save_file:
            json.dump(saved_data, save_file)

        if changed_state == "0":
            str_state = "ON"
        elif changed_state == "1":
            str_state = "OFF"
        else:
            str_state = "Auto"
        print("State of pump {}: {} ({})".format(pump_num, changed_state, str_state))
