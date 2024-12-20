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
artists = None

UPLOAD_FOLDER = 'uploads'
ROOT_DIR = 'events'
app = Flask(__name__)
#            static_url_path='',
#            static_folder='/static')
app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ROOT_DIR'] = ROOT_DIR
app.config['IMAGE_EXTS'] = [".png", ".jpg", ".jpeg", ".gif", ".tiff",".mp4",".JPG"]
socketio = SocketIO(app)

def encode(x):
    return binascii.hexlify(x.encode('utf-8')).decode()

def decode(x):
    return binascii.unhexlify(x.encode('utf-8')).decode()


@app.route('/')
def index():
    global artists
    events = getAllEventsFromJSON()
    events = sortEventsDateDescending(events)
    events = addTitleImagePathToEvents(events)
    maxCharacterCountEventTitle = 16
    events = shortAllEventNamesToGivenLength(events,maxCharacterCountEventTitle)

    statistic,locations,artists = getEventsMetaInformation(events)

    return render_template('index.html', events=events, statistic=statistic,locations=locations,artists=artists.items())

@app.route('/', methods=['POST'])
def upload_file():
    global selectedDate
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        files = request.files.getlist("file") 
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        for file in files:
            print(file)
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
            image_paths,video_paths=getPathsFromDir(event_path)
        return render_template('gallery.html', paths=image_paths, date=selectedDate)

    return

@app.route('/newevent', methods=['POST'])
def create_new_event():
    print(dir(request))
    print(request.args.get("event-date"))

    return
def getPathsFromDir(dir):
    image_paths = []
    video_paths = []
    for root,dirs,files in os.walk(dir):
        for file in files:
            if any(file.endswith(ext) for ext in app.config['IMAGE_EXTS']):
                    if file.endswith(".mp4"):
                        video_paths.append(encode(os.path.join(root,file)))
                    else:
                        image_paths.append(encode(os.path.join(root,file)))

    return image_paths,video_paths

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
                     'tourname': request.args.get("event-tourname"),
                     'entfernung': getEntfernungFromCities("Bitterfeld",request.args.get("event-location"))
        }
        events = main_test.read_json('events.json', events='events')

        events.append(newevent)

        main_test.write_json('events.json', events=events)

        event_path = os.path.join(app.config['ROOT_DIR'],selectedDate)

        if not os.path.exists(event_path):
            os.mkdir(event_path) 

        image_paths,_=getPathsFromDir(event_path)
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
        image_paths,video_paths=getPathsFromDir(event_path)


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
            target = "Bitterfeld"
            destination = event[2]
            entfernung = getEntfernungFromCities(target,destination)

            return render_template('gallery.html', paths=image_paths,video_paths=video_paths, date=event[0],price=event[1],ort=event[2],stadium=event[3],artist=event[4],tour=event[5],days_offset=delta,Entfernung=entfernung)


@app.route('/cdn/<path:filepath>')
def download_file(filepath):
    dir,filename = os.path.split(decode(filepath))
    return send_from_directory(dir, filename, as_attachment=False)

@socketio.on('init_connection')
def init_connection(message):
    global artists
    initDateSelection()
    #json.dump(list(session_ls), fp)
    a = list(artists)
    emit('artist_values', {'artists': a}, broadcast=True)

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

def getEntfernungFromCities(target,destination):
    try:
        from geopy.distance import geodesic as GD
        from geopy.geocoders import Nominatim


        city1 = target
        city2 = destination

        geolocator = Nominatim(user_agent="MyApp")

        location_city1 = geolocator.geocode(city1)
        location_city2 = geolocator.geocode(city2)

        lat_long_city1 = (location_city1.latitude ,location_city1.longitude)
        lat_long_city2 = (location_city2.latitude ,location_city2.longitude)

        distance = GD(lat_long_city1 , lat_long_city2).km
        entfernung = round(distance,2)
        print(f"The distance between {city1} and {city2} is { distance}")
    except:
        entfernung = ''

    return entfernung

def getEventPlaceWithoutSponsorName(event_place):

    # read json 
    arena_leipzig = ["quarterback immobilien arena","arena leipzig","arena","quarterback-immobilien-arena"]
    if event_place.lower() in arena_leipzig:
        return "Leipzig Arena"

    arena_berlin = ["o2 world","mercedes-benz-arena","uber-arena","uber arena",]
    if event_place.lower() in arena_berlin:
        return "Mercedes-Benz-Arena"

    return event_place

def getEventsMetaInformation(events):
    locations = []
    preis_total = 0.0
    statistic = []  
    #[
    #{"name": "Sandrine",  "score": 100},
    #{"name": "Gergeley", "score": 87},
    #{"name": "Frieda", "score": 92},
    #]
    locations_verteilung = {}
    artist_verteilung = {}
    for event in events:
        event_place = event.get('stadium', '')
        event_place = getEventPlaceWithoutSponsorName(event_place)
        if event_place.lower() not in locations:
            locations.append(event_place.lower())

        if event_place in locations_verteilung:
            locations_verteilung[event_place] = locations_verteilung[event_place] + 1
        else:
            locations_verteilung[event_place] = 1

        event_artist = event.get('artist', '')
        if event_artist in artist_verteilung:
            artist_verteilung[event_artist] = artist_verteilung[event_artist] + 1
        else:
            artist_verteilung[event_artist] = 1
        event_price = event.get('price', 0)
        preis_total = preis_total + float(event_price)
    name = 'Konzerte'
    value = len(events)
    statistic.append({'name': name,'value':value})
    name = 'Locations'
    value = len(locations)
    statistic.append({'name': name,'value':value})
    name = 'Gesamtpreis'
    value = str(round(preis_total,2)) + " €"
    statistic.append({'name': name,'value':value})
    name = 'Durchschnittspreis'
    value = str(round(preis_total/len(events),2)) + " €"
    statistic.append({'name': name,'value':value})
    name = 'Entfernung'
    value = "- km"
    statistic.append({'name': name,'value':value}) 


    locations_verteilung = dict(sorted(locations_verteilung.items(), key=lambda item: item[1],reverse=True))
    locations_verteilung = removeKeysFromDictIfTotalCountGreaterThan(locations_verteilung,12)
    print(locations_verteilung)
    artist_verteilung = dict(sorted(artist_verteilung.items(), key=lambda item: item[1],reverse=True))
    artist_verteilung = removeKeysFromDictIfTotalCountGreaterThan(artist_verteilung,12)
    print(artist_verteilung)
    #data['preis_total'] = str(round(preis_total,2)) + " €"
    #data['entfernung_total'] = "- km"
    #data['konzerte_total'] = len(events)
    #data['locations_total'] = len(locations)
    print(statistic)
    return statistic,locations_verteilung.items(),artist_verteilung


def removeKeysFromDictIfTotalCountGreaterThan(dict,maxcount):
    counter = 0
    for k in list(dict.keys()):
        if counter >= maxcount:
            dict.pop(k, None)   
        counter = counter + 1
    return dict

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
    
    paths,_ = getPathsFromDir(event_path)
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