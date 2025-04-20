import turtle, random
from .config import *
from .levels import load_level
from .sounds import play_paddle, play_brick, play_powerup, play_gameover
from .particles import ParticleSystem
from .powerups import PowerUp


class GameEngine:
    def __init__(self):
        # screen
        self.wn = turtle.Screen()
        self.wn.setup(WIDTH,HEIGHT); self.wn.bgcolor('black'); self.wn.tracer(0)
        # paddle
        self.paddle = turtle.Turtle('square'); self.paddle.shapesize(1,5)
        self.paddle.color('white'); self.paddle.penup()
        self.paddle.goto(0,-HEIGHT//2+40)
        # balls
        self.balls = [self._make_ball()]
        # bricks
        self.bricks = []
        self.level = 0
        self.load_bricks()
        # particles & powerups
        self.particles = ParticleSystem()
        self.powerups = []
        # HUD
        self.score=0; self.lives=LIVES
        # controls
        self.wn.listen()
        self.wn.onkeypress(self.move_left,'Left'); self.wn.onkeypress(self.move_right,'Right')

    def _make_ball(self):
        b = turtle.Turtle('circle'); b.color('red'); b.penup()
        b.dx = BALL_SPEED_START*random.choice((1,-1)); b.dy = BALL_SPEED_START
        return b

    def load_bricks(self):
        self.bricks.clear()
        data = load_level(self.level)['layout']
        start_x = -((BRICK_COLS*(BRICK_W+BRICK_PAD)-BRICK_PAD)//2)
        y0 = HEIGHT//2-TOP_OFFSET
        for r,row in enumerate(data):
            for c,val in enumerate(row):
                if val:
                    b = turtle.Turtle('square'); b.shapesize(BRICK_H/20,BRICK_W/20)
                    b.color((r / 255, 0, (255 - r * 50) / 255))
                    b.penup(); b.goto(start_x + c*(BRICK_W+BRICK_PAD), y0 - r*(BRICK_H+BRICK_PAD))
                    self.bricks.append(b)

    def move_left(self):  self.paddle.setx(max(self.paddle.xcor()-PADDLE_SPEED, -WIDTH//2+50))
    def move_right(self): self.paddle.setx(min(self.paddle.xcor()+PADDLE_SPEED, WIDTH//2-50))

    def update(self):
        # move balls
        for ball in self.balls[:]:
            ball.setx(ball.xcor()+ball.dx); ball.sety(ball.ycor()+ball.dy)
            # wall bounce
            if abs(ball.xcor())>WIDTH//2-10: ball.dx*=-1; play_paddle()
            if ball.ycor()>HEIGHT//2-10: ball.dy*=-1; play_paddle()

            # bottom: lose a life, but reset the ball if you still have lives
            if ball.ycor() < -HEIGHT // 2:
                self.lives -= 1
                play_gameover()

                if self.lives == 0:
                    return False
                # reset this ball instead of removing it
                ball.goto(0, 0)
                ball.dx = BALL_SPEED_START * random.choice((1, -1))
                ball.dy = BALL_SPEED_START
                continue

            # paddle
            if ball.dy<0 and abs(ball.xcor()-self.paddle.xcor())<50 and ball.ycor()<self.paddle.ycor()+10:
                ball.dy*=-1; play_paddle()
                # sticky?
                # TODO
            # brick
            for b in self.bricks:
                if abs(ball.xcor()-b.xcor())<BRICK_W/2 and abs(ball.ycor()-b.ycor())<BRICK_H/2:
                    b.hideturtle(); self.bricks.remove(b)
                    ball.dy*=-1; play_brick()
                    self.score+=10
                    self.particles.emit(b.xcor(), b.ycor(), b.color()[0])
                    # maybe spawn powerup
                    if random.random()<POWERUP_CHANCE:
                        self.powerups.append(PowerUp(b.xcor(), b.ycor()))
                    break

        # powerups
        for pu in self.powerups[:]:
            pu.move()
            if pu.distance(self.paddle)<50:
                play_powerup()
                # apply pu.type e.g. multiball
                if pu.type=='multiball':
                    self.balls.append(self._make_ball())
                # TODO: sticky, laser
                pu.hideturtle(); self.powerups.remove(pu)
            elif pu.ycor()< -HEIGHT//2:
                pu.hideturtle(); self.powerups.remove(pu)

        # particles
        self.particles.update()

        # win?
        if not self.bricks:
            self.level+=1
            self.load_bricks()

        return True
