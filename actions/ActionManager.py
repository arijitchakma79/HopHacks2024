from robot.RobotController import RobotController 
from audio.AudioManager import AudioManager

from actions.Actions import Action_Meow, Action_StepForward, Action_TailMotion, Action_LookAround, Action_CrazyRotate

class ActionManager:
    def __init__(self, robot: RobotController, audioManager: AudioManager) -> None:
        self.__robot = robot
        self.__audioManager = audioManager

        self.__actions = {
            "Meow": Action_Meow(),
            "StepForward": Action_StepForward(),
            "TailMotion": Action_TailMotion(),
            "LookAround": Action_LookAround(),
            "CrazyRotate": Action_CrazyRotate()
        }

    def performAction(self, actionName):
        action = self.__actions.get(actionName)
        if(action is None):
            print(f"Action {actionName} not found")
            return
        
        action.perform(self.__robot, self.__audioManager)
        self.__robot.stop()
