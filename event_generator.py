import json
import re # Added for regex-based JSON extraction
import requests
import os
import hashlib
from datetime import datetime # Correct import
from icalendar import Calendar, Event
import google.generativeai as genai # Added for actual Gemini API calls
# import pytz # Not in requirements, will remove for now

SHEET_URL = 'https://docs.google.com/spreadsheets/d/1Lk8Lq5gu-nI1dwZjWZqYM05-x4E-5kD_huPsW-28AMo/gviz/tq'
PROCESSED_PROMPTS_FILE = 'processed_prompts.txt'
OUTPUT_ICS_FILE = 'generated_events.ics' # Will be phased out for individual files
CLUB_SCHEDULES_DIR = 'club_schedules'
PROVINCE_TIMEZONES = {
    "Alberta": "America/Edmonton", "British Columbia": "America/Vancouver", "Manitoba": "America/Winnipeg",
    "New Brunswick": "America/Moncton", "Newfoundland and Labrador": "America/St_Johns", "Nova Scotia": "America/Halifax",
    "Ontario": "America/Toronto", "Prince Edward Island": "America/Halifax", "Quebec": "America/Montreal",
    "Saskatchewan": "America/Regina", "Northwest Territories": "America/Yellowknife", "Nunavut": "America/Iqaluit",
    "Yukon": "America/Whitehorse"
}
DEFAULT_TIMEZONE = "America/Toronto"

def fetch_sheet_data(url):
    try:
        response = requests.get(url, timeout=30) # Increased timeout
        response.raise_for_status()
        text = response.text
        print(f"Debug: Raw sheet response text (first 500 chars): {text[:500]}")

        # Try to match the typical Google Sheets gviz response pattern
        match = re.search(r"google\.visualization\.Query\.setResponse\s*\((.*)\)\s*;", text, re.DOTALL)
        if match:
            json_string = match.group(1)
        else:
            # Fallback for simpler JSON responses or if the main pattern isn't found
            first_brace = text.find('{')
            last_brace = text.rfind('}')
            if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
                json_string = text[first_brace : last_brace+1]
            else:
                print("Error: Could not find JSON object in response using regex or fallback.")
                return None

        json_string = json_string.strip() # Ensure no leading/trailing whitespace
        return json.loads(json_string)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching sheet data: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON data: {e}")
        return None

def parse_club_data(raw_data):
    if not raw_data or 'table' not in raw_data or 'cols' not in raw_data['table'] or 'rows' not in raw_data['table']:
        print("Error: Invalid raw data structure for parsing.")
        return []

    headers = []
    # Ensure 'label' exists and is a string, provide a default unique name if not
    for i, col_def in enumerate(raw_data['table']['cols']):
        headers.append(col_def.get('label', f'col_{i}').strip())


    # This mapping helps standardize some common names, but all columns will be preserved with original names too
    header_map = {
        'Sport Type': 'SportType', 'Sport Type FR': 'SportTypeFR',
        'Province': 'Province', 'Province FR': 'ProvinceFR',
        'Club Name': 'ClubName', 'Club Name FR': 'ClubNameFR',
        'City': 'City', 'City FR': 'CityFR',
        'Practice Location': 'PracticeLocation', 'Practice Location FR': 'PracticeLocationFR',
        'Practice Times': 'PracticeTimes', 'Practice Times FR': 'PracticeTimesFR',
        'Contact Email': 'ContactEmail',
        'Website URL': 'WebsiteURL', 'Facebook URL': 'FacebookURL', 'Instagram URL': 'InstagramURL',
        'Notes': 'Notes', 'Notes FR': 'NotesFR',
        'RRULE': 'RRULE'
    }

    parsed_events = []
    for row_idx, row_data in enumerate(raw_data['table']['rows']):
        if not row_data or 'c' not in row_data:
            print(f"Warning: Skipping empty or invalid row {row_idx}.")
            continue

        event = {}
        cells = row_data['c']

        for i, cell in enumerate(cells):
            if i < len(headers):
                header_name = headers[i]
                cell_value = cell.get('v', None) if cell else None

                # Store all values based on actual header names from the sheet
                event[header_name] = str(cell_value) if cell_value is not None else ""

                # Also map to simplified/standardized keys if they exist in header_map
                if header_name in header_map:
                    event[header_map[header_name]] = str(cell_value) if cell_value is not None else ""

        # Add event if it has at least some data, particularly a Club Name or RRULE
        if event.get('ClubName') or event.get('RRULE'):
             # Ensure essential fields for fingerprinting exist, even if empty, to prevent KeyErrors
            for key_to_check in ['ClubName', 'RRULE', 'PracticeTimes', 'PracticeLocation']:
                if key_to_check not in event: # Check if the mapped key is missing
                    # Try to find original header if mapping was the issue, or default to empty
                    original_header_for_key = next((h for h,m in header_map.items() if m == key_to_check), None)
                    if original_header_for_key and original_header_for_key in event:
                         event[key_to_check] = event[original_header_for_key]
                    else:
                        event[key_to_check] = "" # Default to empty string
            parsed_events.append(event)
        elif cells and any(c.get('v') for c in cells if c): # If cells have values but no ClubName/RRULE
            # print(f"Warning: Skipping row {row_idx} due to missing Club Name and RRULE, but has data: { {headers[i]: (cells[i].get('v') if cells[i] else None) for i in range(len(cells))} }")
            pass # Reduce noise for now

    return parsed_events

