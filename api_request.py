"""
Request data from API.
http://ergast.com/mrd/
Pass the URL as an argument in the command line.
"""

import requests, sys, json, os

# Create folder to hold data if not already made.
try:
    os.makedirs("api_data")
except OSError:
    pass

try:
    # Create filename to save the data under.
    filename = sys.argv[1][25:-5].replace('/', '_')

    # Make the request from the API.
    r = requests.get(url=sys.argv[1])
    r.raise_for_status()

    # Store json data.
    data = r.json()

    # Save data.
    with open(f'api_data/{filename}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"File api_data/{filename}.json has successfully been saved.")

except requests.exceptions.HTTPError as err:
    raise SystemExit(err)

except:
    print('There has been an unspecified error. Please try again.')
