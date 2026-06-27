# Databricks notebook source
# Databricks notebook source

# ============================================================
# BRONZE LAYER - NYC Taxi Raw Ingestion
# Reads Parquet files from Unity Catalog Volume
# and writes to Bronze Delta table
#
# Catalog : nyc_taxi
# Schema  : taxi
# Volume  : nyc_taxi_data
# ============================================================

from pyspark.sql.functions import current_timestamp, col

# -------------------------------------------------------
# Configuration
# -------------------------------------------------------
CATALOG       = "nyc_taxi"
SCHEMA        = "taxi"
VOLUME_PATH   = f"/Volumes/{CATALOG}/{SCHEMA}/nyc_taxi_data"
SOURCE_PATH   = f"{VOLUME_PATH}/*.parquet"
BRONZE_TABLE  = f"{CATALOG}.{SCHEMA}.nyc_taxi_bronze"

# -------------------------------------------------------
# Set current catalog and schema
# -------------------------------------------------------
spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA}")

# -------------------------------------------------------
# Read raw Parquet files from Volume
# -------------------------------------------------------
print(f"Reading Parquet files from: {SOURCE_PATH}")

df_raw = spark.read \
    .option("mergeSchema", "true") \
    .parquet(SOURCE_PATH)

print(f"Raw records read: {df_raw.count():,}")

# -------------------------------------------------------
# Add ingestion metadata
# -------------------------------------------------------
df_bronze = df_raw \
    .withColumn("ingestion_timestamp", current_timestamp()) \
    .withColumn("source_file", col("_metadata.file_path"))

# -------------------------------------------------------
# Write Bronze Delta table (Unity Catalog managed table)
# -------------------------------------------------------
print(f"Writing Bronze Delta table: {BRONZE_TABLE}")

df_bronze.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(BRONZE_TABLE)

# -------------------------------------------------------
# Validation
# -------------------------------------------------------
record_count = spark.table(BRONZE_TABLE).count()
print(f"Bronze ingestion completed successfully.")
print(f"Total records in Bronze table: {record_count:,}")
print(f"Table location: {BRONZE_TABLE}")