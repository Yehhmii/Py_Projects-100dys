import pygame, sys, os

# init mixer
pygame.mixer.init()


def resource_path(rel):
    base = sys._MEIPASS if getattr(sys,'frozen',False) else os.path.abspath(".")
    return os.path.join(base, rel)


def play(path):
    snd = pygame.mixer.Sound(resource_path(path))
    snd.play()


def play_paddle(): play('assets/sounds/paddle.mp3')
def play_brick():  play('assets/sounds/brick.mp3')
def play_powerup(): play('assets/sounds/powerup.mp3')
def play_gameover(): play('assets/sounds/gameover.mp3')
