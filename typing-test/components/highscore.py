import json, os, sys

def resource_path(rel_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller bundles.
    """
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS
    else:
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
