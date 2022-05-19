from dash import html, callback, Input, Output, dcc
import process.load as L
import plotly.express as px
import dash_bootstrap_components as dbc

df_ap, available_indicators, ap_time_list = L.load_addpop()

layout = [
            html.Div([
                html.Div([
                    dbc.Alert("도시 선택" ,color = "secondary"),
                    dcc.Dropdown(
                        id='addsido',
                        options=[{'label': i, 'value': i} for i in available_indicators],
                        value='서울'
                    )
                ]),
                html.Div([dcc.Graph(id='graph_7')])
            ])

]

@callback(
    Output("graph_7", "figure"),
    [Input('addsido', 'value')]
)
def update_figure(addsido):

    filtered_df = df_ap.loc[df_ap['sidoname'] == addsido]

    fig = px.scatter(filtered_df, x='pm10value',y='pm25value',color='cityname',size='pop',size_max=30,
                     animation_frame='datetime',animation_group='cityname',hover_name='cityname',
                     range_x=[0,150],range_y=[0,100], width=1200, height=600,
                     labels={
                         "pm10value": "미세먼지(pm10value)",
                         "pm25value": "초미세먼지(pm25value)",
                         "cityname": "지역구",
                         "pop": "인구수"
                     })

    fig.update_layout()

    return fig
