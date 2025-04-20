import turtle, random
from .config import POWERUP_CHANCE, POWERUP_SPEED

class PowerUp(turtle.Turtle):
    TYPES = ['multiball','sticky','laser']
    def __init__(self, x, y):
        super().__init__(shape='triangle')
        self.color('yellow'); self.penup()
        self.goto(x,y)
        self.dy = -POWERUP_SPEED
        self.type = random.choice(self.TYPES)
    def move(self):
        self.sety(self.ycor()+self.dy)