def load_processed_prompts(filepath):
    if not os.path.exists(filepath):
        return set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return {line.strip() for line in f if line.strip()} # Ensure no empty lines are added
    except IOError as e:
        print(f"Error loading processed prompts: {e}")
        return set()

def save_processed_prompt(filepath, fingerprint):
    try:
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(fingerprint + '\n')
    except IOError as e:
        print(f"Error saving processed prompt: {e}")

def get_event_fingerprint(event_data):
    # Use standardized keys for fingerprinting
    # Use standardized keys for fingerprinting
    club_name = event_data.get('ClubName', '')
    rrule = event_data.get('RRULE', '') # This is the RRULE from the sheet
    practice_times = event_data.get('PracticeTimes', '')
    location = event_data.get('PracticeLocation', '')
    notes = event_data.get('Notes', '')
    notes_fr = event_data.get('NotesFR', '')

    # Fallback to original headers if mapped ones are empty and original exists
    if not club_name and 'Club Name' in event_data: club_name = event_data['Club Name']
    # RRULE from sheet is intentionally kept in fingerprint to detect sheet changes
    if not rrule and 'RRULE' in event_data: rrule = event_data['RRULE']
    if not practice_times and 'Practice Times' in event_data: practice_times = event_data['Practice Times']
    if not location and 'Practice Location' in event_data: location = event_data['Practice Location']
    if not notes and 'Notes' in event_data: notes = event_data['Notes'] # Check original 'Notes'
    if not notes_fr and 'Notes FR' in event_data: notes_fr = event_data['Notes FR'] # Check original 'Notes FR'

    fingerprint_str = f"{club_name}|{rrule}|{practice_times}|{location}|{notes}|{notes_fr}"
    return hashlib.sha256(fingerprint_str.encode('utf-8')).hexdigest()

def sanitize_filename(name):
    # Remove characters that are not alphanumeric, underscore, or hyphen
    name = re.sub(r'[^\w\s-]', '', name).strip()
    # Replace spaces and multiple hyphens with a single underscore
    name = re.sub(r'[-\s]+', '_', name)
    return name if name else "unnamed_club"

