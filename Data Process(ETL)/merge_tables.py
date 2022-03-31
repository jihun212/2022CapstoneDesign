# Databricks notebook source
# MAGIC %md
# MAGIC # Day Week Table: easy format for aggregating by date functions(day, week)

# COMMAND ----------

# MAGIC %sql
# MAGIC USE Capstone

# COMMAND ----------

# MAGIC %sql
# MAGIC -- CREATING A TABLE FOR DAY&WEEK DATETIME MERGE FUNCTION
# MAGIC CREATE TABLE gold_day_week_table
# MAGIC AS
# MAGIC SELECT 
# MAGIC   sidoname,
# MAGIC   cityname,
# MAGIC   pm25value,
# MAGIC   pm10value,
# MAGIC   datetime,
# MAGIC   DATE_TRUNC('day',datetime) AS day,
# MAGIC   DATE_TRUNC('week',datetime) AS week
# MAGIC FROM airpollution_gold

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM gold_day_week_table

# COMMAND ----------

spark.sql("""SELECT sidoname,cityname,pm25value,pm10value,datetime,DATE_TRUNC('day',datetime) AS day,DATE_TRUNC('week',datetime) AS week FROM airpollution_gold""").mode('overwrite').saveAsTable("gold_day_week_table")
