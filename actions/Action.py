from abc import ABC, abstractmethod
from enum import Enum

class ActionType(Enum):
    SFX = 0
    Communication = 1
    Physical = 2

class Action(ABC):
    def __init__(self, name, actionType):
        self.__name = name
        self.__actionType = actionType

    @abstractmethod
    def check(self):
        return True
    
    @abstractmethod
    def perform(self, robot, audio):
        pass