def generate_gemini_prompt(event_data):
    club_name = event_data.get('ClubName', event_data.get('Club Name', 'N/A'))
    club_name_fr = event_data.get('ClubNameFR', event_data.get('Club Name FR', club_name))

    location = event_data.get('PracticeLocation', event_data.get('Practice Location', 'N/A'))
    location_fr = event_data.get('PracticeLocationFR', event_data.get('Practice Location FR', location))

    desc_en_parts = []
    pt_en = event_data.get('PracticeTimes', event_data.get('Practice Times', ''))
    if pt_en: desc_en_parts.append(f"Times: {pt_en}")
    notes_en = event_data.get('Notes', event_data.get('Notes', ''))
    if notes_en: desc_en_parts.append(f"Notes: {notes_en}")
    full_description_en = ". ".join(desc_en_parts)

    desc_fr_parts = []
    pt_fr = event_data.get('PracticeTimesFR', event_data.get('Practice Times FR', ''))
    if pt_fr: desc_fr_parts.append(f"Horaires: {pt_fr}")
    notes_fr = event_data.get('NotesFR', event_data.get('Notes FR', ''))
    if notes_fr: desc_fr_parts.append(f"Remarques: {notes_fr}")
    full_description_fr = ". ".join(desc_fr_parts)

    # Ensure description is not empty, use a placeholder if all parts are empty
    final_description_en = full_description_en if full_description_en else "No specific details provided."
    final_description_fr = full_description_fr if full_description_fr else "Aucun détail spécifique fourni."

    province = event_data.get('Province', event_data.get('Province', ''))
    timezone = PROVINCE_TIMEZONES.get(province, DEFAULT_TIMEZONE)

    # The 'rrule' variable from the sheet is intentionally not used in this prompt template anymore.
    # Gemini is expected to infer recurrence from the descriptive text.

    prompt = f"""
Please generate one or more valid iCalendar VEVENT components based on the following details.
If the event details suggest multiple distinct schedules (e.g., different days or times for different activities under the same club, if clearly specified as separate), create a separate VEVENT for each.
If the details describe a single repeating event, create one VEVENT.

Event Details:
- Primary Language Name: {club_name}
- French Language Name: {club_name_fr}
- Primary Location: {location}
- French Location: {location_fr}
- Primary Description: {final_description_en}
- French Description: {final_description_fr}
- Timezone: {timezone}

Instructions for VEVENT generation:
1.  SUMMARY: Use "{club_name}" as the primary summary. If French name is different and available ("{club_name_fr}"), consider it.
2.  LOCATION: Use "{location}". If French location is different and available ("{location_fr}"), consider it.
3.  DESCRIPTION: Combine English and French descriptions. Example: "EN: {final_description_en}\nFR: {final_description_fr}". If one is empty, use the other.
4.  RECURRENCE (RRULE): Based on the event details provided (such as practice times, descriptions, name), determine if the event is recurring.
    - If recurrence can be clearly inferred (e.g., "Practices every Tuesday at 7pm", "Weekly club meeting"), generate the appropriate iCalendar RRULE property.
    - If the event seems to be a one-time occurrence or if recurrence cannot be reliably determined from the provided text, DO NOT include an RRULE property. In such cases, generate a single event.
    - Do NOT attempt to parse any RRULE string that might have been inadvertently included in the description fields; generate recurrence solely from the general event information.
5.  DTSTART / DTEND: Must be in floating local time with a TZID parameter (e.g., DTSTART;TZID={timezone}:YYYYMMDDTHHMMSS).
    - If an RRULE is generated, DTSTART should be the first occurrence of the event from today or in the near future.
    - If no RRULE is generated (one-time event), DTSTART should be the specific date and time of the event. If only time is mentioned (e.g. "practice at 7pm tonight"), assume it's for today or the nearest upcoming day that matches description.
    - Duration is typically 1-2 hours for practices; if not specified, assume 1 hour. Infer duration from text if possible (e.g., "7pm-9pm").
6.  UID: Generate a unique UID for each VEVENT (e.g., using a UUID or a hash).
7.  DTSTAMP: Set to the current UTC time when you generate this.
8.  Output Format: Provide ONLY the VEVENT block(s), each starting with BEGIN:VEVENT and ending with END:VEVENT. If multiple VEVENTs, list them sequentially. Do not include any other text, explanations, or markdown.

Example of a single VEVENT:
BEGIN:VEVENT
UID:some-unique-id@example.com
DTSTAMP:YYYYMMDDTHHMMSSZ
SUMMARY:Event Name
DTSTART;TZID=America/Toronto:YYYYMMDDTHHMMSS
DTEND;TZID=America/Toronto:YYYYMMDDTHHMMSS
RRULE:FREQ=WEEKLY;BYDAY=TU;INTERVAL=1
LOCATION:Event Location
DESCRIPTION:EN: English description.\nFR: French description.
END:VEVENT

If sufficient information (like practice times or clear event nature) is not available to determine specific dates/times or the general nature of the event, do not generate a VEVENT. Instead, output: "Error: Insufficient information to generate a calendar event for '{club_name}'."
"""
    return prompt.strip()

