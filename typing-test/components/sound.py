import pygame
import threading
import sys, os

# Initialize the pygame mixer
pygame.mixer.init()

def resource_path(rel_path):
    """
    Get the absolute path to a resource, whether running
    from source or from a PyInstaller bundle. in prod mode
    """
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS
    else:
        base = os.path.abspath(".")
    return os.path.join(base, rel_path)

def _play(rel_path):
    def play_sound():
        # resolve via resource_path
        path = resource_path(rel_path)
        sound = pygame.mixer.Sound(path)
        sound.play()
    threading.Thread(target=play_sound, daemon=True).start()

def play_start():
    _play('sounds/start.mp3')

def play_end():
    _play('sounds/end.mp3')

def play_key():
    _play('sounds/keypress.mp3')
