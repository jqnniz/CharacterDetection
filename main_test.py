import datetime
import cv2
#import easyocr
from paddleocr import PaddleOCR
import json
from less_shit_parser import LessShitParser
from more_shit_parser import MoreShitParser
import glob
import os
from dateutil import parser



# Opening JSON file
def read_json(json_path, events):
    with open(json_path) as f:
        data = json.load(f)
    return data[events]


def get_text(image_path,useEasyOCR=True,usePaddleOCR=False):
    # if useEasyOCR:
    #     img = cv2.imread(image_path)
    #     reader = easyocr.Reader(['de'], gpu=True)
    #     results = reader.readtext(img)
    #     text = [result[1] for result in results]
    #     return text
    if usePaddleOCR:
        ocr = PaddleOCR(lang='de')
        result = ocr.ocr(image_path)
        text = [result[1][0] for result in result[0]]
        return text


def get_all_dates(parsed_date=False):
    events = read_json('events.json', events='events')

    # Extract and parse dates from the JSON events
    event_dates = []
    for event in events:
        event_date_str = event.get('date', '')
        event_cost = event.get('cost', '')
        event_place = event.get('place', '')
        event_name = event.get('name', '')
        
        #parsed_date = parser.parse(event_date_str, dayfirst=True, fuzzy=True)
        #if parsed_date:
        event_dates.append([event_date_str, event_cost, event_place, event_name])
    return event_dates


def get_text_from_image(text):
    for t in text:
        bbox, text_temp, score = t
        if text_temp:
            return text_temp
    return None


def get_matching_date(detected_date, event_dates):
    for date_str, cost, place, name in event_dates:
        date = parser.parse(date_str, dayfirst=True, fuzzy=True)
        if detected_date.date() == date.date(): # and detected_date.time() == date.time():
            print(f"Matching event found: {cost}")
            print(f"Matching event found: {place}")
            print(f"Matching event found: {name}")
            return date, place + " " + name
    return None


def main():
    #text = get_text("images/date01.jpeg",True,False)
    list_of_files = glob.glob('uploads/*') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    print(latest_file)
    text = get_text(latest_file,False,True)


    print(text)
    detected_date_02 = MoreShitParser.shit_parse(text)
    detected_date_01 = "" #LessShitParser.shit_parse_nlp(text)

   # print(detected_date_01, detected_date_02)   
    print(detected_date_02)


    if detected_date_01 or detected_date_02:
        all_dates = get_all_dates()
        matching_date, event = get_matching_date(detected_date_02, all_dates)
        if matching_date:
            print(f"Matching date: {matching_date}")
        else:
            print("No matching date found")
    else:
        print("No date detected in the image")

    return matching_date,event



if __name__ == '__main__':
    main()
