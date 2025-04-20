import turtle
from .engine import GameEngine
from .config import *

class UI:
    def __init__(self):
        # CHANGED: keep a reference to the screen so we can clear it
        self.win = turtle.Screen()
        self.win.title("Breakout Clone")

        self.game = GameEngine()

        # CHANGED: separate pen for HUD (cleared each frame)
        self.hud_pen = turtle.Turtle(visible=False)
        self.hud_pen.penup()
        self.hud_pen.color('white')

        # CHANGED: separate pen for button label (drawn once, never cleared)
        self.btn_pen = turtle.Turtle(visible=False)
        self.btn_pen.penup()
        self.btn_pen.color('white')

        # Restart button turtle
        self.btn = turtle.Turtle(visible=False)
        self._draw_button()
        # CHANGED: bind click directly (no lambda needed)
        self.btn.onclick(self.restart)
        self.running = True

    def _draw_button(self):
        self.btn.shape('square')
        self.btn.shapesize(1, 3)
        self.btn.color('gray')
        self.btn.penup()
        self.btn.goto(WIDTH//2 - 80, HEIGHT//2 - 30)
        # CHANGED: hide until game over
        self.btn.hideturtle()

        # CHANGED: draw the "Restart" text once, with btn_pen
        self.btn_pen.goto(WIDTH//2 - 80, HEIGHT//2 - 45)
        self.btn_pen.write("Restart", align='center', font=('Arial', 12, 'bold'))

    def restart(self, x=None, y=None):
        # CHANGED: clear the screen (without killing the event loop) and re-init
        self.win.clearscreen()
        self.__init__()      # rebuild everything
        self.mainloop()      # start the loop again

    def mainloop(self):
        # CHANGED: ensure button is hidden until game over
        self.btn.hideturtle()

        while True:
            if not self.game.update():
                # Game over: show message
                self.hud_pen.goto(0, 0)
                self.hud_pen.write("GAME OVER",
                                   align='center',
                                   font=('Arial', 36, 'bold'))
                break

            # Update HUD (score, lives, level)
            self.hud_pen.clear()
            self.hud_pen.goto(-WIDTH//2 + 20, HEIGHT//2 - 40)
            self.hud_pen.write(
                f"Score: {self.game.score}  Lives: {self.game.lives}  Level: {self.game.level+1}",
                font=('Arial', 18, 'normal')
            )
            self.win.update()

        # CHANGED: show the restart button and hand over to turtle's event loop
        self.btn.showturtle()
        turtle.mainloop()
