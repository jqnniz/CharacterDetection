from flask import Flask, render_template, request,redirect,flash,url_for
from flask_socketio import SocketIO, emit
#!/usr/bin/python
import sqlite3
import os,sys
import requests,time
import json, datetime

UPLOAD_FOLDER = 'uploads'
app = Flask(__name__)
#            static_url_path='',
#            static_folder='/static')
app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
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
            #return redirect(url_for('download_file', name=filename))
            return redirect("/")

    return

if __name__ == '__main__':
    socketio.run(app,host="0.0.0.0",allow_unsafe_werkzeug=True)