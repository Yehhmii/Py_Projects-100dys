import json
import os
import sys

def resource_path(rel_path: str) -> str:
    if getattr(sys, 'frozen', False):
        # Running as a bundled exe: put the JSON next to the .exe
        base = os.path.dirname(sys.executable)
    else:
        # Running in normal Python: base is the current working directory
        base = os.path.abspath(".")
    return os.path.join(base, rel_path)


PATH = resource_path('highscore.json')


def load_scores() -> dict:
    if os.path.exists(PATH):
        with open(PATH, 'r') as f:
            return json.load(f)
    return {}


def save_score(mode: str, diff: str, wpm: float):
    data = load_scores()
    key = f"{mode}-{diff}"
    data[key] = max(data.get(key, 0), wpm)
    with open(PATH, 'w') as f:
        json.dump(data, f, indent=2)
