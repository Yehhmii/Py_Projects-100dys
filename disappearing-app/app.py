import os, json, time
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = os.urandom(24)
LB_FILE = 'leaderboards.json'

def load_leaderboard():
    if os.path.exists(LB_FILE):
        with open(LB_FILE,'r') as f:
            return json.load(f)
    return []

def save_entry(entry):
    """
    Add or update an entry in the leaderboard JSON.
    If the name already exists, only keep the higher score.
    """
    lb = load_leaderboard()

    for i, e in enumerate(lb):
        if e["name"].lower() == entry["name"].lower():
            if entry["score"] > e["score"]:
                lb[i] = entry
            break
    else:
        lb.append(entry)

    lb.sort(key=lambda x: x["score"], reverse=True)

    with open(LB_FILE, "w") as f:
        json.dump(lb, f, indent=2)

def compute_metrics(text, elapsed_ms):
    # words = split on whitespace
    words = [w for w in text.split() if w.strip()]
    word_count = len(words)
    wpm = (word_count / (elapsed_ms / 1000 / 60))
    # meaningful sentences: at least 3 words, ends with .?!
    sentences = [s for s in text.replace('\n',' ').split('.') if len(s.split())>=3]
    sent_count = len(sentences)
    # score weights: WPM (40%), words (30%), sentences (30%), normalized
    # assume max reasonable WPM=80, words=200, sentences=20
    s_wpm  = min(wpm/80,1) * 40
    s_words= min(word_count/200,1) * 30
    s_sent = min(sent_count/20,1) * 30
    total = round(s_wpm + s_words + s_sent)
    return {
        'wpm': round(wpm,1),
        'words': word_count,
        'sentences': sent_count,
        'score': total
    }

@app.route('/', methods=['GET','POST'])
def index():
    if request.method=='POST':
        name = request.form.get('name','Anonymous').strip()[:20]
        session['name'] = name or 'Anonymous'
        return redirect(url_for('write'))
    return render_template('index.html')

@app.route('/write')
def write():
    if 'name' not in session:
        return redirect(url_for('index'))
    return render_template('writer.html', name=session['name'])

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    text = data.get('text','')
    elapsed = data.get('elapsed', 0)
    name = session.get('name','Anonymous')
    metrics = compute_metrics(text, elapsed)
    entry = {
        'name': name,
        'wpm': metrics['wpm'],
        'words': metrics['words'],
        'sentences': metrics['sentences'],
        'score': metrics['score'],
        'timestamp': int(time.time())
    }
    save_entry(entry)
    return jsonify(metrics)  # return JSON back to client

@app.route('/leaderboard')
def leaderboard():
    lb = load_leaderboard()
    return render_template('leaderboard.html', entries=lb)

if __name__=='__main__':
    app.run(debug=True)