def call_gemini_api(prompt, api_key):
    if not api_key:
        print("Warning: GEMINI_API_KEY not provided. Skipping actual Gemini call.")
        # Fallback to a mock response or error, similar to before but clearly indicating no API call was made
        summary_mock = "Mock Event (No API Key)"
        for line in prompt.splitlines():
            if "Primary Language Name:" in line:
                summary_mock = line.split("Primary Language Name:")[1].strip()
                break
        if "Error: Invalid or unusable RRULE" in prompt:
             return f"Error: Invalid or unusable RRULE for event '{summary_mock}' (No API Key)."
        return f"BEGIN:VEVENT\nUID:no-api-key-{hashlib.sha1(prompt.encode()).hexdigest()}@cuga.example.com\nDTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}\nSUMMARY:{summary_mock}\nDTSTART;TZID=America/Toronto:20240101T120000\nDTEND;TZID=America/Toronto:20240101T130000\nDESCRIPTION:Mock event due to missing API key.\nEND:VEVENT"

    try:
        print(f"--- Calling Gemini API ---")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro') # Using gemini-pro, ensure this model is available/correct

        # Safety settings to try and prevent Gemini from refusing to answer
        # These are quite permissive, adjust as needed based on observed refusals
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]

        response = model.generate_content(prompt, safety_settings=safety_settings)

        # print(f"Gemini Raw Response Parts: {response.parts}")
        # print(f"Gemini Prompt Feedback: {response.prompt_feedback}")

        if response.parts:
            # Assuming the first part contains the text response we need.
            # Iterate through parts to find text, as sometimes there might be non-text parts.
            vevent_text_parts = []
            for part in response.parts:
                if hasattr(part, 'text'):
                    vevent_text_parts.append(part.text)

            if not vevent_text_parts:
                # This case might happen if Gemini finishes for a reason like safety, but doesn't raise an explicit error.
                # Check prompt_feedback for blockages.
                if response.prompt_feedback and response.prompt_feedback.block_reason:
                    block_reason = response.prompt_feedback.block_reason
                    print(f"Warning: Gemini API call blocked. Reason: {block_reason}")
                    # Try to get the categories that caused blocking
                    blocked_categories = [rating.category for rating in response.prompt_feedback.safety_ratings if rating.blocked]
                    print(f"Blocked categories: {blocked_categories}")
                    return f"Error: Gemini API call blocked due to {block_reason}. Categories: {blocked_categories}"
                else:
                    print(f"Warning: Gemini API call returned no text parts. Full response: {response}")
                    return "Error: Gemini API call returned no text parts."

            final_vevent_text = "".join(vevent_text_parts)
            # print(f"Gemini VEVENT Output:\n{final_vevent_text[:300]}...") # Log snippet of response
            return final_vevent_text.strip()
        elif response.prompt_feedback and response.prompt_feedback.block_reason:
            # Handle cases where response might be empty but feedback indicates blocking
            block_reason = response.prompt_feedback.block_reason
            blocked_categories = [rating.category for rating in response.prompt_feedback.safety_ratings if rating.blocked]
            print(f"Warning: Gemini API call blocked. Reason: {block_reason}. Categories: {blocked_categories}")
            return f"Error: Gemini API call blocked due to {block_reason}. Categories: {blocked_categories}"
        else:
            # This handles other cases where there are no parts and no explicit block reason in prompt_feedback
            # It could be an empty response for other reasons.
            print(f"Warning: Gemini API call returned no usable parts and no explicit block reason. Full response: {response}")
            return "Error: Gemini API call returned an empty or unusable response."

    except genai.types.BlockedPromptException as e: # More specific exception for blocked prompts
        print(f"Error: Gemini API call failed because the prompt was blocked: {e}")
        return f"Error: Gemini API call failed - Prompt Blocked: {e}"
    except genai.types.StopCandidateException as e: # Handles cases where generation stops unexpectedly
        print(f"Error: Gemini API call failed because generation stopped unexpectedly: {e}")
        return f"Error: Gemini API call failed - Generation Stopped: {e}"
    except requests.exceptions.RequestException as e: # Handles network-type errors for the underlying requests library used by genai
        print(f"Error: Gemini API call failed due to a network issue: {e}")
        return f"Error: Gemini API call failed - Network Issue: {e}"
    except Exception as e:
        # Catching google.api_core.exceptions.PermissionDenied (403) or other specific API errors might be useful here
        # For now, a general exception to catch unexpected issues.
        print(f"Error calling Gemini API: {e}")
        # Check if the error object has more details, e.g. response code
        error_details = str(e)
        if hasattr(e, 'grpc_status_code'): # Example for gRPC errors
            error_details += f" (gRPC status: {e.grpc_status_code})"
        elif hasattr(e, 'response') and hasattr(e.response, 'status_code'): # Example for HTTP errors via requests
             error_details += f" (HTTP status: {e.response.status_code})"
        return f"Error: An unexpected error occurred with the Gemini API: {error_details}"

