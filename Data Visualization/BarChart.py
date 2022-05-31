import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import numpy as np

df20 = pd.read_csv("2020_pm_dataset.csv")
df19 = pd.read_csv("2019_pm_dataset.csv")
df21 = pd.read_csv("2021_pm_dataset.csv")

df19.rename(columns = {'PM10' : 'pm10value'}, inplace = True)
df19.rename(columns = {'PM25' : 'pm25value'}, inplace = True)

df_past = pd.concat([df19, df20, df21], ignore_index=True)
df_past['datetime'] = pd.to_datetime(df_past['datetime']).dt.tz_localize(None)
df_past['month']=df_past['datetime'].dt.month
df_past['year']=df_past['datetime'].dt.year
list_year = df_past['datetime'].dt.year.unique()

df = pd.read_csv("2022_pm_dataset.csv")
df['datetime'] = pd.to_datetime(df['datetime']).dt.tz_localize(None)
df['month']=df['datetime'].dt.month
df['year']=df['datetime'].dt.year

list_year =np.concatenate((list_year, df['datetime'].dt.year.unique()))
list_month = df['datetime'].dt.month.unique()

list_year = np.unique(list_year)

app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        "년도 선택",
        dcc.Dropdown(
            id='year',
            options=[{'label': i, 'value': i} for i in list_year],
            value=list_year[-1]
        )
    ]),
    html.Div([
        "월 선택",
        dcc.Dropdown(
            id='month',
            options=[{'label': i, 'value': i} for i in list_month],
            value=sorted(list_month)[-1]
        )
    ]),
    html.Div([dcc.Graph(id='graph')])
])

@app.callback(
    Output("month", "options"),
    Input("year", "value")
)

def update_options(year):
    #2022년도와 이전년도 테이블 레이블이 다르기 때문에 일단 하드코딩함
    # 레이블 통일하면 year==list_year[-1]로 테이블 업데이트에 최적화
    if year==2022:
        list_month = df['datetime'].dt.month.unique()
    else:
        list_month = df_past['datetime'].dt.month.unique()

    return list_month

@app.callback(
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
    dftime = filtered_df.groupby('sidoname').sum().reset_index()

    dftime['rank_by_average'] = dftime['pm10value'].rank(ascending=False,method = 'min') # rank default method='average
    dftime = dftime.sort_values(by='rank_by_average')


    # 그래프 min_max 설
    if((dftime['pm10value'].max()-dftime['pm10value'].min())>100000):
        round_down=100000
    elif((dftime['pm10value'].max()-dftime['pm10value'].min())>10000):
        round_down=10000
    elif((dftime['pm10value'].max()-dftime['pm10value'].min())>1000):
        round_down=1000
    elif((dftime['pm10value'].max()-dftime['pm10value'].min())>100):
        round_down=100
    elif((dftime['pm10value'].max()-dftime['pm10value'].min())>10):
        round_down=10
    else:
        round_down=1

    fig = px.bar(dftime, x='pm10value', y='sidoname',color='sidoname')
    fig.update_layout(yaxis={'categoryorder':'total ascending'}) # add only this line
    fig.update_xaxes(range=[np.floor(dftime['pm10value'].min()/round_down)* round_down,np.ceil(dftime['pm10value'].max()/round_down)*round_down])
    fig.update_layout(title_text='%d년도 %d월달 미세먼지 수치 총합'%(year,month))
    fig.update_layout(xaxis_title='미세먼지', yaxis_title='도시')
    fig.update_layout(showlegend=False)
    fig.update_layout()
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)