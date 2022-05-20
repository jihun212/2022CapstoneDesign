from dash import Dash, Input, Output, dcc, html
import plotly.express as px
import plotly.graph_objs as go
import mapboxgl
import dash
from mapboxgl.viz import *
from mapboxgl.utils import create_color_stops
import matplotlib.pyplot as plt
import pandas as pd
import dash_bootstrap_components as dbc
import process.load as L
import process.animation as animation
import IPython
import requests
import process.LineChart as LineChart
import process.barChart as barChart


df_sido, state_geo1 = L.load_live_sido_table() #sido geojson
df_city, state_geo_s1 = L.load_live_city_table() #city geojson
df_ap, available_indicators, ap_time_list = L.load_addpop()

center_map = [{"lat": 38.00, "lon": 128.22}, {"lat": 37.50, "lon": 126.50}, {"lat": 35.16, "lon": 126.85},
                  {"lat": 35.53, "lon": 129.31}, {"lat": 36.35, "lon": 127.38}, {"lat": 37.56, "lon": 127.19},
                  {"lat": 37.56, "lon": 126.97}, {"lat": 35.87, "lon": 128.60}, {"lat": 35.18, "lon": 129.07},
                  {"lat": 36.51, "lon": 126.80}, {"lat": 34.45, "lon": 127.00}, {"lat": 36.49, "lon": 127.39},
                  {"lat": 35.45, "lon": 127.15}, {"lat": 35.15, "lon": 128.15}, {"lat": 36.53, "lon": 127.17},
                  {"lat": 36.19, "lon": 128.45}, {"lat": 33.25, "lon": 126.30}]
df_sido['center_map'] = center_map

CONTENT_STYLE = {
    "margin-left": "1rem",
    "margin-right": "1rem",
    "padding": "3rem 3rem",
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO], suppress_callback_exceptions=True, meta_tags=[
    {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
])
application = app.server

layout_title = dbc.Row(dbc.Col([html.H1('Lake House', style={'text-align': 'left', "margin-left": "1rem",
    "margin-right": "1rem",
    "padding": "1rem 1rem",}, ), ]))
layout_nav = dbc.Row(dbc.Col([dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("지도 실시간 정보", href="/", active="exact")),
        dbc.NavItem(dbc.NavLink("시각화 애니메이션", href="/animation", active="exact")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("라인 차트", href="/LineChart", active="exact"),
                dbc.DropdownMenuItem("막대 차트", href="/barChart", active="exact"),
            ],
            nav=True,
            in_navbar=True,
            label="More",

        ),
    ],
    brand="미세먼지 & 초미세먼지 정보",
    brand_href="#",
    color="primary",
    dark=True,

)
])
)


layout_content = html.Div(id="page-content",
                          style = CONTENT_STYLE,
                          children=[])

