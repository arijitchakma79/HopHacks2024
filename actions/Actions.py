from actions.Action import Action, ActionType
import time

# Sound effect actions
class Action_Meow(Action):
    def __init__(self):
        super().__init__("Meow", ActionType.SFX)
    
    def check(self):
        return True
    
    def perform(self, robot, audio):
        audio.play("meow.ogg", 1.0)

        
class Action_Bark(Action):
    def __init__(self):
        super().__init__("Bark", ActionType.SFX)
    
    def check(self):
        return True
    
    def perform(self, robot, audio):
        audio.play("bark.ogg", 1.0)

class Action_Ring(Action):
    def __init__(self):
        super().__init__("Ring", ActionType.SFX)
    
    def check(self):
        return True
    
    def perform(self, robot, audio):
        audio.play("ring.ogg", 1.0)

class Action_Horn(Action):
    def __init__(self):
        super().__init__("Horn", ActionType.SFX)
    
    def check(self):
        return True
    
    def perform(self, robot, audio):
        audio.play("horn.ogg", 1.0)

class Action_Hello(Action):
    def __init__(self):
        super().__init__("Hello", ActionType.Communication)
    
    def check(self):
        return True
    
    def perform(self, robot, audio):
        audio.play("hello.ogg", 1.0)

class Action_Welcome(Action):
    def __init__(self):
        super().__init__("Welcome", ActionType.Communication)
    
    def check(self):
        return True
    
    def perform(self, robot, audio):
        audio.play("welcome.ogg", 1.0)

class Action_Lost(Action):
    def __init__(self):
        super().__init__("Lost", ActionType.Communication)
    
    def check(self):
        return True
    
    def perform(self, robot, audio):
        audio.play("lost.ogg", 1.0)

class Action_Attention(Action):
    def __init__(self):
        super().__init__("Lost", ActionType.Communication)
    
    def check(self):
        return True
    
    def perform(self, robot, audio):
        audio.play("pay_attention.mp3", 1.0)

# Physical Movement Actions
class Action_StepForward(Action):
    def __init__(self):
        super().__init__("Step",  ActionType.Physical)
    
    def check(self):
        return True
    
    def perform(self, robot, audio):
        robot.moveForward(50)
        robot.safeWait(1000)

class Action_TailMotion(Action):
    def __init__(self):
        super().__init__("TailMotion", ActionType.Physical)
    
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
        super().__init__("LookAround", ActionType.Physical)
    
    def check(self):
        return True
    
    def perform(self, robot, audio):
        for cycle in range(1):
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
        super().__init__("CrazyRotate", ActionType.Physical)
    
    def check(self):
        return True
    
    def perform(self, robot, audio):
        robot.rotateClockwise(85)
        robot.safeWait(3000)
        robot.stop()