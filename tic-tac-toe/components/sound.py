import pygame
import threading
import os

pygame.mixer.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUND_DIR = os.path.join(BASE_DIR, "../assets")

def play_sound(file_name):
    def _play():
        sound_path = os.path.join(SOUND_DIR, file_name)
        sound = pygame.mixer.Sound(sound_path)
        sound.play()
    threading.Thread(target=_play).start()

def play_click():
    play_sound("click.mp3")

def play_win():
    play_sound("win.mp3")

def play_draw():
    play_sound("draw.mp3")
