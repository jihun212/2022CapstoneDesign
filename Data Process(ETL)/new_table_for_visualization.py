# Databricks notebook source
# MAGIC %md
# MAGIC # Test Version of Merge table 
# MAGIC adding new column, test version of merging two tables(silver, gold)

# COMMAND ----------

# MAGIC %sql
# MAGIC USE Capstone

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM
# MAGIC (SELECT *
# MAGIC FROM
# MAGIC (SELECT
# MAGIC   sidoname,
# MAGIC   sidoname as cityname,
# MAGIC   pm10value,
# MAGIC   pm25value,
# MAGIC   count,
# MAGIC   datetime
# MAGIC FROM
# MAGIC (SELECT 
# MAGIC   sidoname, 
# MAGIC   ROUND(AVG(pm10value)) AS pm10value, 
# MAGIC   ROUND(AVG(pm25value)) AS pm25value, 
# MAGIC   COUNT(*) AS count,
# MAGIC   datetime 
# MAGIC FROM airpollution_silver 
# MAGIC WHERE 
# MAGIC   datetime IS NOT NULL
# MAGIC GROUP BY sidoname,datetime) gold_temp
# MAGIC 
# MAGIC UNION ALL 
# MAGIC 
# MAGIC SELECT *
# MAGIC FROM 
# MAGIC (SELECT 
# MAGIC   sidoname,
# MAGIC   cityname,
# MAGIC   pm10value,
# MAGIC   pm25value,
# MAGIC   count(*) as count, 
# MAGIC   datetime
# MAGIC FROM airpollution_silver
# MAGIC WHERE 
# MAGIC   datetime is not null
# MAGIC GROUP BY 
# MAGIC   sidoname,
# MAGIC   cityname,
# MAGIC   pm10value,
# MAGIC   pm25value,
# MAGIC   datetime ) merge_temp))

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   sidoname,
# MAGIC   sidoname as cityname,
# MAGIC   pm10value,
# MAGIC   pm25value,
# MAGIC   count,
# MAGIC   datetime
# MAGIC FROM
# MAGIC (SELECT 
# MAGIC   sidoname, 
# MAGIC   ROUND(AVG(pm10value)) AS pm10value, 
# MAGIC   ROUND(AVG(pm25value)) AS pm25value, 
# MAGIC   COUNT(*) AS count,
# MAGIC   datetime 
# MAGIC FROM airpollution_silver 
# MAGIC WHERE 
# MAGIC   datetime IS NOT NULL
# MAGIC GROUP BY sidoname,datetime) gold_temp

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TEMPORARY VIEW sample_merge
# MAGIC AS
# MAGIC   (SELECT * FROM airpollution_silver)

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TEMPORARY VIEW sample_merge_1
# MAGIC AS
# MAGIC (SELECT * FROM airpollution_silver UNION ALL SELECT 
# MAGIC   sidoname,
# MAGIC   sidoname as cityname,
# MAGIC   pm10value,
# MAGIC   pm25value,
# MAGIC   datetime
# MAGIC FROM airpollution_gold
# MAGIC )

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM sample_merge_1