def write_ics_file_from_vevents(list_of_vevent_strings, output_filepath):
    if not list_of_vevent_strings:
        print(f"No VEVENTs provided for {output_filepath}. Skipping file creation.")
        return

    cal = Calendar()
    cal.add('prodid', '-//CUGA Event Generator Script//cuga.org//')
    cal.add('version', '2.0')

    added_events_count = 0
    for vevent_str in list_of_vevent_strings: # Changed variable name
        if isinstance(vevent_str, str) and "BEGIN:VEVENT" in vevent_str and "END:VEVENT" in vevent_str:
            # The icalendar library's Event.from_ical expects a full calendar string,
            # not just a VEVENT snippet directly for robust parsing of individual components.
            # A workaround is to wrap it in a minimal calendar structure for parsing.
            temp_cal_str = f"BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Temp//EN\n{vevent_str}\nEND:VCALENDAR"
            try:
                temp_gcal = Calendar.from_ical(temp_cal_str)
                for component in temp_gcal.walk():
                    if component.name == "VEVENT":
                        # Create a new Event to avoid issues with components from different calendars
                        # or to re-parent it correctly.
                        new_event = Event()
                        for key, value in component.items():
                            new_event.add(key, value)
                        # Ensure DTSTAMP is present, add if not (Gemini might forget)
                        if not component.get('dtstamp'):
                            new_event.add('dtstamp', datetime.utcnow())
                        cal.add_component(new_event)
                        added_events_count +=1
            except Exception as e:
                print(f"Error parsing VEVENT string into component: {e}\nString was:\n{vevent_str[:300]}...")
        else:
            print(f"Skipping invalid or non-VEVENT data: {str(vevent_str)[:100]}")

    if added_events_count == 0:
         print("No valid VEVENTs to add. Creating an ICS file with a placeholder event.")
         dummy_event = Event()
         dummy_event.add('summary', 'Placeholder Event - No valid VEVENTs generated or available.')
         # Make dtstart timezone-aware using a fixed offset if pytz is not available
         # For simplicity, using naive datetime, assuming local time interpretation by calendar clients
         dummy_event.add('dtstart', datetime(2024,1,1,10,0,0))
         dummy_event.add('dtstamp', datetime.utcnow())
         dummy_event.add('uid', f'dummy-{datetime.utcnow().timestamp()}@cuga.example.com')
         cal.add_component(dummy_event)

    try:
        with open(output_filepath, 'wb') as f:
            f.write(cal.to_ical())
        print(f"Successfully wrote ICS file to {output_filepath} with {added_events_count if added_events_count > 0 else '1 placeholder'} event(s).")
    except IOError as e:
        print(f"Error writing ICS file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during ICS file writing: {e}")

