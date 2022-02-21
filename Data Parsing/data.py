# Databricks notebook source
# MAGIC %md
# MAGIC  
# MAGIC ## Data Parsing from Open Api 
# MAGIC 
# MAGIC 
# MAGIC    ####한국환경공단 - 대기오염
# MAGIC 
# MAGIC https://www.data.go.kr/iim/api/selectAPIAcountView.do

# COMMAND ----------

# MAGIC %run ../includes/installations

# COMMAND ----------

from pyspark.sql.types import *

customschema = StructType([
    StructField("so2Value",  DoubleType(), False),
    StructField("coValue", DoubleType(), False),
    StructField("cityName", StringType(), False),
    StructField("cityNameEng", StringType(), False),
    StructField("pm10Value", IntegerType(), False),
    StructField("datatime", TimestampType(), False),
    StructField("no2Value", DoubleType(), False),
    StructField("districtnumseq", IntegerType(), False),
    StructField("o3Value", DoubleType(), False),
    StructField("pm25Value", IntegerType(), False),
    StructField("sidoName", StringType(), False)])

# COMMAND ----------


import requests
import json
import xmltodict

import pandas as pd
import bs4


pandas_df = pd.DataFrame()

dosi = ['서울','경기','인천']
gu = ['25','31','10']
i = 0
for i in range(len(dosi)):
    
    url = 'http://apis.data.go.kr/B552584/ArpltnStatsSvc/getCtprvnMesureSidoLIst?sidoName='+dosi[i]+'&searchCondition=DAILY&pageNo=1&numOfRows='+gu[i]+'&returnType=xml&serviceKey=5Ztnnqpm6wBoBE0%2FhONq8zqiXjnydmC7kRuFtT%2BETSA%2Fpw4OlGFCGd83ayCPMVTBTrkxYPyf51hZZ0pcck%2FHNA%3D%3D'
    content = requests.get(url).content
    dict = xmltodict.parse(content)
    jsonString = json.dumps(dict['response']['body']['items'],ensure_ascii=False)
    jsonObj = json.loads(jsonString)
    for item in jsonObj['item'] :
        obj = bs4.BeautifulSoup(content,'lxml')
        rows = obj.findAll('item')


        row_list = []
        name_list = []
        value_list = []

        i = 0
        for i in range(0, len(rows)):
            columns = rows[i].find_all()
            for j in range(0,len(columns)):
                if i ==0:
                    name_list.append(columns[j].name)
                value_list.append(columns[j].text)
            row_list.append(value_list)
            value_list=[]

    dust_df = pd.DataFrame(row_list, columns=name_list)
    pandas_df = pd.concat((pandas_df,dust_df), axis =0, sort=False)

# COMMAND ----------

print(pandas_df)

# COMMAND ----------

#Erase 'khaivalue' column
del pandas_df['khaivalue']

# COMMAND ----------

from pyspark.sql.functions import *

#transform pandas dataframe to Spark Dataframe 
sparkDf = spark.createDataFrame(pandas_df)

#Change Dataframe Schema 
sparkDf = (sparkDf.withColumn("so2value", col("so2value").cast("double"))
.withColumn("covalue", col("covalue").cast("double"))
.withColumn("pm10value", col("pm10value").cast("integer"))
.withColumn("datatime", col("datatime").cast("timestamp"))
.withColumn("no2value", col("no2value").cast("double"))
.withColumn("districtnumseq", col("districtnumseq").cast("integer"))
.withColumn("o3value", col("o3value").cast("double"))
.withColumn("pm25value", col("pm25value").cast("integer")))

# COMMAND ----------

display(pandas_df)

# COMMAND ----------


sparkDf.write.format("delta").partitionBy("sidoname").mode("overwrite").option("overwriteSchema", "true").save("dbfs:/tmp/air_pollution/raw")

# COMMAND ----------

#check out the schema of spark dataframe in the storage
sample_df = spark.read.format("delta").load("dbfs:/tmp/air_pollution/raw")
sampld_df.printSchema()
