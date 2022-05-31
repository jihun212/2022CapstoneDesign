import pandas as pd
import plotly.graph_objs as go

from dash import Dash, dcc, html, Input, Output

df20 = pd.read_csv("2020_pm_dataset.csv")
df19 = pd.read_csv("2019_pm_dataset.csv")
df21 = pd.read_csv("2021_pm_dataset.csv")
df22 = pd.read_csv("2022_pm_dataset.csv")

df22['datetime'] = pd.to_datetime(df22['datetime']).dt.tz_localize(None)
df20['datetime'] = pd.to_datetime(df20['datetime']).dt.tz_localize(None)
df19['datetime'] = pd.to_datetime(df19['datetime']).dt.tz_localize(None)
df21['datetime'] = pd.to_datetime(df21['datetime']).dt.tz_localize(None)

available_indicators = df22['datetime'].dt.month.unique()
now_month=available_indicators[-1]

frame22 = df22.loc[(df22['datetime'].dt.month == now_month) | (df22['datetime'].dt.month == now_month+1)]
frame21 = df21.loc[(df21['datetime'].dt.month == now_month) | (df21['datetime'].dt.month == now_month+1)]
frame20 = df20.loc[(df20['datetime'].dt.month == now_month) | (df20['datetime'].dt.month == now_month+1)]
frame19 = df19.loc[(df19['datetime'].dt.month == now_month) | (df19['datetime'].dt.month == now_month+1)]

frame22 = frame22.sort_values("datetime")
frame20 = frame20.sort_values("datetime")
frame19 = frame19.sort_values("datetime")
frame21 = frame21.sort_values("datetime")
frame22=frame22.groupby(pd.Grouper(key='datetime',freq='D')).mean().reset_index()
frame21=frame21.groupby(pd.Grouper(key='datetime',freq='D')).mean().reset_index()
frame20=frame20.groupby(pd.Grouper(key='datetime',freq='D')).mean().reset_index()
frame19=frame19.groupby(pd.Grouper(key='datetime',freq='D')).mean().reset_index()

frame22['month']=frame22['datetime'].dt.month
frame22['dayday']=frame22['datetime'].dt.day
frame22['monthday']= frame22['month'].astype(str) + '월 ' + frame22['dayday'].astype(str) +'일'
frame20['month']=frame20['datetime'].dt.month
frame20['dayday']=frame20['datetime'].dt.day
frame20['monthday']= frame20['month'].astype(str) + '월 ' + frame20['dayday'].astype(str) +'일'
frame19['month']=frame19['datetime'].dt.month
frame19['dayday']=frame19['datetime'].dt.day
frame19['monthday']= frame19['month'].astype(str) + '월 ' + frame19['dayday'].astype(str) +'일'
frame19['pm10value']=frame19['PM10']
frame21['month']=frame21['datetime'].dt.month
frame21['dayday']=frame21['datetime'].dt.day
frame21['monthday']= frame21['month'].astype(str) + '월 ' + frame21['dayday'].astype(str) +'일'

app = Dash(__name__)
fig = go.Figure()
fig.add_trace(go.Scatter(x=frame22['monthday'], y=frame22['pm10value'], line={'width':5}, mode='lines',name='2022년',connectgaps=True))
fig.add_trace(go.Scatter(x=frame21['monthday'], y=frame21['pm10value'], mode='lines',name='2021년',connectgaps=True))
fig.add_trace(go.Scatter(x=frame20['monthday'], y=frame20['pm10value'], mode='lines',name='2020년',connectgaps=True))
fig.add_trace(go.Scatter(x=frame19['monthday'], y=frame19['pm10value'], mode='lines',name='2019년',connectgaps=True))

app.layout = html.Div([
    html.Div([dcc.Graph(figure=fig)])
])

if __name__ == '__main__':
    app.run_server(debug=True)