def main():
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    if not gemini_api_key:
            print("Info: GEMINI_API_KEY environment variable not set. Actual Gemini API calls will be skipped.")
            # Script will still run with mock/placeholder data if API key is missing

    raw_data = fetch_sheet_data(SHEET_URL)
    if not raw_data:
        print("Fatal: Failed to fetch or parse sheet data. Exiting.")
        return

    club_events = parse_club_data(raw_data)
    if not club_events:
        print("Fatal: No club data parsed successfully from sheet. Exiting.")
        return

    print(f"Info: Successfully parsed {len(club_events)} potential events from the sheet.")

    processed_event_fingerprints = load_processed_prompts(PROCESSED_PROMPTS_FILE)
    print(f"Info: Loaded {len(processed_event_fingerprints)} previously processed event fingerprints.")

    club_specific_vevents = [] # Changed from all_generated_vevents_strings

    if not os.path.exists(CLUB_SCHEDULES_DIR):
        os.makedirs(CLUB_SCHEDULES_DIR)

    for idx, event_data in enumerate(club_events):
        # Basic check for enough data to form a prompt
        if not event_data.get('ClubName', event_data.get('Club Name')) and \
           not event_data.get('PracticeTimes', event_data.get('Practice Times')):
            # print(f"Skipping event {idx+1} due to missing key information (Club Name and Practice Times). Data: {event_data}")
            continue

        fingerprint = get_event_fingerprint(event_data)

        if fingerprint in processed_event_fingerprints:
            # print(f"Info: Skipping already processed event: {event_data.get('ClubName', 'N/A')} (FP: {fingerprint[:8]})")
            continue

        club_name_for_log = event_data.get('ClubName', event_data.get('Club Name', 'Unknown Club'))
        print(f"Processing new event: {club_name_for_log} (FP: {fingerprint[:8]})")

        gemini_prompt = generate_gemini_prompt(event_data)
        # print(f"Generated Gemini Prompt for {club_name_for_log}:\n{gemini_prompt[:250]}...") # Log snippet for debugging

        vevent_output_from_gemini = call_gemini_api(gemini_prompt, gemini_api_key)

        current_club_name = event_data.get('ClubName', event_data.get('Club Name', 'UnknownClub'))

        if vevent_output_from_gemini and "Error:" not in str(vevent_output_from_gemini) and "blocked" not in str(vevent_output_from_gemini).lower():
            raw_vevents_from_gemini = vevent_output_from_gemini.split("BEGIN:VEVENT")
            parsed_vevents_for_this_entry = []
            valid_vevent_found_for_entry = False
            for vevent_part in raw_vevents_from_gemini:
                if vevent_part.strip():
                    full_vevent_str = "BEGIN:VEVENT" + vevent_part
                    # Basic validation of VEVENT structure
                    if "END:VEVENT" in full_vevent_str and "UID:" in full_vevent_str and "DTSTAMP:" in full_vevent_str:
                        parsed_vevents_for_this_entry.append(full_vevent_str)
                        valid_vevent_found_for_entry = True
                    else:
                        print(f"Warning: Invalid VEVENT structure received from Gemini for '{club_name_for_log}': {full_vevent_str[:200]}...")

            if valid_vevent_found_for_entry:
                club_specific_vevents.append({
                    "club_name": current_club_name,
                    "original_event_data": event_data,
                    "vevents": parsed_vevents_for_this_entry
                })
                print(f"Success: Gemini API call for '{club_name_for_log}' (entry {idx+1}) returned valid VEVENT(s).")
            else:
                print(f"Warning: No valid VEVENTs found in Gemini output for '{club_name_for_log}' (entry {idx+1}). Output: {vevent_output_from_gemini[:200]}...")
            save_processed_prompt(PROCESSED_PROMPTS_FILE, fingerprint)

        elif "Error:" in str(vevent_output_from_gemini) or "blocked" in str(vevent_output_from_gemini).lower():
            print(f"Warning: Gemini API call for '{club_name_for_log}' (entry {idx+1}) resulted in an error or was blocked: {vevent_output_from_gemini}")
            save_processed_prompt(PROCESSED_PROMPTS_FILE, fingerprint) # Save fingerprint even if Gemini reports error
        else: # No output or empty string
            print(f"Warning: Gemini API call returned no output or empty string for: {club_name_for_log} (entry {idx+1})")
            # Optionally, save fingerprint here too to prevent retries on events that consistently fail at Gemini stage
            save_processed_prompt(PROCESSED_PROMPTS_FILE, fingerprint)

    # After the main event processing loop
    print(f"Collected {len(club_specific_vevents)} items for ICS generation, potentially multiple per club.")

    # --- Aggregate events by club name ---
    aggregated_events_by_club = {}
    all_master_vevents = [] # For the master ICS file

    for item in club_specific_vevents:
        club_name = item['club_name']
        vevents = item['vevents']

        if club_name not in aggregated_events_by_club:
            aggregated_events_by_club[club_name] = {
                "vevents": [],
                "original_event_data_for_json": item['original_event_data']
            }
        aggregated_events_by_club[club_name]['vevents'].extend(vevents)
        all_master_vevents.extend(vevents)

    print(f"Aggregated events for {len(aggregated_events_by_club)} unique clubs.")

    # --- Generate Per-Club ICS Files ---
    processed_club_data_for_json = [] # To store data for cuga_club_data.json

    for club_name, data in aggregated_events_by_club.items():
        club_vevents = data['vevents']
        original_data = data['original_event_data_for_json']

        club_info_for_json = {
            'ClubName': original_data.get('ClubName', original_data.get('Club Name', club_name)),
            'ClubNameFR': original_data.get('ClubNameFR', original_data.get('Club Name FR', '')),
            'Province': original_data.get('Province', original_data.get('Province', '')),
            'City': original_data.get('City', original_data.get('City', '')),
            'PracticeLocation': original_data.get('PracticeLocation', original_data.get('Practice Location', '')),
            'PracticeLocationFR': original_data.get('PracticeLocationFR', original_data.get('Practice Location FR', '')),
            'PracticeTimes': original_data.get('PracticeTimes', original_data.get('Practice Times', '')),
            'PracticeTimesFR': original_data.get('PracticeTimesFR', original_data.get('Practice Times FR', '')),
            'Notes': original_data.get('Notes', original_data.get('Notes', '')),
            'NotesFR': original_data.get('NotesFR', original_data.get('Notes FR', '')),
            'SportType': original_data.get('SportType', original_data.get('Sport Type', '')),
            'ContactEmail': original_data.get('ContactEmail', ''),
            'WebsiteURL': original_data.get('WebsiteURL', ''),
            'FacebookURL': original_data.get('FacebookURL', ''),
            'InstagramURL': original_data.get('InstagramURL', ''),
            'ics_file_path': None
        }

        if not club_vevents:
            print(f"No VEVENTs generated for club: {club_name}. Skipping ICS file.")
            processed_club_data_for_json.append(club_info_for_json)
            continue

        sanitized_club_name_for_file = sanitize_filename(club_name)
        club_ics_filename = f"{sanitized_club_name_for_file}.ics"
        club_ics_filepath = os.path.join(CLUB_SCHEDULES_DIR, club_ics_filename)

        write_ics_file_from_vevents(club_vevents, club_ics_filepath)
        club_info_for_json['ics_file_path'] = club_ics_filepath
        processed_club_data_for_json.append(club_info_for_json)

    # --- Generate Master ICS File ---
    master_ics_filepath = 'master_cuga_schedule.ics'
    if all_master_vevents:
        write_ics_file_from_vevents(all_master_vevents, master_ics_filepath)
    else:
        print("No VEVENTs available to generate a master schedule. Master file will not be created.")
        # write_ics_file_from_vevents([], master_ics_filepath) # This would do nothing as per current func def

    # --- Generate cuga_club_data.json ---
    cuga_club_data_filepath = 'cuga_club_data.json'
    try:
        # Sort by province, then by club name for consistent output
        processed_club_data_for_json.sort(key=lambda x: (x.get('Province', '').lower(), x.get('ClubName', '').lower()))
        with open(cuga_club_data_filepath, 'w', encoding='utf-8') as f:
            json.dump(processed_club_data_for_json, f, ensure_ascii=False, indent=4)
        print(f"Successfully wrote club data to {cuga_club_data_filepath}")
    except IOError as e:
        print(f"Error writing club data JSON file: {e}")

    print("Script finished.")

if __name__ == '__main__':
    main()
