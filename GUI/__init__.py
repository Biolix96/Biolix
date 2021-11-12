import os

from GUI.Controler import Controler
from GUI.Model import Model
from GUI.Vue import Vue


class CustomWindow:
    def __init__(self):
        self.model = Model()
        self.controler = Controler(self.model)
        self.vue = Vue(self.controler)
        self.model.add_observer(self.vue)

    def mainloop(self):
        self.vue.mainloop()
        self.model.stop()
