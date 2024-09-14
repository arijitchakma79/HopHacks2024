from abc import ABC, abstractmethod

class Action(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def check(self):
        return True
    
    @abstractmethod
    def perform(self, robot):
        pass