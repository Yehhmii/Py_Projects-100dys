import pygame
import sys, os

# Initialize mixer once
pygame.mixer.init()


# Determine base path (bundle vs script)
def _resource_path(filename):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, filename)
    return filename


def play_check():
    path = _resource_path(os.path.join('sounds', 'airport.mp3'))
    pygame.mixer.Sound(path).play()


def play_break():
    path = _resource_path(os.path.join('sounds', 'collect.mp3'))
    pygame.mixer.Sound(path).play()