app.layout = dbc.Container([
    layout_title,
    layout_nav,
    html.Div([
        dcc.Location(id='url'),
        layout_content
    ])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/animation':
        return animation.layout
    if pathname == '/LineChart':
        return LineChart.layout
    if pathname == '/barChart':
        return barChart.layout
    # if pathname == '/barchart' :
    # return barchart.layout
    if pathname == "/":
        return [
            html.Div([
                html.H1('대기정보', style={'text-align': 'center'}),
                dcc.Tabs(id="tabs", value='tab1', children=[
                    dcc.Tab(label='미세먼지', value='tab1'),
                    dcc.Tab(label='초미세먼지', value='tab2'),
                ]),
                html.Div(id='tabs_content')
            ]),

            dbc.Row([dbc.Col(dbc.CardGroup(
            [
            dbc.Card(
                dbc.CardBody(
                        [
                            html.H4("미세먼지(㎍/㎥) 기준", className="card-title"),
                            html.P(
                                html.Span(
                                    [
                                        dbc.Col(dbc.Badge("좋음 : ~ 30", pill=True, color="primary")),
                                        dbc.Col(dbc.Badge("보통 : ~ 80", pill=True, color="success")),
                                        dbc.Col(dbc.Badge("나쁨 : ~ 150", pill=True, color="#ffd414")),
                                        dbc.Col(dbc.Badge("매우 나쁨 : 151 ~", pill=True, color="danger"))
                                    ]
                                ),
                                className="card-text",
                            ),
                        ]
                    )
                ),
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4("한국의 미세먼지 기준은?", className="card-title"),
                            html.P(
                                "한국의 미세먼지 환경기준은 일평균 100㎍/m³ 입니다. WHO의 50㎍/m³나 미국의 150㎍/m³처럼 국가나 기관 마다 그 기준이 다릅니다."
                                "\n Lake House의 웹앱에서는 공공기관-한국 환경 공단 Air Korea-의 실시간 관측 자료를 기반으로 대기상태를 보여드리고 있습니다.",
                                className="card-text",
                            ),
                            dbc.Button(
                                "Air Korea", id = "externalLink", color="success", className="mt-auto", href = 'https://www.airkorea.or.kr/web'
                            ),
                        ]
                    )
                ),
            ]
            ))]),

        ]
    else:
        return "404 Page Error!"


