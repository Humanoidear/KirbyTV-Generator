# Italian locale functions and constants
LOCALE_CODE = "it"

def sing(amount, unit):
    if unit == "giorno":
        return f"{amount} {'giorno' if amount == 1 else 'giorni'}"
    elif unit == "ora":
        return f"{amount} {'ora' if amount == 1 else 'ore'}"
    elif unit == "minuto":
        return f"{amount} {'minuto' if amount == 1 else 'minuti'}"
    elif unit == "secondo":
        return f"{amount} {'secondo' if amount == 1 else 'secondi'}"
    else:
        return f"{amount} {unit}"

def deltaconv(seconds):
    mins, secs = divmod(seconds, 60)
    hrs, mins = divmod(mins, 60)
    dys, hrs = divmod(hrs, 24)
    timedict = {'giorno': dys, 'ora': hrs, 'minuto': mins, 'secondo': secs}
    cleaned = {k:v for k,v in timedict.items() if v != 0}
    return " ".join(sing(v,k) for k,v in cleaned.items())

def get_ordinal_suffix(day_str):
    return 'º'

def format_date_with_ordinal(timestamp):
    import datetime
    
    italian_months = {
        1: 'gennaio', 2: 'febbraio', 3: 'marzo', 4: 'aprile',
        5: 'maggio', 6: 'giugno', 7: 'luglio', 8: 'agosto',
        9: 'settembre', 10: 'ottobre', 11: 'novembre', 12: 'dicembre'
    }
    
    dt = datetime.datetime.fromtimestamp(timestamp)
    day = int(dt.strftime('%d'))
    month = italian_months[dt.month]
    year = dt.year
    
    return f'{day}º {month} {year}'

def get_dynamic_text(dayc, endtime, daycount):
    txtint2 = f'Gli episodi saranno rilasciati<br/>ogni {dayc}<br/>fino al {endtime}.'
    txtint3 = f'Gli episodi rimarranno disponibili<br/>per {daycount}. Controlla il Programma<br/>Episodi per vedere i prossimi<br/>episodi.'
    return txtint2, txtint3

def get_xml_file_path():
    return './locales/it/gb_config_it.xml'