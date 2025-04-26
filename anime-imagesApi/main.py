import random
import requests
from flask import Flask, render_template

app = Flask(__name__)

SELECTION = {
            'sfw': ['waifu', 'neko', 'shinobu', 'megumin', 'bully', 'cuddle', 'cry', 'hug', 'awoo', 'kiss',
                    'lick', 'pat', 'smug', 'bonk', 'yeet', 'blush', 'smile', 'wave', 'highfive', 'handhold',
                    'nom', 'bite', 'glomp', 'slap', 'kill', 'kick', 'happy', 'wink', 'poke', 'dance', 'cringe'
                    ],
            'nsfw': ['waifu', 'neko', 'trap', 'blowjob'],
          }

API_BASE = "https://api.waifu.pics"


def fetch_random(category: str, count: int = 10) -> list[str]:
    urls = []
    for _ in range(count):
        tag = random.choice(SELECTION[category])
        endpoint = f"{API_BASE}/{category}/{tag}"
        try:
            resp = requests.get(endpoint, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            urls.append(data['url'])
        except Exception:
            # on failure, skip this one
            continue
    return urls


@app.route('/')
def index():
    sfw_images  = fetch_random('sfw', count=10)
    nsfw_images = fetch_random('nsfw', count=10)
    return render_template('index.html',
                           sfw_images=sfw_images,
                           nsfw_images=nsfw_images)


if __name__ == '__main__':
    app.run(debug=True)

