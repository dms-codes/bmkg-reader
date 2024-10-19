import xml.etree.ElementTree as ET
import requests
import pandas as pd

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

# BMKG API URL for weather data
url = 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-Aceh.xml'
response = requests.get(url)
root = ET.fromstring(response.content)

# Define DataFrame columns
columns = ['area_id', 'lat', 'long', 'coord', 'type', 'description', 
           'param_id', 'param_description', 'param_type', 'timerange_type', 
           'timerange_datetime', 'value', 'unit']
df_areas = pd.DataFrame(columns=columns)

# Parsing the XML data
for area in root.findall(".//area"):
    area_id = area.get('id')
    lat = area.get('latitude')
    lon = area.get('longitude')
    coord = area.get('coordinate')
    area_type = area.get('type')
    description = area.get('description')

    print(60 * '=')
    print(f'{area_id}\t{description}\nLat, Long: {lat},{lon}\nCoordinate: {coord}')
    print(60 * '=')

    for parameter in area.findall('parameter'):
        param_id = parameter.get('id')
        param_description = parameter.get('description')
        param_type = parameter.get('type')

        print(f'{param_id} {param_description} ({param_type})')
        print(60 * '=')

        for timerange in parameter.findall('timerange'):
            timerange_type = timerange.get('type')
            timerange_datetime = timerange.get('datetime')

            # Formatting the datetime
            date_str = f"{timerange_datetime[6:8]}-{timerange_datetime[4:6]}-{timerange_datetime[:4]} {timerange_datetime[8:10]}:{timerange_datetime[10:]}"

            for value in timerange.findall('value'):
                # If the description is 'Weather', map the value to the weather code
                if description == 'Weather':
                    value.text = kode_cuaca.get(int(value.text), value.text)

                # Create a new row for the DataFrame
                new_row = pd.Series({
                    'area_id': area_id, 'lat': lat, 'long': lon, 'coord': coord,
                    'type': area_type, 'description': description,
                    'param_id': param_id, 'param_description': param_description, 'param_type': param_type,
                    'timerange_type': timerange_type, 'timerange_datetime': timerange_datetime,
                    'value': value.text, 'unit': value.get('unit')
                })

                # Append the new row to the DataFrame
                df_areas = pd.concat([df_areas, new_row.to_frame().T], ignore_index=True)

                # Print the formatted output
                print(date_str, value.text, value.get('unit'))
                break  # Exit after processing one value per timerange

        print(60 * '=')

# Display the DataFrame
print(df_areas)
