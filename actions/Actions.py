from actions.Action import Action
import time

class Action_TailMotion(Action):
    def __init__(self):
        super().__init__("TailMotion")
    
    def check(self):
        return True
    
    def perform(self, robot):
        for cycle in range(7):
            robot.rotateClockwise(70)
            time.sleep(0.1)
            robot.rotateCounterClockwise(70)
            time.sleep(0.15)

class Action_LookAround(Action):
    def __init__(self):
        super().__init__("LookAround")
    
    def check(self):
        return True
    
    def perform(self, robot):
        for cycle in range(3):
            robot.rotateClockwise(40)
            time.sleep(0.6)
            robot.stop()
            time.sleep(1)
            robot.rotateCounterClockwise(50)
            time.sleep(0.6)
            robot.stop()
            time.sleep(1)

class Action_CrazyRotate(Action):
    def __init__(self):
        super().__init__("CrazyRotate")
    
    def check(self):
        return True
    
    def perform(self, robot):
        robot.rotateClockwise(85)
        time.sleep(2)
        robot.stop()