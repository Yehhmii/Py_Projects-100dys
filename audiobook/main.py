import io
from flask import Flask, render_template, request, send_file, flash
from werkzeug.utils import secure_filename
from gtts import gTTS
import PyPDF2

ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.secret_key = '9821791264196914771'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'pdf' not in request.files:
        flash('No file part')
        return render_template('index.html')
    file = request.files['pdf']
    if file.filename == '':
        flash('No selected file')
        return render_template('index.html')
    if not allowed_file(file.filename):
        flash('Only PDF files are allowed')
        return render_template('index.html')

    # Read PDF text
    reader = PyPDF2.PdfReader(file)
    full_text = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text.append(text)
    book_text = "\n".join(full_text).strip()
    if not book_text:
        flash('Could not extract any text from PDF')
        return render_template('index.html')

    # Convert to speech
    tts = gTTS(book_text)
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    # Send as downloadable file
    filename = secure_filename(file.filename.rsplit('.',1)[0] + '.mp3')
    return send_file(
        mp3_fp,
        mimetype='audio/mpeg',
        as_attachment=True,
        download_name=filename
    )

if __name__ == '__main__':
    app.run(debug=True)
