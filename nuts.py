import pandas as pd
import json
import os

# geojson files
PATH_GEOJSON_0 = 'data/NUTS_LB_2021_4326_LEVL_0.geojson'
PATH_GEOJSON_1 = 'data/NUTS_LB_2021_4326_LEVL_1.geojson'
PATH_GEOJSON_2 = 'data/NUTS_LB_2021_4326_LEVL_2.geojson'
PATH_GEOJSON_3 = 'data/NUTS_LB_2021_4326_LEVL_3.geojson'

# Read the xlsx file
COL_TYPES = {"Country": str, "Name of School": str, "Website": str, "Official Email": str, "NUTs": str}
SHEET_NAME = 'Sheet1'


def data_geojson(key_excel):
    # Create a json data structure
    data_geojson = choose_geojson_file(key_excel)
    # Data of GEOJSON file
    nuts_names_json = {}
    for features in data_geojson['features']:
        nuts_names_json[features['properties']['NUTS_ID']] = {'prefix': features['properties']['CNTR_CODE'],
                                                              'country': features['properties']['CNTR_CODE'],
                                                              'city': features['properties']['NUTS_NAME'],
                                                              'coordinates': features['geometry']['coordinates']}
    return (nuts_names_json)


def choose_geojson_file(key_excel):
    global data
    lenght_nut = len(key_excel)
    # Choose the correct json file depending of the NUT's lenght
    if lenght_nut == 2:
        with open(PATH_GEOJSON_0) as content:
            data = json.load(content)
    elif lenght_nut == 3:
        with open(PATH_GEOJSON_1) as content:
            data = json.load(content)
    elif lenght_nut == 4:
        with open(PATH_GEOJSON_2) as content:
            data = json.load(content)
    elif lenght_nut == 5:
        with open(PATH_GEOJSON_3) as content:
            data = json.load(content)
    return (data)


def data_excel(df):
    # Create a data structure from excel file
    df = df.sort_values('Name of School')
    nuts_names_excel = {}
    final_df = sort_row_nut(df)
    for index, row in final_df.iterrows():
        row_nut = row['NUTs']
        value = nuts_names_excel.get(row_nut)
        if (value):
            value.append(row)
        else:
            nuts_names_excel[row_nut] = [row]
    return (nuts_names_excel)


def sort_row_nut(df):
    # Replacing the coincident nuts between lenght = 4 and lenght = 5
    row_nut_aux = 0
    for index, row in df.iterrows():
        row_nut = row['NUTs']
        if len(row_nut) == 5:
            if row_nut[3] == '0' and row_nut[4] == '0':
                row_nut_aux = row_nut

    for index1, row1 in df.iterrows():
        row_nut1 = row1['NUTs']
        if row_nut_aux == row_nut1 + '0':
            df['NUTs'].replace({row1['NUTs']: row_nut_aux}, inplace=True)
    return (df)


def iter_excel_item(key, value):
    # Data of each value needed
    for key in value:
        for item in value:
            return (item['Country'])


def iter_excel(key, value):
    # Build entryList
    entryList = []
    for key in value:
        for item in value:
            entryList.append({'name': item['Name of School'], 'web': item['Website'], 'email': item['Official Email']})
        return (entryList)


def create_json_kml():
    # Creation of the final json
    json_final = {}
    list_feature = []

    json_final['type'] = 'FeatureCollection'

    for f in files_xlsx:
        print(f)
        df = pd.read_excel(f, skiprows=1, sheet_name=SHEET_NAME, dtype=COL_TYPES)
        df = df.fillna(value="")

        nuts_names_excel = data_excel(df)

        for key_excel, value_excel in nuts_names_excel.items():
            nuts_names_json = data_geojson(key_excel)
            for key_json, value_json in nuts_names_json.items():
                if key_json == key_excel:
                    json_final['features'] = {'type': 'Feature', 'properties':
                        {"prefix": value_json['prefix'],
                         "country": iter_excel_item(key_excel, value_excel),
                         "city": value_json['city'],
                         "entryList": iter_excel(key_excel, value_excel)																},
                                              'geometry':{
                                                  'type' : 'Point',
                                                  'coordinates': value_json['coordinates']
                                              }
                                              }

                    features = json_final.get('features')
                    if (features):
                        list_feature.append(features)

        # Dump to final JSON

        json_final['features'] = list_feature
        json_dump = json.dumps(json_final, indent = 2,ensure_ascii=False)

        # Writing to a final_result.json
        with open ("data/FIN AL_R ESULT.json","w",encoding='utf8') as outfile:
            outfile.write(json_dump)


if __name__ == '__main__':
    # Get all the xlsx files from the folder
    path = os.getcwd()
    files = os.listdir(path)
    files_xlsx = [f for f in files if f[-4:] == 'xlsx']
    create_json_kml()