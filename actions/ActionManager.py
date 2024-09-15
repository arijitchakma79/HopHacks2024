from robot.RobotController import RobotController 
from audio.AudioManager import AudioManager

from actions.Actions import Action_Meow, Action_Bark, Action_Ring, Action_Horn
from actions.Actions import Action_Hello, Action_Welcome, Action_Lost, Action_Attention
from actions.Actions import Action_StepForward, Action_TailMotion, Action_LookAround, Action_CrazyRotate

class ActionManager:
    def __init__(self, robot: RobotController, audioManager: AudioManager) -> None:
        self.__robot = robot
        self.__audioManager = audioManager

        self.__actions = {
            "Meow": Action_Meow(),
            "Bark": Action_Bark(),
            "Ring": Action_Ring(),
            "Horn": Action_Horn(),
            "Hello": Action_Hello(),
            "Welcome": Action_Welcome(),
            "Lost": Action_Lost(),
            "Attention": Action_Attention(),
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