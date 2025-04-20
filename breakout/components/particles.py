# ====== components/particles.py ======

import turtle
import random
import math
from .config import PARTICLE_COUNT, PARTICLE_SPEED

class Particle:
    def __init__(self, x, y, color):
        self.t = turtle.Turtle(shape='circle')
        self.t.shapesize(0.2, 0.2)
        self.t.color(color)
        self.t.penup()
        self.t.goto(x, y)
        # pick a random angle in radians
        angle = random.uniform(0, 2 * math.pi)
        self.dx = PARTICLE_SPEED * random.uniform(0.5, 1) * math.cos(angle)
        self.dy = PARTICLE_SPEED * random.uniform(0.5, 1) * math.sin(angle)
        self.ttl = 20  # “time to live” frames

    def update(self):
        x, y = self.t.position()
        self.t.goto(x + self.dx, y + self.dy)
        self.ttl -= 1
        if self.ttl <= 0:
            self.t.hideturtle()
            return False
        return True

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, color):
        for _ in range(PARTICLE_COUNT):
            self.particles.append(Particle(x, y, color))

    def update(self):
        # keep only the particles still alive
        self.particles[:] = [p for p in self.particles if p.update()]
