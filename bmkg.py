import xml.etree.ElementTree as ET
import requests
import pandas as pd

kode_cuaca= {
0 : "Cerah / Clear Skies",
1 : "Cerah Berawan / Partly Cloudy",
2 : "Cerah Berawan / Partly Cloudy",
3 : "Berawan / Mostly Cloudy",
4 : "Berawan Tebal / Overcast",
5 : "Udara Kabur / Haze",
10 : "Asap / Smoke",
45 : "Kabut / Fog",
60 : "Hujan Ringan / Light Rain",
61 : "Hujan Sedang / Rain",
63 : "Hujan Lebat / Heavy Rain",
80 : "Hujan Lokal / Isolated Shower",
95 : "Hujan Petir / Severe Thunderstorm",
97 : "Hujan Petir / Severe Thunderstorm",
}
url =  'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-Aceh.xml'
text = requests.get(url).text
root = ET.fromstring(text)


columns = ['area_id', 'lat', 'long', 'coord', 'type','description','param_id','param_description','param_type','timerange_type', 'timerange_datetime','value','unit']
df_areas = pd.DataFrame(columns=columns)
for areas in root:
    for area in areas:
        if area.tag == 'area':
            area_id, lat, long, coord, type, description = area.attrib['id'],area.attrib['latitude'],area.attrib['longitude'], area.attrib['coordinate'], area.attrib['type'],area.attrib['description']
            #new_row = pd.Series({'area_id':area_id, 'lat':lat, 'long':long, 'coord':coord, 'type':type, 'description':description})
            #print(new_row)
            #df_areas = pd.concat([df_areas,new_row.to_frame().T],ignore_index=True)
            #print(df_areas)
            print(60*'=')
            print(f'{id}\t{description}\nLat, Long: {lat},{long}\nCoordinate: {coord}')
            print(60*'=')
            for params in area:
                print('area',area)
                print('params', params)
                if params.tag == 'parameter':
                    param_id, param_description,param_type = params.attrib['id'], params.attrib['description'], params.attrib['type']
                    print(f'{param_id} {param_description}({param_type})')
                    print(60*'=')

                    for timerange in params:
                        #print(timerange.tag, timerange.attrib)
                        timerange_type, timerange_datetime = timerange.attrib['type'],timerange.attrib['datetime']
                        
                        datedate,mondate,yeardate= timerange_datetime[6:8], timerange_datetime[4:6],timerange_datetime[:4]
                        hourdate, mindate = timerange_datetime[8:10], timerange_datetime[10:]
                        tgl = f'{datedate}-{mondate}-{yeardate} {hourdate}:{mindate}'
                        for value in timerange:
                            if description == 'Weather':
                                value.text = kode_cuaca[int(value.text)]
                            new_row = pd.Series({'area_id':area_id, 'lat':lat, 'long':long, 'coord':coord, 'type':type, 'description':description,
                                            'param_id':param_id, 'param_description':param_description,'param_type':param_type,
                                            'timerange_type':timerange_type, 'timerange_datetime':timerange_datetime,
                                            'value':value.text,'unit':value.attrib['unit'] })
                            df_areas = pd.concat([df_areas,new_row.to_frame().T],ignore_index=True)
                            print(tgl, value.text,value.attrib['unit'])
                            break
                    print(60*'=')
                else:
                    pass

        else:
            pass
        print("")

print(df_areas)
