import pandas as pd
import json

# geojson files
PATH_GEOJSON_2 = '/Users/shirk3n/Documents/Programacion/nuts/data/NUTS_LB_2021_4326_LEVL_2.geojson'

# Excel file path
PATH_EXCEL_FILE = '/Users/shirk3n/Documents/Programacion/nuts/data/Spain1.xlsx'

# Read the xlsx file
COL_TYPES = {"Country": str, "Name of School": str, "Website": str, "Official Email": str, "NUTs": str}
SHEET_NAME = 'Sheet1'


def data_geojson():
    with open(PATH_GEOJSON_2) as content:
        data_geojson = json.load(content)
    # Data of GEOJSON file
    nuts_names_json = {}
    for features in data_geojson['features']:
        nuts_names_json[features['properties']['NUTS_ID']] = {'prefix': features['properties']['CNTR_CODE'],
                                                              'country': features['properties']['CNTR_CODE'],
                                                              'city': features['properties']['NUTS_NAME'],
                                                              'coordinates': features['geometry']['coordinates']}
    return (nuts_names_json)


def data_excel(df):
    # Create a data structure from excel file
    nuts_names_excel = {}
    for index, row in df.iterrows():
        row_nut = row['NUTs']
        value = nuts_names_excel.get(row_nut)
        if (value):
            value.append(row)
        else:
            nuts_names_excel[row_nut] = [row]
    return (nuts_names_excel)


def iter_excel_item(key, value):
    # data of each value needed
    for key in value:
        for item in value:
            return (item['Country'])


def iter_excel(key, value):
    entryList = []
    # build entryList
    for key in value:
        for item in value:
            entryList.append({'name': item['Name of School'], 'web': item['Website'], 'email': item['Official Email']})
        return (entryList)


def create_json_kml(df):
    jsonFinal = {}
    list_feature = []

    nuts_names_json = data_geojson()
    nuts_names_excel = data_excel(df)

    jsonFinal['type'] = 'FeatureCollection'

    for key, value in nuts_names_excel.items():
        for jsonId, jsonValue in nuts_names_json.items():
            if jsonId == key:
                jsonFinal['features'] = {'type': 'Feature', 'properties':
                    {"prefix": jsonValue['prefix'],
                     "country": iter_excel_item(key, value),
                     "city": jsonValue['city'],
                     "entryList": iter_excel(key, value)																	},
                                         'geometry':{
                                             'type' : 'Point',
                                             'coordinates': jsonValue['coordinates']
                                         }
                                         }

                features = jsonFinal.get('features')
                if (features):
                    list_feature.append(features)

    jsonFinal['features'] = list_feature
    print(jsonFinal)

    print('\n')



    json_dump = json.dumps(jsonFinal, indent = 2)

    # writing to a final_result.json
    with open ("data/final_result.json","w") as outfile:
        outfile.write(json_dump)


if __name__ == '__main__':
    print('\n')
    df = pd.read_excel(PATH_EXCEL_FILE,skiprows=1,sheet_name=SHEET_NAME,dtype=COL_TYPES)
    create_json_kml(df)