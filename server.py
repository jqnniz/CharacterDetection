from flask import Flask, render_template,request,redirect,flash,url_for,send_from_directory
from flask_socketio import SocketIO, emit
#!/usr/bin/python
import sqlite3
import os,sys
import requests,time
import json, datetime
import binascii
import main_test

selectedDate = ""

UPLOAD_FOLDER = 'uploads'
ROOT_DIR = 'events'
app = Flask(__name__)
#            static_url_path='',
#            static_folder='/static')
app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ROOT_DIR'] = ROOT_DIR
app.config['IMAGE_EXTS'] = [".png", ".jpg", ".jpeg", ".gif", ".tiff"]
socketio = SocketIO(app)

def encode(x):
    return binascii.hexlify(x.encode('utf-8')).decode()

def decode(x):
    return binascii.unhexlify(x.encode('utf-8')).decode()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    global selectedDate
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file: #and allowed_file(file.filename):
            #filename = secure_filename(file.filename)
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            date,event_str = main_test.main()
            if date:
                selectedDate = date.strftime('%Y-%m-%d')
            else:
                selectedDate = ""
            print(date,event_str)
            return render_template('index.html', date=selectedDate, event=event_str)

    return

@app.route('/gallery')
def home():
    global selectedDate
    root_dir = app.config['ROOT_DIR']
    image_paths = []
    if selectedDate == "":
        return redirect("/")
    else:
        event_path = os.path.join(root_dir,selectedDate)

        for root,dirs,files in os.walk(event_path):
            for file in files:
                if any(file.endswith(ext) for ext in app.config['IMAGE_EXTS']):
                    image_paths.append(encode(os.path.join(root,file)))
        return render_template('gallery.html', paths=image_paths, date=selectedDate)


@app.route('/cdn/<path:filepath>')
def download_file(filepath):
    dir,filename = os.path.split(decode(filepath))
    return send_from_directory(dir, filename, as_attachment=False)

if __name__ == '__main__':
    socketio.run(app,host="0.0.0.0",allow_unsafe_werkzeug=True)