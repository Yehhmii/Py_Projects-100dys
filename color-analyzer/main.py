import os
from flask import Flask, render_template, request, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
from collections import Counter

# --- Configuration ---
ALLOWED_EXTENSIONS = {'png','jpg','jpeg','gif'}
UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Make sure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# --- Helpers ---
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


# --- Routes ---
@app.route('/', methods=['GET','POST'])
def index():
    top_colors = []
    image_url = None

    if request.method == 'POST':
        file = request.files.get('image')
        if not file or file.filename == '':
            flash('No file selected')
            return render_template('index.html')

        if not allowed_file(file.filename):
            flash('Invalid file type')
            return render_template('index.html')

        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)

        # Build a correct URL to serve it
        image_url = url_for('uploaded_file', filename=filename)

        # Extract top 10 colors
        img = Image.open(save_path).convert('RGB')
        img = img.resize((100, 100))  # downsample for speed
        arr = np.array(img)
        pixels = arr.reshape(-1, 3)
        counter = Counter(map(tuple, pixels))
        most_common = counter.most_common(10)
        top_colors = [(rgb, rgb_to_hex(rgb), count) for rgb, count in most_common]

    return render_template('index.html',
                           top_colors=top_colors,
                           image_url=image_url)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# --- Run ---
if __name__ == '__main__':
    app.run(debug=True)
