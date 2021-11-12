from abc import ABC


class Observer(ABC):
    def __init__(self):
        pass

    def obs_update(self, item: dict) -> None:
        pass


class Observable(ABC):
    def __init__(self):
        self.lst_observer = list()

    def add_observer(self, obs: Observer) -> None:
        pass

    def remove_observer(self) -> None:
        pass

    def notify_observer(self, item) -> None:
        pass
