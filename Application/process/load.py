import pandas as pd
from databricks import sql
import json

with sql.connect(server_hostname="<hostname>",
                 http_path="<path>",
                 access_token="<access_token>") as connection:
    with connection.cursor() as cursor:
        # 지현씨 시군구 데이터
        cursor.execute("SELECT * FROM capstone.live_silver_table")
        result = cursor.fetchall()
        df1 = pd.DataFrame.from_records(result, columns=[desc[0] for desc in cursor.description])

        # 지현씨 시도 데이터
        cursor.execute("SELECT * FROM capstone.live_gold_table")
        result = cursor.fetchall()
        df = pd.DataFrame.from_records(result, columns=[desc[0] for desc in cursor.description])

        # 지훈씨 버블차트
        cursor.execute(
            "SELECT s.sidoname, s.cityname, s.pm10value, s.pm25value, p.pop, s.datetime FROM capstone.airpollution_silver s LEFT JOIN capstone.population_table p ON s.cityname = p.cityname WHERE s.sidoname = p.sidoname ")
        result = cursor.fetchall()
        addpop_df = pd.DataFrame.from_records(result, columns=[desc[0] for desc in cursor.description])

        # 지훈씨 라인, 바차트 2022년도
        cursor.execute("SELECT * FROM capstone.gold_day_week_table")
        result = cursor.fetchall()
        df22 = pd.DataFrame.from_records(result, columns=[desc[0] for desc in cursor.description])

        cursor.close()

def load_live_sido_table():
    """
    지현씨 맵박스 시도 코드에 들어가는 df
    """
    global df
    #df = pd.read_csv('live_sido_table.csv', encoding='utf-8')
    df = df.astype({'pm10value': 'float'})
    df = df.astype({'pm25value': 'float'})

    state_geo = 'SouthKorea.geojson'
    state_geo1 = json.load(open(state_geo, encoding='utf-8'))

    for idx, sido_dict in enumerate(state_geo1['features']):
        sido = sido_dict['properties']['sidoname']
        sidoname_g = df.loc[(df.cityname == sido), 'sidoname'].iloc[0]
        dust_a = df.loc[(df.cityname == sido), 'pm10value'].iloc[0]
        dust_b = df.loc[(df.cityname == sido), 'pm25value'].iloc[0]
        time = df.loc[(df.cityname == sido), 'datetime'].iloc[0]
        txt = f'<b><h4>{sidoname_g}</h4></b>pm10value : {dust_a}<br>pm25value : {dust_b}'

        state_geo1['features'][idx]['properties']['tooltip1'] = txt
        state_geo1['features'][idx]['properties']['지역'] = sidoname_g, dust_a
        state_geo1['features'][idx]['properties']['미세먼지'] = dust_a
        state_geo1['features'][idx]['properties']['초미세먼지'] = dust_b

    return df, state_geo1


def load_live_city_table():
    """
    지현씨 맵박스 시군구 지도 코드에 들어가는 df
    
    """
    global df1
    #df1 = pd.read_csv('live_city_table.csv', encoding='utf-8')
    df1["full"] = df1["sidoname"] + df1["cityname"]

    state_geo_s = 'features(1).geojson'
    state_geo_s1 = json.load(open(state_geo_s, encoding='utf-8'))

    for idx, sigun_dict in enumerate(state_geo_s1['features']):
        sigun = sigun_dict['properties']['sidoname'] + sigun_dict['properties']['cityname']
        cityname_g = df1.loc[(df1.full == sigun), 'cityname'].iloc[0]
        dust_a = df1.loc[(df1.full == sigun), 'pm10value'].iloc[0]
        dust_b = df1.loc[(df1.full == sigun), 'pm25value'].iloc[0]
        time = df1.loc[(df1.full == sigun), 'datetime'].iloc[0]
        txt = f'<b><h4>{cityname_g}</h4></b>pm10value : {dust_a}<br>pm25value : {dust_b}<br>datetime : {time}'

        state_geo_s1['features'][idx]['properties']['tooltip1'] = txt
        state_geo_s1['features'][idx]['properties']['미세먼지'] = dust_a
        state_geo_s1['features'][idx]['properties']['초미세먼지'] = dust_b

    return df1, state_geo_s1

def load_addpop():
    """
    지훈씨 시각화 애니메이션 코드에 들어가는 df
    """
    global addpop_df

    addpop_df = addpop_df[addpop_df['datetime'] > '2022-05-08']

    addpop_df['datetime'] = pd.to_datetime(addpop_df['datetime']).dt.tz_localize(None)
    addpop_df = addpop_df.sort_values("datetime")
    addpop_df['datetime'] = addpop_df['datetime'].astype(str)
    available_indicators = addpop_df['sidoname'].unique()
    ap_time_list = sorted(list(set(addpop_df['datetime'])))

    return addpop_df, available_indicators, ap_time_list

def load_lineC():
    """
    지훈씨 라인차트 코드에 들어가는 df
    """

    df22['datetime'] = pd.to_datetime(df22['datetime']).dt.tz_localize(None)

    return df22