@app.callback(Output('tabs_content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab1':
        return html.Div([

            html.Div([
                dcc.Graph(id='map1',
                          clickData={'points': [{'customdata': '서울'}]}
                          )
            ], style={'width': '49%', 'display': 'inline-block', 'marginTop': '5px', 'padding': '0 20'}),
            html.Div([

                dcc.Graph(id='map2', figure={})
            ], style={'width': '49%', 'display': 'inline-block', 'marginTop': '5px', 'float': 'right'}),
            html.Div(id='graph_content1')
        ])
    elif tab == 'tab2':
        return html.Div([
            html.Div([
                dcc.Graph(id='map3',
                          clickData={'points': [{'customdata': '서울'}]}
                          )
            ], style={'width': '49%', 'display': 'inline-block', 'marginTop': '5px', 'padding': '0 20'}),
            html.Div([
                dcc.Graph(id='map4', figure={})
            ], style={'width': '49%', 'display': 'inline-block', 'marginTop': '5px', 'float': 'right'}),
            html.Div(id='graph_content2')
        ])


@app.callback(
    Output('map1', 'figure'),
    Input('graph_content1', 'value')

)
def update_graph(graph_content1):
    dff = df_sido.copy()

    fig = px.choropleth_mapbox(dff, geojson=state_geo1,
                               locations='sidoname',
                               color='pm10value',
                               color_continuous_scale="portland",
                               range_color=(0, 120),
                               mapbox_style="carto-positron",
                               featureidkey="properties.sidoname",
                               zoom=4.8, center={"lat": 37.565, "lon": 126.986},
                               opacity=0.5,
                               labels={'pm10value': '미세먼지'}
                               )

    fig.update_traces(customdata=dff['sidoname'], selector=dict(type='choroplethmapbox'))
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig


@app.callback(
    Output('map2', 'figure'),
    [Input('graph_content1', 'value'),
     Input('map1', 'clickData')]
)
def update_graph(graph_content1, clickData):
    dff1 = df_city.copy()

    locations = clickData['points'][0]['customdata']
    dff1 = dff1[dff1['sidoname'] == locations]
    i=6

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
        i = 16

    j = 9.2
    if clickData['points'][0]['customdata'] == '강원':
        j = 7
    elif clickData['points'][0]['customdata'] == '인천':
        j = 8.2
    elif clickData['points'][0]['customdata'] == '광주':
        j = 9.2
    elif clickData['points'][0]['customdata'] == '울산':
        j = 8.7
    elif clickData['points'][0]['customdata'] == '대전':
        j = 9.2
    elif clickData['points'][0]['customdata'] == '경기':
        j = 7.5
    elif clickData['points'][0]['customdata'] == '서울':
        j = 9.2
    elif clickData['points'][0]['customdata'] == '대구':
        j = 9
    elif clickData['points'][0]['customdata'] == '부산':
        j = 9
    elif clickData['points'][0]['customdata'] == '충남':
        j = 7.4
    elif clickData['points'][0]['customdata'] == '전남':
        j = 6.9
    elif clickData['points'][0]['customdata'] == '충북':
        j = 7.4
    elif clickData['points'][0]['customdata'] == '전북':
        j = 7.4
    elif clickData['points'][0]['customdata'] == '경남':
        j = 7.2
    elif clickData['points'][0]['customdata'] == '세종':
        j = 9.2
    elif clickData['points'][0]['customdata'] == '경북':
        j = 7

    else:
        j = 8.2

    fig = px.choropleth_mapbox(dff1, geojson=state_geo_s1,
                               locations='full',
                               color='pm10value',
                               color_continuous_scale="portland",
                               range_color=(0, 120),
                               mapbox_style="carto-positron",
                               featureidkey="properties.geofull",
                               zoom=j, center = center_map[i],
                               opacity=0.5,
                               labels={'pm10value': '미세먼지'}
                               )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig


@app.callback(
    Output('map3','figure'),
    Input('graph_content2','value')
)
def update_graph(graph_content2):
    dff = df_sido.copy()

    fig = px.choropleth_mapbox(dff, geojson=state_geo1,
                               locations='sidoname',
                               color='pm25value',
                               color_continuous_scale="portland",
                               range_color=(0, 120),
                               mapbox_style="carto-positron",
                               featureidkey="properties.sidoname",
                               zoom=4.8, center={"lat": 37.565, "lon": 126.986},
                               opacity=0.5,
                               labels={'pm25value': '초미세먼지'}
                               )

    fig.update_traces(customdata=dff['sidoname'], selector=dict(type='choroplethmapbox'))
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig


@app.callback(
    Output('map4', 'figure'),
    [Input('graph_content2', 'value'),
     Input('map3', 'clickData')]
)
def update_graph(graph_content2, clickData):
    dff1 = df_city.copy()

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
        i = 16

    j = 9.2
    if clickData['points'][0]['customdata'] == '강원':
        j = 7
    elif clickData['points'][0]['customdata'] == '인천':
        j = 8.2
    elif clickData['points'][0]['customdata'] == '광주':
        j = 9.2
    elif clickData['points'][0]['customdata'] == '울산':
        j = 8.7
    elif clickData['points'][0]['customdata'] == '대전':
        j = 9.2
    elif clickData['points'][0]['customdata'] == '경기':
        j = 7.5
    elif clickData['points'][0]['customdata'] == '서울':
        j = 9.2
    elif clickData['points'][0]['customdata'] == '대구':
        j = 9
    elif clickData['points'][0]['customdata'] == '부산':
        j = 9
    elif clickData['points'][0]['customdata'] == '충남':
        j = 7.4
    elif clickData['points'][0]['customdata'] == '전남':
        j = 6.9
    elif clickData['points'][0]['customdata'] == '충북':
        j = 7.4
    elif clickData['points'][0]['customdata'] == '전북':
        j = 7.4
    elif clickData['points'][0]['customdata'] == '경남':
        j = 7.2
    elif clickData['points'][0]['customdata'] == '세종':
        j = 9.2
    elif clickData['points'][0]['customdata'] == '경북':
        j = 7

    else:
        j = 8.2

    fig = px.choropleth_mapbox(dff1, geojson=state_geo_s1,
                               locations='full',
                               color='pm25value',
                               color_continuous_scale="portland",
                               range_color=(0, 120),
                               mapbox_style="carto-positron",
                               featureidkey="properties.geofull",
                               zoom=j, center = center_map[i],
                               opacity=0.5,
                               labels={'pm25value': '초미세먼지'}
                               )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig

if __name__ == '__main__':
    application.run(debug=True,port=8080)
