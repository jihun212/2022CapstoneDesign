# Databricks notebook source
# MAGIC %md 
# MAGIC #### To-do List
# MAGIC ##### 1. SET UP PATHWAY & ENVIRONMENT(환경설정)
# MAGIC ##### 2. DATAFRAME -> DELTA FORMAT & STORE AT S3 BUCKET (데이터 변환 및 S3 BUCKET에 저장)
# MAGIC ##### 3. MAKE BRONZE TABLE(RAW) (BRONZE TABLE 작성, RAW DATA)
# MAGIC ##### 4. CLEAN THE DATA (데이터 전처리)
# MAGIC ##### 5. MAKE SILVER TABLE(CLEANED) (SILVER TABLE 작성)
# MAGIC ##### 6. AGGREGATE SILVER TABLE -> MAKE GOLD TABLE(AGGREGATED) (최종 데이터 작성 및 저장)
# MAGIC ##### 7. USE TRIGGER (1시간마다 코드 실행하기 설정)
# MAGIC - auto vacuum 
# MAGIC spark.conf.set("spark.databricks.delta.retentionDurationCheck.enabled", False)

# COMMAND ----------

raw_path = "dbfs:/tmp/air_pollution/raw"

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE DATABASE IF NOT EXISTS Capstone;
# MAGIC USE Capstone
