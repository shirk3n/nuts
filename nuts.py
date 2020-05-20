import pandas as pd
import json

# geojson files
PATH_GEOJSON_0 = '/Users/shirk3n/Documents/Programacion/nuts/data/NUTS_LB_2021_4326_LEVL_0.geojson'
PATH_GEOJSON_1 = '/Users/shirk3n/Documents/Programacion/nuts/data/NUTS_LB_2021_4326_LEVL_1.geojson'
PATH_GEOJSON_2 = '/Users/shirk3n/Documents/Programacion/nuts/data/NUTS_LB_2021_4326_LEVL_2.geojson'
PATH_GEOJSON_3 = '/Users/shirk3n/Documents/Programacion/nuts/data/NUTS_LB_2021_4326_LEVL_3.geojson'

# Excel file path
PATH_EXCEL_FILE = '/Users/shirk3n/Documents/Programacion/nuts/data/Spain1.xlsx'

# Read the xlsx file
COL_TYPES = {"Country": str, "Name of School": str, "Website": str, "Official Email": str, "NUTs": str}
SHEET_NAME = 'Sheet1'

def choose_geojson_file(key):
    length_nut = len(key)
    #Choose the correct json file depending of the NUT's length
    if length_nut == 2:
        print('2')
        with open(PATH_GEOJSON_0) as content:
            data = json.load(content)
    elif length_nut == 3:
        print('3')
        with open(PATH_GEOJSON_1) as content:
            data = json.load(content)
    elif length_nut == 4:
        print('4')
        with open(PATH_GEOJSON_2) as content:
            data = json.load(content)
    elif length_nut == 5:
        print('5')
        with open(PATH_GEOJSON_3) as content:
            data = json.load(content)
    # print(data)
    print('\n')
    return(data)

def data_geojson(key):
    data_geojson = choose_geojson_file(key)
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
    final_df = sort_row_nut(df)
    for index, row in final_df.iterrows():
        row_nut = row['NUTs']
        # print(row_nut)
        value = nuts_names_excel.get(row_nut)
        if (value):
            value.append(row)
        else:
            nuts_names_excel[row_nut] = [row]
    return (nuts_names_excel)

def sort_row_nut(df):
    row_nut_aux = ''
    list_aux = []
    for index, row in df.iterrows():
        row_nut = row['NUTs']
        if len(row_nut) == 5:
            if row_nut[3] == '0' and row_nut[4] == '0':
                row_nut_aux = row_nut

    for index1, row1 in df.iterrows():
        row_nut1 = row1['NUTs']
        if row_nut_aux == row_nut1 + '0':
            print('asdasd')
            df['NUTs'].replace({row1['NUTs']:row_nut_aux},inplace=True)
    return(df)

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

    nuts_names_excel = data_excel(df)

    jsonFinal['type'] = 'FeatureCollection'

    for key, value in nuts_names_excel.items():
        nuts_names_json = data_geojson(key)
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
    # print(jsonFinal)

    print('\n')



    json_dump = json.dumps(jsonFinal, indent = 2)

    # writing to a final_result.json
    with open ("data/final_result.json","w") as outfile:
        outfile.write(json_dump)


if __name__ == '__main__':
    print('\n')
    df = pd.read_excel(PATH_EXCEL_FILE,skiprows=1,sheet_name=SHEET_NAME,dtype=COL_TYPES)
    create_json_kml(df)
    print(sort_row_nut(df))