# Databricks notebook source
# MAGIC %md 
# MAGIC 
# MAGIC ### Environment Set-up
# MAGIC - Mandatory installation
# MAGIC - Data Schema 

# COMMAND ----------

pip install xmltodict

# COMMAND ----------

pip install lxml

# COMMAND ----------

pip install beautifulsoup4 

# COMMAND ----------

#Dataframe Schema 
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
