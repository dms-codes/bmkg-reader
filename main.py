import xml.etree.ElementTree as ET
import requests 
import pandas as pd
from bs4 import BeautifulSoup as bs
from datetime import datetime
import pickle

# Weather codes mapping
kode_cuaca = {
    0: "Cerah / Clear Skies",
    1: "Cerah Berawan / Partly Cloudy",
    2: "Cerah Berawan / Partly Cloudy",
    3: "Berawan / Mostly Cloudy",
    4: "Berawan Tebal / Overcast",
    5: "Udara Kabur / Haze",
    10: "Asap / Smoke",
    45: "Kabut / Fog",
    60: "Hujan Ringan / Light Rain",
    61: "Hujan Sedang / Rain",
    63: "Hujan Lebat / Heavy Rain",
    80: "Hujan Lokal / Isolated Shower",
    95: "Hujan Petir / Severe Thunderstorm",
    97: "Hujan Petir / Severe Thunderstorm",
}

# Function to retrieve the list of XML files from BMKG
def get_xml_files():
    HOME_URL = 'https://data.bmkg.go.id/prakiraan-cuaca/'
    html = requests.get(HOME_URL).content 
    soup = bs(html, 'lxml')
    return [
        'https://data.bmkg.go.id/' + a['href'][3:]
        for a in soup.find_all('a') if '.xml' in a['href']
    ]

# Function to process each XML file
def process_xml_file(xml_file, df):
    response = requests.get(xml_file).text
    root = ET.fromstring(response)
    
    # Parsing the XML data
    for area in root.findall(".//area"):
        area_info = {
            'area_id': area.get('id'),
            'lat': area.get('latitude'),
            'long': area.get('longitude'),
            'coord': area.get('coordinate'),
            'type': area.get('type'),
            'description': area.get('description')
        }

        for parameter in area.findall('parameter'):
            param_info = {
                'param_id': parameter.get('id'),
                'param_description': parameter.get('description'),
                'param_type': parameter.get('type')
            }

            for timerange in parameter.findall('timerange'):
                timerange_info = {
                    'timerange_type': timerange.get('type'),
                    'timerange_datetime': timerange.get('datetime')
                }
                timerange_info['formatted_datetime'] = f"{timerange_info['timerange_datetime'][6:8]}-{timerange_info['timerange_datetime'][4:6]}-{timerange_info['timerange_datetime'][:4]} {timerange_info['timerange_datetime'][8:10]}:{timerange_info['timerange_datetime'][10:]}"

                for value in timerange.findall('value'):
                    # Update weather description based on the code
                    value_text = kode_cuaca.get(int(value.text), value.text) if area_info['description'] == 'Weather' else value.text

                    # Add row to the dataframe
                    new_row = {
                        **area_info,
                        **param_info,
                        **timerange_info,
                        'value': value_text,
                        'unit': value.get('unit')
                    }
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    print(df)
                    # Only processing one value per timerange
                    break
    return df

# Main function
if __name__ == '__main__':
    start = datetime.now()
    print(f'Time start: {start}')

    # Initialize the DataFrame
    columns = ['area_id', 'lat', 'long', 'coord', 'type', 'description', 
               'param_id', 'param_description', 'param_type', 'timerange_type', 
               'timerange_datetime', 'value', 'unit']
    df = pd.DataFrame(columns=columns)

    # Process each XML file
    for xml_file in get_xml_files():
        df = process_xml_file(xml_file, df)

    print(f'Final dataframe shape: {df.shape}')
    
    # Save the DataFrame to a pickle file
    with open('data.pickle', 'wb') as f:
        pickle.dump(df, f, pickle.HIGHEST_PROTOCOL)

    end = datetime.now()
    print(f'Time finish: {end}')
    print(f'Finished in {end - start}')
    print('Data saved to data.pickle. - Task Completed')
