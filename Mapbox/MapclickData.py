from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import mapboxgl
from mapboxgl.viz import *
import os
from mapboxgl.utils import create_color_stops
import matplotlib.pyplot as plt


app = Dash(__name__, suppress_callback_exceptions=True)

df = pd.read_csv('live_sido_table.csv', encoding='utf-8')
df = df.astype({'pm10value' : 'float'})
df = df.astype({'pm25value' : 'float'})
center_map = [{"lat" : 38.00, "lon":128.22},{"lat" :37.45, "lon":126.70},{"lat" :35.16, "lon":126.85},{"lat" :35.53, "lon":129.31},{"lat" :36.35, "lon":127.38},{"lat" :37.56, "lon":127.19},{"lat" :37.56, "lon":126.97},{"lat" :35.87, "lon":128.60},{"lat" :35.18, "lon":129.07},{"lat" :36.51, "lon":126.80},{"lat" :34.45, "lon":127.00}, {"lat" :36.49, "lon":127.39},{"lat" :35.45, "lon":127.15}, {"lat" :35.15, "lon":128.15},{"lat" :36.25, "lon":127.17},{"lat" :36.19, "lon":128.45}, {"lat" :33.25, "lon":126.30}]
df['center_map'] = center_map

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





df1 = pd.read_csv('live_city_table.csv', encoding='utf-8')
df1["full"] = df1["sidoname"]+df1["cityname"]

state_geo_s = 'features(1).geojson'
state_geo_s1 = json.load(open(state_geo_s, encoding='utf-8'))


for idx, sigun_dict in enumerate(state_geo_s1['features']):
    sigun = sigun_dict['properties']['sidoname']+ sigun_dict['properties']['cityname']
    cityname_g = df1.loc[(df1.full == sigun), 'cityname'].iloc[0]
    dust_a = df1.loc[(df1.full == sigun), 'pm10value'].iloc[0]
    dust_b = df1.loc[(df1.full == sigun), 'pm25value'].iloc[0]
    time = df1.loc[(df1.full == sigun), 'datetime'].iloc[0]
    txt = f'<b><h4>{cityname_g}</h4></b>pm10value : {dust_a}<br>pm25value : {dust_b}<br>datetime : {time}'

    state_geo_s1['features'][idx]['properties']['tooltip1'] = txt
    state_geo_s1['features'][idx]['properties']['미세먼지'] = dust_a
    state_geo_s1['features'][idx]['properties']['초미세먼지'] = dust_b



app.layout = html.Div([
    html.H1('대기정보',style = {'text-align':'center'}),
    dcc.Tabs(id="tabs", value='tab1', children=[
        dcc.Tab(label='미세먼지', value='tab1'),
        dcc.Tab(label='초미세먼지', value='tab2'),
    ]),
    html.Div(id='tabs_content')
])

@app.callback(Output('tabs_content','children'),
              Input('tabs','value'))

def render_content(tab):
    if tab == 'tab1':
        return html.Div([

            
            html.Div([
                dcc.Graph(id = 'map1',
                          clickData={'points': [{'customdata':'서울'}]}
                )
            ],style={'width':'49%', 'display':'inline-block','marginTop':'5px','padding':'0 20'}),
            html.Div([
        
                dcc.Graph(id = 'map2', figure={})
                ],style={'width':'49%', 'display':'inline-block','marginTop':'5px','float':'right'}),
            html.Div(id='graph_content1')
            ])
    elif tab == 'tab2':
        return html.Div([
            html.Div([
                dcc.Graph(id = 'map3',
                          clickData={'points': [{'customdata':'서울'}]}
                )
                ],style={'width':'49%', 'display':'inline-block','marginTop':'5px','padding':'0 20'}),
            html.Div([
                dcc.Graph(id = 'map4', figure={})
                ],style={'width':'49%', 'display':'inline-block','marginTop':'5px','float':'right'}),
            html.Div(id='graph_content2')
    ])

@app.callback(
    Output('map1','figure'),
    Input('graph_content1','value')
    
)

def update_graph(graph_content1):

    dff = df.copy()

  
    fig = px.choropleth_mapbox(dff, geojson=state_geo1,
                               locations='sidoname',
                               color = 'pm10value',
                               color_continuous_scale="portland",
                               range_color=(0,75),
                               mapbox_style="carto-positron",
                               featureidkey="properties.sidoname",
                               zoom=4.8, center={"lat":37.565,"lon":126.986},
                               opacity=0.5,
                               labels={'pm10value':'미세먼지'}
                               )

    fig.update_traces(customdata=dff['sidoname'],selector=dict(type='choroplethmapbox'))
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    


    return fig

@app.callback(
    Output('map2','figure'),
    [Input('graph_content1','value'),
     Input('map1', 'clickData')]
)

