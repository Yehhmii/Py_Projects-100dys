import json, os, sys
from .config import LEVEL_FILES

def resource_path(rel):
    base = sys._MEIPASS if getattr(sys, 'frozen',False) else os.path.abspath(".")
    return os.path.join(base, rel)

def load_level(index=0):
    path = resource_path(LEVEL_FILES[index % len(LEVEL_FILES)])
    with open(path,'r') as f:
        return json.load(f)
