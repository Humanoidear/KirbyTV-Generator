import datetime
import lxml.etree as ET
import importlib.util
import os
import sys
import shutil

# Configuration
uptime = 259200
startdate = 1752379200
startdateEX = 1752379200
enddate = startdate + uptime
dtformat = '%Y %m %d %H %M %S'

# Supported locales
SUPPORTED_LOCALES = ['en', 'es', 'it', 'fr']

def load_locale_module(locale_code):
    """Dynamically load locale module"""
    locale_path = f'./locales/{locale_code}/{locale_code}.py'
    
    if not os.path.exists(locale_path):
        print(f"Locale file not found: {locale_path}")
        return None
    
    spec = importlib.util.spec_from_file_location(f"locale_{locale_code}", locale_path)
    locale_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(locale_module)
    
    return locale_module

def process_locale(locale_code):
    """Process a single locale and generate its XML file"""
    print(f"Processing locale: {locale_code}")
    
    # Load locale module
    locale = load_locale_module(locale_code)
    if not locale:
        print(f"Failed to load locale: {locale_code}")
        return False
    
    # Get XML file path
    xmlfile = locale.get_xml_file_path()
    
    if not os.path.exists(xmlfile):
        print(f"XML file not found: {xmlfile}")
        return False
    
    # Parse XML
    parser = ET.XMLParser(strip_cdata=False)
    root = ET.parse(xmlfile, parser=parser)
    body = root.getroot()
    
    # Reset dates for this locale processing
    current_startdate = startdate
    current_enddate = enddate
    
    # Process episodes
    episodes = body.findall("episode_data")
    
    for episode in episodes:
        items = episode.findall("item")
        
        for item in items:
            item_id = item.get('id')
            if item_id == "1" or item_id == "2" or item_id == "3":
                tempstart = datetime.datetime.fromtimestamp(current_startdate).strftime(dtformat)
                tempend = datetime.datetime.fromtimestamp(current_enddate).strftime(dtformat)
                item.set("start_date", tempstart)
                item.set("end_date", tempend)
                current_enddate = current_enddate + uptime
                
                # Update video path with locale
                video_elem = item.find("video")
                if video_elem is not None:
                    current_path = video_elem.get("path")
                    if current_path and not current_path.startswith(f"{locale_code}/"):
                        # Extract episode number from path (e.g., "kirby1.mo" -> "1")
                        episode_num = current_path.replace("kirby", "").replace(".mo", "")
                        new_path = f"{locale_code}/kirby{episode_num}.mo"
                        video_elem.set("path", new_path)
                continue

            tempstart = datetime.datetime.fromtimestamp(current_startdate).strftime(dtformat)
            tempend = datetime.datetime.fromtimestamp(current_enddate).strftime(dtformat)
            item.set("start_date", tempstart)
            item.set("end_date", tempend)
            current_startdate = current_startdate + uptime
            current_enddate = current_enddate + uptime
            
            # Update video path with locale
            video_elem = item.find("video")
            if video_elem is not None:
                current_path = video_elem.get("path")
                if current_path and not current_path.startswith(f"{locale_code}/"):
                    # Extract episode number from path (e.g., "kirby1.mo" -> "1")
                    episode_num = current_path.replace("kirby", "").replace(".mo", "")
                    new_path = f"{locale_code}/kirby{episode_num}.mo"
                    video_elem.set("path", new_path)

    # Calculate dynamic text using locale functions
    final_enddate = current_enddate - uptime
    endtime = locale.format_date_with_ordinal(final_enddate)
    dayamnt = uptime * 4
    daycount = locale.deltaconv(dayamnt)
    dayc = locale.deltaconv(uptime)

    # Get localized dynamic text from locale module
    txtint2, txtint3 = locale.get_dynamic_text(dayc, endtime, daycount)

    # Update XML with dynamic text
    locales = body.findall("locale")

    for locale_elem in locales:
        units = locale_elem.findall('trans_unit')
        for trans_unit in units:
            unit_id = trans_unit.get('id')
            if unit_id == 'txt_intro_2':
                messages = trans_unit.findall('message')
                for message in messages:
                    targets = message.findall('target')
                    for target in targets:
                        target.text = ET.CDATA(txtint2)
            if unit_id == 'txt_intro_3':
                messages = trans_unit.findall('message')
                for message in messages:
                    targets = message.findall('target')
                    for target in targets:
                        target.text = ET.CDATA(txtint3)

    help_data_sections = body.findall("help_data")
    for help_data in help_data_sections:
        units = help_data.findall('.//trans_unit')
        for trans_unit in units:
            unit_id = trans_unit.get('id')
            if unit_id == 'channel_2':
                messages = trans_unit.findall('message')
                for message in messages:
                    targets = message.findall('target')
                    for target in targets:
                        target.text = ET.CDATA(txtint2)

    # Write the updated XML
    root.write(xmlfile, xml_declaration=True, encoding='utf-8')
    print(f"XML updated successfully: {xmlfile}")
    
    # Copy the generated XML file to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_filename = f"gb_config_{locale_code}.xml"
    output_path = os.path.join(script_dir, output_filename)
    
    try:
        shutil.copy2(xmlfile, output_path)
        print(f"XML copied to: {output_path}")
    except Exception as e:
        print(f"Failed to copy XML file: {e}")
        return False
    
    return True

def main():
    """Main function to process all locales"""
    print("Starting localized XML generation...")
    
    success_count = 0
    total_count = len(SUPPORTED_LOCALES)
    
    for locale_code in SUPPORTED_LOCALES:
        if process_locale(locale_code):
            success_count += 1
        print()  # Add blank line between locales
    
    print(f"Processing complete: {success_count}/{total_count} locales processed successfully")
    
    # Show the location of copied files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"\nGenerated XML files copied to: {script_dir}")

if __name__ == "__main__":
    main()