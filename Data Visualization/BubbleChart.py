from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv("2022_BubbleChartTable.csv")

df['datetime'] = pd.to_datetime(df['datetime']).dt.tz_localize(None)
df = df.sort_values("datetime")
df['datetime']=df['datetime'].astype(str)
available_indicators = df['sidoname'].unique()

app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        "도시 선택",
        dcc.Dropdown(
            id='addsido',
            options=[{'label': i, 'value': i} for i in available_indicators],
            value='서울'
        )
    ]),
    html.Div([dcc.Graph(id='graph')])
])

@app.callback(
    Output('graph', 'figure'),
    [Input('addsido', 'value')])

def update_figure(addsido):
    filtered_df = df.loc[df['sidoname'] == addsido]
    fig = px.scatter(filtered_df, x='pm10value',y='pm25value',color='cityname',size='pop',size_max=50,
                     animation_frame='datetime',animation_group='cityname',hover_name='cityname',
                     range_x=[0,150],range_y=[0,150],
                     labels={
                         "pm10value": "미세먼지(pm10value)",
                         "pm25value": "초미세먼지(pm25value)",
                         "cityname": "지역구",
                         "pop": "인구수"
                     })
    fig.update_layout()
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)