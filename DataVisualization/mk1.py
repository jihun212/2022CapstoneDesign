# Databricks notebook source
import plotly.express as px

import pandas as pd

silver = pd.read_csv("/Users/choejihun/Downloads/silver.csv")
gold = pd.read_csv("/Users/choejihun/Downloads/gold.csv")

available_indicators = gold['sidoname'].unique()

radio = 'sidoname'
addsido = '서울'

if radio == 'sidoname':
    filtered_df = silver
elif radio == 'cityname':
    filtered_df = gold



is_sidoname = filtered_df['sidoname'] == '충남'
filtered_df= filtered_df[is_sidoname]

dataframe = gold.append(filtered_df)
print(dataframe.info())

fig = px.scatter(dataframe, x='pm10value',y='pm25value',color='sidoname',size='count',size_max=35,
                 animation_frame='datetime',animation_group='cityname',hover_name='cityname',
                 range_x=[0,150],range_y=[0,150])
# filtered_df = silver[silver['sidoname' == radio]]
# filtered_df = filtered_df.append(gold['sidoname']== addsido)
fig.show()
