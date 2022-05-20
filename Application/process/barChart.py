import pandas as pd
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import numpy as np
import dash_bootstrap_components as dbc
from dash import html, callback, Input, Output, dcc
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import process.load as L
df = L.load_lineC()

df20 = pd.read_csv("2020_pm_dataset.csv")
df19 = pd.read_csv("2019_pm_dataset.csv")
df21 = pd.read_csv("2021_pm_dataset.csv")

df19.rename(columns = {'PM10' : 'pm10value'}, inplace = True)
df19.rename(columns = {'PM25' : 'pm25value'}, inplace = True)

df_past = pd.concat([df19, df20, df21], ignore_index=True)
df_past['datetime'] = pd.to_datetime(df_past['datetime']).dt.tz_localize(None)
df_past['month']=df_past['datetime'].dt.month
df_past['year']=df_past['datetime'].dt.year
# list_month = df_past['datetime'].dt.month.unique()
list_year = df_past['datetime'].dt.year.unique()

df['datetime'] = pd.to_datetime(df['datetime']).dt.tz_localize(None)
df['month']=df['datetime'].dt.month
df.sort_values('month')
df['year']=df['datetime'].dt.year

# list_month =np.concatenate((list_month, df['datetime'].dt.month.unique()))
list_year =np.concatenate((list_year, df['datetime'].dt.year.unique()))
list_month = df['datetime'].dt.month.unique()

# list_month = np.unique(list_month)
list_year = np.unique(list_year)
# print(np.concatenate((available_indicators_past, available_indicators_past2), axis=None))

layout = html.Div([
    html.Div([
        html.H4("연도 선택"),
        dcc.Dropdown(
            id='year',
            options=[{'label': i, 'value': i} for i in list_year],
            value=list_year[-1]
        )
    ]),
    html.Div([
        html.H4("월 선택"),
        dcc.Dropdown(
            id='month',
            options=[{'label': i, 'value': i} for i in list_month],
            value=sorted(list_month)[-1]
            # value=list_month[-1]
        )
    ]),
    html.Div([dcc.Graph(id='graph')])
])

@callback(
    Output("month", "options"),
    Input("year", "value")
)

def update_options(year):
    if year==2022:
        list_month = df['datetime'].dt.month.unique()
    else:
        list_month = df_past['datetime'].dt.month.unique()

    return list_month

@callback(
    Output('graph', 'figure'),
    [Input('year', 'value'),
     Input('month', 'value')])



def update_figure(year, month):
    if(year == 2022):
        df_use = df
    else:
        df_use = df_past
    filtered_df = df_use.loc[df_use['year'] == year]
    filtered_df = filtered_df.loc[filtered_df['month'] == month]

    list_month = filtered_df['datetime'].dt.month.unique()

    dftime = filtered_df.groupby('sidoname').sum().reset_index()

    dftime['rank_by_average'] = dftime['pm10value'].rank(ascending=False,method = 'min') # rank default method='average
    dftime = dftime.sort_values(by='rank_by_average')

    if ((dftime['pm10value'].max() - dftime['pm10value'].min()) > 100000):
        round_down = 100000
    elif ((dftime['pm10value'].max() - dftime['pm10value'].min()) > 10000):
        round_down = 10000
    elif ((dftime['pm10value'].max() - dftime['pm10value'].min()) > 1000):
        round_down = 1000
    elif ((dftime['pm10value'].max() - dftime['pm10value'].min()) > 100):
        round_down = 100
    elif ((dftime['pm10value'].max() - dftime['pm10value'].min()) > 10):
        round_down = 10
    else:
        round_down = 1
    fig = px.bar(dftime, x='pm10value', y='sidoname', color='sidoname')
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})  # add only this line
    fig.update_xaxes(range=[np.floor(dftime['pm10value'].min() / round_down) * round_down,
                            np.ceil(dftime['pm10value'].max() / round_down) * round_down])
    fig.update_layout(title_text='%d년도 %d월달 미세먼지 데이터 총합' % (year, month))
    fig.update_layout(xaxis_title='미세먼지', yaxis_title='도시')
    # fig.update_layout(showlegend=False,font=dict(
    #     size=20
    # ))
    fig.update_layout(showlegend=False)
    fig.update_layout()
    return fig