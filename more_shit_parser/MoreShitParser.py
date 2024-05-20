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

months_pattern = '|'.join([month[0] for month in months])


def replace_month_abbr_with_num(date_str):
    # Replace all month abbreviations with their numeric equivalents
    for month_abbr, month_num in months:
        date_str = re.sub(r'\b' + month_abbr + r'\b', month_num, date_str)
    return date_str


def shit_parse(date_str):
    try:
        # Replace month abbreviations with their numeric equivalents
        date_str = replace_month_abbr_with_num(date_str)

        # Parse the date string with dayfirst=True
        parsed_date = parser.parse(date_str, dayfirst=True, fuzzy=True)

        # Format the parsed date as DD/MM/YYYY
        formatted_date = parsed_date.strftime('%d/%m/%Y')
        return formatted_date
    except ValueError:
        return None