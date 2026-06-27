# Databricks notebook source
# Databricks notebook source

# ============================================================
# SILVER LAYER - NYC Taxi Transformations & Data Quality
# Reads from Bronze Delta table, applies quality filters,
# and writes to Silver Delta table in Unity Catalog
#
# Catalog : nyc_taxi
# Schema  : taxi
# ============================================================

from pyspark.sql.functions import col, to_timestamp, hour, dayofweek, month, year

# -------------------------------------------------------
# Configuration
# -------------------------------------------------------
CATALOG       = "nyc_taxi"
SCHEMA        = "taxi"
BRONZE_TABLE  = f"{CATALOG}.{SCHEMA}.nyc_taxi_bronze"
SILVER_TABLE  = f"{CATALOG}.{SCHEMA}.nyc_taxi_silver"

# -------------------------------------------------------
# Set current catalog and schema
# -------------------------------------------------------
spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA}")

# -------------------------------------------------------
# Read Bronze Delta table
# -------------------------------------------------------
print(f"Reading Bronze table: {BRONZE_TABLE}")

df_bronze = spark.table(BRONZE_TABLE)
print(f"Bronze records: {df_bronze.count():,}")

# -------------------------------------------------------
# Data quality filtering
# -------------------------------------------------------
df_silver = df_bronze \
    .filter(col("trip_distance") > 0) \
    .filter(col("trip_distance") < 200) \
    .filter(col("fare_amount") > 0) \
    .filter(col("fare_amount") < 500) \
    .filter(col("passenger_count") > 0) \
    .filter(col("passenger_count") <= 6) \
    .filter(col("tpep_pickup_datetime").isNotNull()) \
    .filter(col("tpep_dropoff_datetime").isNotNull())\
    .filter(year(col("tpep_pickup_datetime")) == 2026)

# -------------------------------------------------------
# Timestamp conversion + derived columns
# -------------------------------------------------------
df_silver = df_silver \
    .withColumn("pickup_timestamp", to_timestamp(col("tpep_pickup_datetime"))) \
    .withColumn("dropoff_timestamp", to_timestamp(col("tpep_dropoff_datetime"))) \
    .withColumn("pickup_hour", hour(col("tpep_pickup_datetime"))) \
    .withColumn("pickup_day_of_week", dayofweek(col("tpep_pickup_datetime"))) \
    .withColumn("pickup_month", month(col("tpep_pickup_datetime"))) \
    .withColumn("pickup_year", year(col("tpep_pickup_datetime")))

# -------------------------------------------------------
# Remove duplicates
# -------------------------------------------------------
df_silver = df_silver.dropDuplicates()

# -------------------------------------------------------
# Write Silver Delta table
# -------------------------------------------------------
print(f"Writing Silver Delta table: {SILVER_TABLE}")

df_silver.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(SILVER_TABLE)

# -------------------------------------------------------
# Validation
# -------------------------------------------------------
silver_count = spark.table(SILVER_TABLE).count()
bronze_count = df_bronze.count()
rejected     = bronze_count - silver_count

print(f"Silver transformation completed successfully.")
print(f"Bronze records  : {bronze_count:,}")
print(f"Silver records  : {silver_count:,}")
print(f"Rejected records: {rejected:,} ({rejected/bronze_count*100:.1f}%)")
print(f"Table location  : {SILVER_TABLE}")