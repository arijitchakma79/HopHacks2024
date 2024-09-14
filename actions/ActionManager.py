from robot.RobotController import RobotController 

from actions.Actions import Action_TailMotion, Action_LookAround, Action_CrazyRotate

class ActionManager:
    def __init__(self, robot: RobotController) -> None:
        self.__robot = robot

    def performAction(self, actionName):
        action = Action_CrazyRotate()
        action.perform(self.__robot)
