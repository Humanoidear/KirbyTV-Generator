# Spanish locale functions and constants
LOCALE_CODE = "es"

def sing(amount, unit):
    """Singularizer - returns a string containing the amount 
    and type of something. The type/unit of item will be pluralized
    if the amount is greater than one."""
    if amount == 1:
        return f"{amount} {unit}"
    
    # Basic Spanish pluralization
    if unit.endswith('a') or unit.endswith('e') or unit.endswith('o'):
        return f"{amount} {unit}s"
    elif unit.endswith('z'):
        return f"{amount} {unit[:-1]}ces"
    else:
        return f"{amount} {unit}s"

def deltaconv(seconds):
    """Converts a timedelta's total_seconds() to a humanized string."""
    mins, secs = divmod(seconds, 60)
    hrs, mins = divmod(mins, 60)
    dys, hrs = divmod(hrs, 24)
    
    # Spanish time units
    timedict = {'día': dys, 'hora': hrs, 'minuto': mins, 'segundo': secs}
    cleaned = {k:v for k,v in timedict.items() if v != 0}
    return " ".join(sing(v,k) for k,v in cleaned.items())

def get_ordinal_suffix(day_str):
    """Returns the appropriate ordinal format for Spanish (no suffix needed)"""
    return ''  # Spanish doesn't use ordinal suffixes

def format_date_with_ordinal(timestamp):
    """Formats date in Spanish format"""
    import datetime
    dt = datetime.datetime.fromtimestamp(timestamp)
    
    # Spanish month names
    spanish_months = [
        'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
        'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
    ]
    
    day = dt.day
    month = spanish_months[dt.month - 1]
    year = dt.year
    
    return f'{day} de {month} de {year}'

def get_dynamic_text(dayc, endtime, daycount):
    """Returns the localized dynamic text for txt_intro_2 and txt_intro_3"""
    txtint2 = f'Los episodios se publicarán<br/>cada {dayc}<br/>hasta el {endtime}.'
    txtint3 = f'Los episodios permanecerán disponibles<br/>por {daycount}. Revisa el Horario<br/>de Episodios para ver los próximos<br/>episodios.'
    return txtint2, txtint3

def get_xml_file_path():
    """Returns the path to the XML file for this locale"""
    return './locales/es/gb_config_es.xml'
