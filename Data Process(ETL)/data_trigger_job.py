# Databricks notebook source
# MAGIC %md
# MAGIC  
# MAGIC ## Data Parsing from Open Api 
# MAGIC 
# MAGIC 
# MAGIC    #### 한국환경공단 - 대기오염
# MAGIC 
# MAGIC https://www.data.go.kr/iim/api/selectAPIAcountView.do

# COMMAND ----------

# MAGIC %md
# MAGIC  
# MAGIC ## Trigger Job notebook 

# COMMAND ----------

# MAGIC %run ../includes/installations

# COMMAND ----------

# MAGIC %run ../includes/path_setup

# COMMAND ----------

import requests
import json
import xmltodict
import time
import pandas as pd
import bs4


pandas_df = pd.DataFrame()

dosi = ['서울','부산','대구','인천','광주','대전','울산','경기','강원','충북','충남','전북','전남','경북','경남','제주','세종']
gu = ['25','16','8','10','5','5','5','31','18','11','15','14','22','23','18','2','1']
i = 0
for i in range(len(dosi)):
    
    url = 'http://apis.data.go.kr/B552584/ArpltnStatsSvc/getCtprvnMesureSidoLIst?sidoName='+dosi[i]+'&searchCondition=DAILY&pageNo=1&numOfRows='+gu[i]+'&returnType=xml&serviceKey=5Ztnnqpm6wBoBE0%2FhONq8zqiXjnydmC7kRuFtT%2BETSA%2Fpw4OlGFCGd83ayCPMVTBTrkxYPyf51hZZ0pcck%2FHNA%3D%3D'
    content = requests.get(url).content
    dict = xmltodict.parse(content)
    jsonString = json.dumps(dict['response']['body']['items'],ensure_ascii=False)
    jsonObj = json.loads(jsonString)
    time.sleep(2)                                   ##need some time to get response from url
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

#append the data

(sparkDf.write.format("delta")\
.mode("append").partitionBy("sidoname")\
.option("mergeSchema", "true")\
.save(bronze_path))

# COMMAND ----------

# MAGIC %sql
# MAGIC --DROP TABLE IF EXISTS airpollution_bronze;
# MAGIC --
# MAGIC --DROP TABLE IF EXISTS airpollution_silver;
# MAGIC --
# MAGIC --DROP TABLE IF EXISTS airpollution_gold;

# COMMAND ----------

# MAGIC %md
# MAGIC # Bronze Table: Raw Table 

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY bronze_path

# COMMAND ----------

#Creating bronze table 
(spark.read
 .format("delta")
 .options(inferschema = True)
 .load(bronze_path)
 .createOrReplaceTempView("airpollution_bronze_1"))

# COMMAND ----------

spark.sql("""SELECT * FROM airpollution_bronze_1""").write.partitionBy("sidoname").mode("overwrite").saveAsTable("airpollution_bronze")

# COMMAND ----------

# MAGIC %md
# MAGIC # Silver Table: Cleaned Table
# MAGIC 
# MAGIC selected only sidoname,cityname,pm10value,pm25valuel, datetime value 

# COMMAND ----------

#silver table

spark.sql("""SELECT sidoname, cityname, pm10value, pm25value, datatime as datetime 
FROM airpollution_bronze_1""").write.partitionBy("sidoname").mode("overwrite").saveAsTable("airpollution_silver")

# COMMAND ----------

# MAGIC %md
# MAGIC # Gold Table: Aggregated Table
# MAGIC Average pm10, pm2.5 value of each "시도"

# COMMAND ----------

#gold temporary table

spark.sql("""SELECT sidoname, ROUND(AVG(pm10value)) AS pm10value, ROUND(AVG(pm25value)) AS pm25value, datetime FROM airpollution_silver GROUP BY sidoname,datetime""").write.format("delta").partitionBy("sidoname").mode("overwrite").saveAsTable("airpollution_gold")

# COMMAND ----------

# MAGIC %md
# MAGIC # Optimizing the data files

# COMMAND ----------

# MAGIC %sql
# MAGIC OPTIMIZE airpollution_silver;
# MAGIC OPTIMIZE airpollution_bronze;
