from dateutil import parser
import re

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
#pattern erkennt DD.MM.YYYY
#pattern erkennt DD.MM.YY
#pattern erkennt DD-MM-YYYY
#pattern erkennt DD-MM-YY
pattern = r'^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$'



months_pattern = '|'.join([month[0] for month in months])


def replace_month_abbr_with_num(date_str):
    # Replace all month abbreviations with their numeric equivalents
    for month_abbr, month_num in months:
        date_str = re.sub(r'\b' + month_abbr + r'\b', month_num, date_str)
    return date_str


def preprocess(inputs):
    output = []
    for input in inputs:
        if "," in input:
            i = input.split(",")
            for elem in i:
                output.append(elem.strip())
        else:
            output.append(input)
        if " " in input:
            i = input.split(" ")
            for elem in i:
                output.append(elem.strip())
        else:
            output.append(input)

    return output


def shit_parse(date_str):
    inputs = preprocess(date_str)
    for input in inputs:
        dateFound = False

        result = re.compile(pattern)
        r = result.match(input[0:10])
        if r:

            try:
                parsed_date = parser.parse(r.group(0), dayfirst=True, fuzzy=True)
                dateFound = True
            except ValueError:
                dateFound = False
        else:
            r = result.match(input[0:8])
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
            #formatted_date = parsed_date.strftime('%Y-%m-%d')


            # Format the parsed date as DD/MM/YYYY
            return parsed_date
    return None