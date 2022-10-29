import xml.etree.ElementTree as ET
import requests 
import pandas as pd
from bs4 import BeautifulSoup as bs

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

def get_xml_files():
    res = []
    HOME_URL = 'https://data.bmkg.go.id/prakiraan-cuaca/'
    html = requests.get(HOME_URL).content 
    soup = bs(html,'lxml')
    for a in soup.find_all('a'):
        if '.xml' in a['href']:
            res.append('https://data.bmkg.go.id/'+a['href'][3:])
    return res

def proc(xml_file):
    global df
    #url =  'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-Aceh.xml'
    url = xml_file
    #print(url)
    text = requests.get(url).text
    root = ET.fromstring(text)

    for areas in root:
        for area in areas:
            if area.tag == 'area':
                area_id, lat, long, coord, type, description = area.attrib['id'],area.attrib['latitude'],area.attrib['longitude'], area.attrib['coordinate'], area.attrib['type'],area.attrib['description']
                #print(60*'=')
                #print(f'{id}\t{description}\nLat, Long: {lat},{long}\nCoordinate: {coord}')
                #print(60*'=')
                for params in area:
                    #print('area',area)
                    #print('params', params)
                    if params.tag == 'parameter':
                        param_id, param_description,param_type = params.attrib['id'], params.attrib['description'], params.attrib['type']
                        #print(f'{param_id} {param_description}({param_type})')
                        #print(60*'=')

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
                                df= pd.concat([df,new_row.to_frame().T],ignore_index=True)
                                print(df)
                                #print(tgl, value.text,value.attrib['unit'])
                                #break
                        #print(60*'=')
                    else:
                        pass

            else:
                pass
            #print("")
    #return df2


if __name__ == '__main__':
    from datetime import datetime
    start = datetime.now()
    print(f'Time start: {start}')
    columns = ['area_id', 'lat', 'long', 'coord', 'type','description','param_id','param_description','param_type','timerange_type', 'timerange_datetime','value','unit']
    df = pd.DataFrame(columns=columns)
    for xml_file in get_xml_files():
        proc(xml_file)
    print('df:',df)
    end = datetime.now()
    print(f'Time finish: {end}')
    print(f'Finished in {end-start}')
    #print(f'Total rows: {df.shape[0]}')
    #print(df.tail())
    import pickle
    with open('data.pickle', 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(df, f, pickle.HIGHEST_PROTOCOL)
    print('Data saved to data.pickle. - Task Completed')
        