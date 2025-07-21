LOCALE_CODE = "fr"

def sing(amount, unit):

    if amount == 1:
        return f"{amount} {unit}"
    
    # French pluralization rules (stupid)
    if unit.endswith('s') or unit.endswith('x') or unit.endswith('z'):
        return f"{amount} {unit}"  # No change for words ending in s, x, z
    elif unit.endswith('eau') or unit.endswith('eu'):
        return f"{amount} {unit}x"  # Add x for words ending in eau/eu
    elif unit.endswith('al'):
        return f"{amount} {unit[:-2]}aux"  # al -> aux
    else:
        return f"{amount} {unit}s"  # Default: add s

def deltaconv(seconds):
    """Converts a timedelta's total_seconds() to a humanized string."""
    mins, secs = divmod(seconds, 60)
    hrs, mins = divmod(mins, 60)
    dys, hrs = divmod(hrs, 24)
    
    timedict = {'jour': dys, 'heure': hrs, 'minute': mins, 'seconde': secs}
    cleaned = {k:v for k,v in timedict.items() if v != 0}
    return " ".join(sing(v,k) for k,v in cleaned.items())

def get_ordinal_suffix(day_str):
    day = int(day_str)
    if day == 1:
        return 'er'  # 1er (premier)
    else:
        return ''  # No suffix for other numbers

def format_date_with_ordinal(timestamp):
    import datetime
    dt = datetime.datetime.fromtimestamp(timestamp)
    
    french_months = [
        'janvier', 'février', 'mars', 'avril', 'mai', 'juin',
        'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'
    ]
    
    day = dt.day
    month = french_months[dt.month - 1]
    year = dt.year
    
    if day == 1:
        return f'1er {month} {year}'
    else:
        return f'{day} {month} {year}'

def get_dynamic_text(dayc, endtime, daycount):
    """Returns the localized dynamic text for txt_intro_2 and txt_intro_3"""
    txtint2 = f'Les épisodes sortiront<br/>tous les {dayc} jusqu\'au<br/>{endtime}.'
    txtint3 = f'Les épisodes resteront disponibles pendant {daycount}. Vérifiez le programme pour voir les épisodes à venir.'
    return txtint2, txtint3

def get_xml_file_path():
    return './locales/fr/gb_config_fr.xml'
