from dateutil import parser

import re

dest = "2019-11-18"

inputs = ['Montag , 18.Nov.19, 20-00 Uhr',
          'Montag , 18 Nov.19, 20-00 Uhr',
            'Montag  18 Nov 19, 20-00 Uhr',
            '18.11.2019',
            '18.11.19, 20-00 Uhr',
            '18.11.19',
            '18-11-19',
            '18/11/19',
            'Montag , 18.Nov.19',
            '18.11.19, 20-00 Uhr',
            'NOVEMBER 18 2019',
            'NovEMBER 18 2019',
            'Montag.18.Nov.19,20:00Uhr'
]


dest_count = len(inputs)


months = [
        ["Jan", "01"],
        ["Feb", "02"],
        ["Mar", "03"],
        ["Mrz", "03"],  # German abbreviation for March
        ["Apr", "04"],
        ["May", "05"],
        ["Jun", "06"],
        ["Jul", "07"],
        ["Aug", "08"],
        ["Sep", "09"],
        ["Oct", "10"],
        ["Nov", "11"],
        ["Dec", "12"]
    ]



def preprocess(inputs):
    output = []
    for input in inputs:
        if "," in input:
            i = input.split(",")
            for elem in i:
                output.append(elem.strip())
        else:
            output.append(input)

    return output

#pattern erkennt DD.MM.YYYY
#pattern erkennt DD.MM.YY
#pattern erkennt DD-MM-YYYY
#pattern erkennt DD-MM-YY
pattern = r'^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$'


inputs = preprocess(inputs)
found_dates = 0
for input in inputs:
    print("########################")
    print("parsing date input: ", input)
    dateFound = False

    #regex = re.compile(pattern)
    #m = regex.match(input)
    result = re.compile(pattern)
    r = result.match(input)
    print(r)
    if r:

        try:
            parsed_date = parser.parse(r.group(0), dayfirst=True, fuzzy=True)
            dateFound = True
        except ValueError:
            dateFound = False
    else:

        for abbr,abbr_num in months:
            if abbr in input or abbr.upper() in input:
                print("detected month")
                print(abbr)

                input.replace(abbr,abbr_num)

                print(input)

                try:
                    parsed_date = parser.parse(input, dayfirst=True, fuzzy=True)
                    dateFound = True
                except ValueError:
                    dateFound = False
                

    if dateFound:
        print(parsed_date)
        formatted_date = parsed_date.strftime('%Y-%m-%d')
        print(formatted_date)

        if formatted_date == dest:
            
            found_dates = found_dates + 1
            print("success")

        formatted_date = ""
        parsed_date = ""


print(found_dates,dest_count)