def update_graph(graph_content1, clickData):

    
    dff1 = df1.copy()
    
    locations = clickData['points'][0]['customdata']
    dff1 = dff1[dff1['sidoname'] == locations]
    i = 6
    
    if clickData['points'][0]['customdata'] == '강원':
        i = 0
    elif clickData['points'][0]['customdata'] == '인천':
        i = 1
    elif clickData['points'][0]['customdata'] == '광주':
        i = 2
    elif clickData['points'][0]['customdata'] == '울산':
        i = 3
    elif clickData['points'][0]['customdata'] == '대전':
        i = 4
    elif clickData['points'][0]['customdata'] == '경기':
        i = 5
    elif clickData['points'][0]['customdata'] == '서울':
        i = 6
    elif clickData['points'][0]['customdata'] == '대구':
        i = 7
    elif clickData['points'][0]['customdata'] == '부산':
        i = 8
    elif clickData['points'][0]['customdata'] == '충남':
        i = 9
    elif clickData['points'][0]['customdata'] == '전남':
        i = 10
    elif clickData['points'][0]['customdata'] == '충북':
        i = 11
    elif clickData['points'][0]['customdata'] == '전북':
        i = 12
    elif clickData['points'][0]['customdata'] == '경남':
        i = 13
    elif clickData['points'][0]['customdata'] == '세종':
        i = 14
    elif clickData['points'][0]['customdata'] == '경북':
        i = 15
        
    else:
        i= 16
            
    
    
  
    
    fig = px.choropleth_mapbox(dff1, geojson=state_geo_s1,
                               locations='full',
                               color = 'pm10value',
                               color_continuous_scale="portland",
                               range_color=(0,75),
                               mapbox_style="carto-positron",
                               featureidkey="properties.geofull",
                               zoom = 7, center = center_map[i],
                               opacity=0.5,
                               labels={'pm10value':'미세먼지'}
                               )
    
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig

@app.callback(
    Output('map3','figure'),
    Input('graph_content2','value')
)

def update_graph(graph_content2):

    dff = df.copy()
    
    
    fig = px.choropleth_mapbox(dff, geojson=state_geo1,
                               locations='sidoname',
                               color = 'pm25value',
                               color_continuous_scale="portland",
                               range_color=(0,75),
                               mapbox_style="carto-positron",
                               featureidkey="properties.sidoname",
                               zoom=4.8, center={"lat":37.565,"lon":126.986},
                               opacity=0.5,
                               labels={'pm25value':'초미세먼지'}
                               )

    fig.update_traces(customdata=dff['sidoname'],selector=dict(type='choroplethmapbox'))
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig


@app.callback(
    Output('map4','figure'),
    [Input('graph_content2','value'),
     Input('map3', 'clickData')]
)
def update_graph(graph_content2, clickData):

    dff1 = df1.copy()

    locations = clickData['points'][0]['customdata']
    dff1 = dff1[dff1['sidoname'] == locations]
    i = 6
    
    if clickData['points'][0]['customdata'] == '강원':
        i = 0
    elif clickData['points'][0]['customdata'] == '인천':
        i = 1
    elif clickData['points'][0]['customdata'] == '광주':
        i = 2
    elif clickData['points'][0]['customdata'] == '울산':
        i = 3
    elif clickData['points'][0]['customdata'] == '대전':
        i = 4
    elif clickData['points'][0]['customdata'] == '경기':
        i = 5
    elif clickData['points'][0]['customdata'] == '서울':
        i = 6
    elif clickData['points'][0]['customdata'] == '대구':
        i = 7
    elif clickData['points'][0]['customdata'] == '부산':
        i = 8
    elif clickData['points'][0]['customdata'] == '충남':
        i = 9
    elif clickData['points'][0]['customdata'] == '전남':
        i = 10
    elif clickData['points'][0]['customdata'] == '충북':
        i = 11
    elif clickData['points'][0]['customdata'] == '전북':
        i = 12
    elif clickData['points'][0]['customdata'] == '경남':
        i = 13
    elif clickData['points'][0]['customdata'] == '세종':
        i = 14
    elif clickData['points'][0]['customdata'] == '경북':
        i = 15
        
    else:
        i= 16
    
    
    fig = px.choropleth_mapbox(dff1, geojson=state_geo_s1,
                               locations='full',
                               color = 'pm25value',
                               color_continuous_scale="portland",
                               range_color=(0,75),
                               mapbox_style="carto-positron",
                               featureidkey="properties.geofull",
                               zoom = 7, center = center_map[i],
                               opacity=0.5,
                               labels={'pm25value':'초미세먼지'}
                               )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig



if __name__ == '__main__':
    app.run_server(debug=True)
