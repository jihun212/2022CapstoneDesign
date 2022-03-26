# Databricks notebook source
# MAGIC %md 
# MAGIC ### Merge Dataset(2021.01 ~ 2021.07)

# COMMAND ----------

import pandas as pd

df1 = pd.read_excel("2021_1.xlsx")
df2 = pd.read_excel("2021_2.xlsx")
df3 = pd.read_excel("2021_3.xlsx")
df4 = pd.read_excel("2021_4.xlsx")
df5 = pd.read_excel("2021_5.xlsx")
df6 = pd.read_excel("2021_6.xlsx")
df7 = pd.read_excel("2021_7.xlsx")

sidoname = ['서울','부산','대구','인천','광주','대전','울산','경기','강원','충북','충남','전북','전남','경북','경남','제주','세종']
merge_df = pd.DataFrame()


# COMMAND ----------

## add sidoname column function
def add_sidoname(sidoname,df):
    fil_df = df.loc[:,('지역','PM10','PM25','측정일시')]
    new_df = fil_df[fil_df['지역'].str.contains(sidoname)]
    new_df['sidoname'] = sidoname
    return new_df

## Merging Dataset Function
def merge_dataset(df):
        i=0
        raw_df = pd.DataFrame()
        final_df = pd.DataFrame()
        for i in range(len(sidoname)):
            sido_df = add_sidoname(sidoname[i],df)
            final_df = pd.concat([sido_df,final_df])
        group_by_df =final_df.groupby(['sidoname','측정일시'])['PM10','PM25'].mean()
        group_by_df.reset_index(inplace=True)
        raw_df = pd.concat([group_by_df,raw_df])
        return raw_df

# COMMAND ----------

##데이터 합치기
final = final.append(merge_dataset(df1))
final = final.append(merge_dataset(df2))
final = final.append(merge_dataset(df3))
final = final.append(merge_dataset(df4))
final = final.append(merge_dataset(df5))
final = final.append(merge_dataset(df6))
final = final.append(merge_dataset(df7))


# COMMAND ----------

##데이터 저장하기
final.to_csv('2021_pm_dataset.csv')
