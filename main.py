from flask import Flask, render_template , request , flash , redirect , url_for
from werkzeug.utils import secure_filename 
import os
import cv2
import numpy as np
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webp'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/error')
def error():
    return render_template('error.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image(filename, operation):
    print('Processing image', filename, 'with operation', operation)
    img = cv2.imread(f'static/uploads/{filename}')
    print('Image shape:', img.shape)
    match operation:
        case 'cwebp':
            newFilename = f'static/processed/cwebp_{filename.split(".")[0]}.webp'
            cv2.imwrite(newFilename, img)
            return newFilename
        case 'cjpg':
            newFilename = f'static/processed/cjpg_{filename.split(".")[0]}.jpg'
            cv2.imwrite(newFilename, img)
            return newFilename
        case 'cpng':
            newFilename = f'static/processed/cpng_{filename.split(".")[0]}.png'
            cv2.imwrite(newFilename, img)
            return newFilename
        case 'cgrey':
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newFilename = f'static/processed/cgrey_{filename}'
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename
        case 'cblur':
            imgProcessed = cv2.GaussianBlur(img, (21, 21), 0)
            newFilename = f'static/processed/cblur_{filename}'
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename

        case 'ccanny':
            imgProcessed = cv2.Canny(img, 100, 200)
            newFilename = f'static/processed/ccanny_{filename}'
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename

        case 'cdilate':
            kernel = np.ones((5, 5), np.uint8)
            imgProcessed = cv2.dilate(img, kernel, iterations=1)
            newFilename = f'static/processed/cdilate_{filename}'
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename

        case 'cerode':
            kernel = np.ones((5, 5), np.uint8)
            imgProcessed = cv2.erode(img, kernel, iterations=1)
            newFilename = f'static/processed/cerode_{filename}'
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename

        case 'cThreshold':
            imgProcessed = cv2.threshold(img, 125, 255, cv2.THRESH_BINARY)
            newFilename = f'static/processed/cThreshold_{filename}'
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename

        case _:
            print('Invalid operation', operation)
            return redirect(url_for('error'))

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        # Do something with the form data
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return render_template('error.html')
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return render_template('error.html')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'uploads/' + filename))
            op = request.form['operation']
            newFilename = process_image(filename, op)

            flash(f'File uploaded and processed <a href="{newFilename}" target="_blank"> here </a>')
            return render_template('index.html')
        return 'Form data posted'
    return render_template('edit.html')

app.secret_key = '535345464646474634653454364'
app.config['SESSION_TYPE'] = 'filesystem'


app.run(debug=True, port=8000, host='0.0.0.0')
