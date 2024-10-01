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
    events = getAllEventsFromJSON()
    events = sortEventsDateDescending(events)
    events = addTitleImagePathToEvents(events)
    maxCharacterCountEventTitle = 16
    events = shortAllEventNamesToGivenLength(events,maxCharacterCountEventTitle)
    return render_template('index.html', events=events)

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
            #return render_template('index.html', date=selectedDate, event=event_str)
            return redirect('/gallery')

    return
@app.route('/gallery', methods=['POST'])
def upload_file_toGallery():
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
            event_path = os.path.join(app.config['ROOT_DIR'],selectedDate)

            if not os.path.exists(event_path):
                os.mkdir(event_path) 

            file.save(os.path.join(event_path,filename))
            image_paths=getPathsFromDir(event_path)
        return render_template('gallery.html', paths=image_paths, date=selectedDate)

    return

@app.route('/newevent', methods=['POST'])
def create_new_event():
    print(dir(request))
    print(request.args.get("event-date"))

    return
def getPathsFromDir(dir):
    image_paths = []
    for root,dirs,files in os.walk(dir):
        for file in files:
            if any(file.endswith(ext) for ext in app.config['IMAGE_EXTS']):
                image_paths.append(encode(os.path.join(root,file)))

    return image_paths

@app.route('/newevent')
def newevent():
    global selectedDate
    if request.args:
        selectedDate = request.args.get("event-date")

        newevent = {'date': request.args.get("event-date"),
                     'price': request.args.get("event-price"),
                     'location': request.args.get("event-location"),
                     'stadium': request.args.get("event-stadium"),
                     'artist': request.args.get("event-artist"),
                     'tourname': request.args.get("event-tourname")
        }
        events = main_test.read_json('events.json', events='events')

        events.append(newevent)

        main_test.write_json('events.json', events=events)

        event_path = os.path.join(app.config['ROOT_DIR'],selectedDate)

        if not os.path.exists(event_path):
            os.mkdir(event_path) 

        image_paths=getPathsFromDir(event_path)
        return redirect(url_for('.home', paths=image_paths, date=selectedDate))


    return render_template('newevent.html')

@app.route('/gallery')
def home():
    global selectedDate
    root_dir = app.config['ROOT_DIR']

    selectedDate = request.args.get('eventdate')

    if selectedDate == "" or selectedDate == None:
        return redirect("/")
    else:
        event_path = os.path.join(root_dir,selectedDate)
        image_paths=getPathsFromDir(event_path)


        event = getEventFromJSONWhereDate(selectedDate)
        if event == None:
            return redirect("/")
        else:
            #try:
            d0 = datetime.datetime.strptime(selectedDate,"%Y-%m-%d")
            d1 = datetime.datetime.now()
            delta = (d1 - d0).days
            #except:
            #    delta = ""
            #    pass

            return render_template('gallery.html', paths=image_paths, date=event[0],price=event[1],ort=event[2],stadium=event[3],artist=event[4],tour=event[5],days_offset=delta)


@app.route('/cdn/<path:filepath>')
def download_file(filepath):
    dir,filename = os.path.split(decode(filepath))
    return send_from_directory(dir, filename, as_attachment=False)

@socketio.on('init_connection')
def init_connection(message):
    initDateSelection()

@socketio.on('select_date')
def select_date(message):
    global selectedDate
    selectedDate = message["date"]
    print(selectedDate)


@socketio.on('selectTitleImage')
def select_title_image(image):
    global selectedDate
    element = image["data"]
    print("selectTitleImage")
    print(element)
    encodedpath = element.split("/cdn/")[-1]
    print(encodedpath)

    decodedFullPath = decode(encodedpath)
    print(decodedFullPath)

    filename = decodedFullPath.split("\\")[-1]
    if filename == decodedFullPath:
        filename = decodedFullPath.split("/")[-1]

    print(filename)

    event_path = os.path.join(app.config['ROOT_DIR'],selectedDate)
    writeTitleImagePathToSingleTXTFile(event_path,filename)


def initDateSelection():
    print("client connected. Init Date Selection")
    allDates = []   
    event_path = app.config['ROOT_DIR']
    for root,dirs,files in os.walk(event_path):
        allDates.append(dirs)

    emit('init_date_selection',{'data': str(allDates)}, broadcast=True)


def getEventFromJSONWhereDate(date):
    events = main_test.read_json('events.json', events='events')

    for event in events:
        event_date_str = event.get('date','')
        if event_date_str == date:
            event_cost = event.get('price', '')
            event_place = event.get('location', '')
            event_stadium = event.get('stadium', '')
            artist = event.get('artist', '')
            tour = event.get('tourname', '')

            return [event_date_str,event_cost,event_place,event_stadium,artist,tour]
    return None


def sortEventsDateDescending(events):
    return sorted(events, key=lambda x: datetime.datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)


def readTitleImagePathFromSingleTXTFile(eventpath):
    titleImagePath = ""
    filepath = os.path.join(eventpath,"title_image.txt")

    if not os.path.isfile(filepath):
        return ""
    f = open(filepath, "r") 
    titleImagePath = f.readlines()[0].replace("\n","")
    print("readTitleImage path:",titleImagePath)
    f.close()
    print("readTitleImage path:",titleImagePath)
    return titleImagePath

def writeTitleImagePathToSingleTXTFile(eventpath,imagepath):
    filepath = os.path.join(eventpath,"title_image.txt")
    

    f = open(filepath, "w") 
    f.write(imagepath)
    f.write('\n')
    f.close()


def selectSinglePathFromDir(date):
    event_path = os.path.join(app.config['ROOT_DIR'],date)
    path = readTitleImagePathFromSingleTXTFile(event_path)
    if path != "":
        path = encode(os.path.join(event_path,path))
        return path
    
    paths = getPathsFromDir(event_path)
    if len(paths) == 0:
        return ""
    else:
        print(paths[0])
        return paths[0]

def addTitleImagePathToEvents(events):
    for event in events:
        event['imgsrc'] = selectSinglePathFromDir(event['date'])
    return events

def getAllEventsFromJSON():
    events = main_test.read_json('events.json', events='events')
    dir(events)
    return events

def shortStringToLengthAddPoints(string,length):
    newstring = string[0:length] + "..."
    return newstring

def isStringLongerThanGivenLength(string,length):
    longer = len(string)>length
    return longer

def shortAllEventNamesToGivenLength(events,maxlength):
    for event in events:
        name = event['artist']
        if isStringLongerThanGivenLength(name,maxlength):
            event['artist'] = shortStringToLengthAddPoints(name,maxlength)
    return events

if __name__ == '__main__':
    #socketio.run(app,host="0.0.0.0",allow_unsafe_werkzeug=True,debug=True)
    app.run("0.0.0.0",debug=True)