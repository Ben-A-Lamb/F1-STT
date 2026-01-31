import requests
from time import sleep

#Audio
def get_audio_files(session_key):
    files = []
    url = f"https://api.openf1.org/v1/team_radio?session_key={session_key}"
    response = requests.get(url)
    data = response.json()
    for file in data:
        print(list(file.keys()))
        files.append(file['recording_url'])
    return files

#Session Keys
def get_session_keys_by_location(circuit_key, rain=False):
    url = f"https://api.openf1.org/v1/sessions?session_type=Race&circuit_key={circuit_key}"
    response = requests.get(url)
    data = response.json()
    return [session['session_key'] for session in data]

def get_calendar_by_year(year):
    locations = []
    url = f"https://api.openf1.org/v1/sessions?session_type=Race&year={year}"
    response = requests.get(url)
    data = response.json()
    for race in data:
        locations.append([race['circuit_short_name'], race['circuit_key']])
    return locations

def get_latest_session_key():
    url = "https://api.openf1.org/v1/sessions?session_type=Race&session_key=latest"
    response = requests.get(url)
    data = response.json()
    data = data[0]
    return data['session_key']

# Filters
def filter_rain_sessions(sessions, rain=False):
    rainy_sessions = []
    dry_sessions = []
    for session in sessions:
        rainy = False
        url = f"https://api.openf1.org/v1/weather?session_key={session}"
        response = requests.get(url)
        data = response.json()
        consecutive_rain_count = 0
        for weather_point in data:
            if weather_point['rainfall'] == 1:
                consecutive_rain_count += 1
                if consecutive_rain_count >= 10:
                    rainy=True
            else:
                consecutive_rain_count = 0
        if rainy and rain:
            rainy_sessions.append(session)
        elif not rainy and not rain:
            dry_sessions.append(session)
        sleep(0.34)  # To avoid hitting API rate limits
    
    if rain:
        filtered_sessions = rainy_sessions
    else:
        filtered_sessions = dry_sessions
    
    return filtered_sessions




# Race data
def get_stint_data(session_key):
    url = f"https://api.openf1.org/v1/stints?session_key={session_key}"
    response = requests.get(url)
    data = response.json()
    return [[stint['driver_number'], stint['compound'], stint['stint_number'], stint['lap_start'], stint['lap_end']] for stint in data]


def driver_specific_strategies(races):
    race_strategies = []
    for stints in races:
        strategies = {}
        for stint in stints:
            print(stint[0])
            if stint[0] not in list(strategies):
                strategies[stint[0]] = [stint[1:]]
            else:
                strategies[stint[0]].append(stint[1:])
        race_strategies.append(strategies)
    return race_strategies

def get_grid_and_result(session_key):
    url = f"https://api.openf1.org/v1/grid?session_key={session_key}"
    response = requests.get(url)
    grid_data = response.json()
    
    url = f"https://api.openf1.org/v1/results?session_key={session_key}"
    response = requests.get(url)
    result_data = response.json()
    
    grid = [[entry['position'], entry['driver_number']] for entry in grid_data]
    results = [[entry['position'], entry['driver_number']] for entry in result_data]
    
    return {'grid': grid, 'results': results}

## Example usage
calendar = get_calendar_by_year(2026)
races = get_session_keys_by_location(calendar[0][1]) # Example usage
dry_races = filter_rain_sessions(races, rain=False)
wet_races = filter_rain_sessions(races, rain=True)

dry_strategies = []
wet_strategies = []

for race in races:
    if race in dry_races:
        dry_strategies.append(get_stint_data(race))
    elif race in wet_races:
        wet_strategies.append(get_stint_data(race))


    
print(driver_specific_strategies(wet_strategies))