import random
from threading import Thread
from time import sleep

import matplotlib.pyplot as plt

from GUI.Observ import Observable


class Model(Observable):
    def __init__(self):
        super().__init__()

        self.stop_threads = False
        self.threads = list()
        self.threads.append(Thread(target=self.read_probes))
        self.threads.append(Thread(target=self.draw_graph))
        for thread in self.threads:
            thread.start()

    def read_probes(self):
        probe_names = ["pH 1", "pH 2", "ORP 1", "ORP 2", "Cu²\u207A"]
        while not self.stop_threads:
            self.notify_observer({random.choice(probe_names): random.randint(0, 10)})
            sleep(1)

    def draw_graph(self):
        values = [0]
        for _ in range(50):
            values.append(random.randint(values[-1]-2, values[-1]+2))

        while not self.stop_threads:
            for _ in range(3):
                values.append(random.randint(values[-1]-2, values[-1]+2))
            self.notify_observer({"graph 1": values})
            sleep(3)

    def add_observer(self, obs):
        self.lst_observer.append(obs)

    def notify_observer(self, item):
        for obs in self.lst_observer:
            obs.obs_update(item)

    def remove_observer(self):
        self.lst_observer = list()

    def stop(self):
        self.stop_threads = True
