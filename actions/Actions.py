from actions.Action import Action
import time

class Action_Meow(Action):
    def __init__(self):
        super().__init__("Meow")
    
    def check(self):
        return True
    
    def perform(self, robot, audio):
        audio.play("meow.ogg")

class Action_StepForward(Action):
    def __init__(self):
        super().__init__("TailMotion")
    
    def check(self):
        return True
    
    def perform(self, robot, audio):
        robot.moveForward(50)
        robot.safeWait(1000)

class Action_TailMotion(Action):
    def __init__(self):
        super().__init__("TailMotion")
    
    def check(self):
        return True
    
    def perform(self, robot, audio):
        for cycle in range(7):
            robot.rotateClockwise(70)
            robot.safeWait(100)
            robot.rotateCounterClockwise(70)
            robot.safeWait(150)

class Action_LookAround(Action):
    def __init__(self):
        super().__init__("LookAround")
    
    def check(self):
        return True
    
    def perform(self, robot, audio):
        for cycle in range(3):
            robot.rotateClockwise(40)
            robot.safeWait(600)
            robot.stop()
            robot.safeWait(1000)
            robot.rotateCounterClockwise(50)
            robot.safeWait(600)
            robot.stop()
            robot.safeWait(1000)

class Action_CrazyRotate(Action):
    def __init__(self):
        super().__init__("CrazyRotate")
    
    def check(self):
        return True
    
    def perform(self, robot, audio):
        robot.rotateClockwise(85)
        robot.safeWait(20000)
        robot.stop()