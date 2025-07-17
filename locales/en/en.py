# English locale functions and constants
LOCALE_CODE = "en"

def sing(amount, unit):
    """Singularizer - returns a string containing the amount 
    and type of something. The type/unit of item will be pluralized
    if the amount is greater than one."""
    return f"{amount} {amount == 1 and f'{unit}' or f'{unit}s'}"

def deltaconv(seconds):
    """Converts a timedelta's total_seconds() to a humanized string."""
    mins, secs = divmod(seconds, 60)
    hrs, mins = divmod(mins, 60)
    dys, hrs = divmod(hrs, 24)
    timedict = {'day': dys, 'hour': hrs, 'minute': mins, 'second': secs}
    cleaned = {k:v for k,v in timedict.items() if v != 0}
    return " ".join(sing(v,k) for k,v in cleaned.items())

def get_ordinal_suffix(day_str):
    """Returns the appropriate ordinal suffix for English"""
    st = ['01', '21', '31']
    nd = ['02', '22']
    rd = ['03', '23']
    
    if day_str in st:
        return 'st'
    elif day_str in nd:
        return 'nd'
    elif day_str in rd:
        return 'rd'
    else:
        return 'th'

def format_date_with_ordinal(timestamp):
    """Formats date with English ordinal suffix"""
    import datetime
    dt = datetime.datetime.fromtimestamp(timestamp)
    day_str = dt.strftime('%d')
    suffix = get_ordinal_suffix(day_str)
    return dt.strftime(f'%d{suffix} of %B, %Y')

def get_dynamic_text(dayc, endtime, daycount):
    """Returns the localized dynamic text for txt_intro_2 and txt_intro_3"""
    txtint2 = f'Episodes will be released<br/>every {dayc}<br/>until {endtime}.'
    txtint3 = f'Episodes will remain available<br/>for {daycount}. Check the Episode<br/>Timetable to view upcoming<br/>episodes.'
    return txtint2, txtint3

def get_xml_file_path():
    """Returns the path to the XML file for this locale"""
    return './locales/en/gb_config_en.xml'
