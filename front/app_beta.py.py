# Databricks notebook source
from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import dash_html_components as html
import base64
import csv
from datetime import date


external_stylesheets = ["https://api.mapbox.com/styles/v1/dalet0831/cl0ou1nxi001z15pojf4gz212/draft"]
app = Dash(__name__, external_stylesheets=external_stylesheets)


image_directory='/C:/Users/jjeun/AppData/Local/Programs/Python/Python39/'
image_filename = 'LakeHouseLogo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

colors = {
    'background': '#111111',
    'text': '#FFFFFF',
    'B' : '#000000'
}



app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.Div([
        html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={'float' : 'left', 'padding-left' : '30px', 'margin-top': '10px'})
        ]),
    
    html.H1(
        children='실시간 미세먼지',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'margin-top': '20px'
        }
    ),

    html.Div(children='대한민국의 미세먼지 정보를 실시간으로 알려드립니다.', style={
        'textAlign': 'center',
        'color': colors['text'],
        'margin-top': '25px'
    }),


    html.Div(children='날짜와 시간을 정할 수 있습니다. 월 / 일 / 시', style={
        'margin-top': '60px', 'padding-top':'15px', 'padding-bottom':'15px', 'padding-left' : '20px',
        'textAlign': 'left',
        'color': colors['text']
    }),

    html.Div([
        dcc.DatePickerSingle(
            id='my-date-picker-single',
            min_date_allowed=date(2000, 1, 1),
            max_date_allowed=date(2022,3,14),
            initial_visible_month=date(2022,3,14),
            date=date(2022, 3, 13)
        ),
        html.Div(id='output-contaiiner-date-picker-single',
                 style={'float' : 'right','padding-left' : '40px', 'vertical-align':'middle', 'text-align':'center'})
    ]),

    html.Div([
        dcc.Dropdown(['00','01','02', '03', '04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23'],
                     style={'padding-left' : '150px', 'width':'auto','color': colors['B']})
        

    ]),

    html.Div([

    html.Iframe(src="https://api.mapbox.com/styles/v1/dalet0831/cl0ou1nxi001z15pojf4gz212.html?title=view&access_token=pk.eyJ1IjoiZGFsZXQwODMxIiwiYSI6ImNrendicW1xMDg0amsyb3R2MXo2eXQ0bWMifQ.0Xq3q2Y3GjRqQOyDYfLqdg&zoomwheel=true&fresh=true#6.74/36.463/128.855",
                style={'margin-left' : '20px', 'height': '500px', 'width': '40%'})

    
])


    
])

if __name__ == '__main__':
    app.run_server(debug=True)
