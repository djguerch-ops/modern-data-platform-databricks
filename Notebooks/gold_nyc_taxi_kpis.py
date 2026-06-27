# Databricks notebook source
# Databricks notebook source

# ============================================================
# GOLD LAYER - NYC Taxi Business KPIs
# Reads from Silver Delta table and computes
# analytics-ready KPI aggregations
#
# Catalog : nyc_taxi
# Schema  : taxi
# ============================================================

from pyspark.sql.functions import col, count, sum, avg, round

# -------------------------------------------------------
# Configuration
# -------------------------------------------------------
CATALOG      = "nyc_taxi"
SCHEMA       = "taxi"
SILVER_TABLE = f"{CATALOG}.{SCHEMA}.nyc_taxi_silver"
GOLD_TABLE   = f"{CATALOG}.{SCHEMA}.nyc_taxi_kpis"

# -------------------------------------------------------
# Set current catalog and schema
# -------------------------------------------------------
spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA}")

# -------------------------------------------------------
# Read Silver Delta table
# -------------------------------------------------------
print(f"Reading Silver table: {SILVER_TABLE}")

df_silver = spark.table(SILVER_TABLE)
print(f"Silver records: {df_silver.count():,}")

# -------------------------------------------------------
# Compute Gold KPIs
# -------------------------------------------------------
df_gold = df_silver \
    .groupBy("pickup_year", "pickup_month", "pickup_hour", "pickup_day_of_week", "payment_type") \
    .agg(
        count("*").alias("total_trips"),
        round(sum("total_amount"), 2).alias("total_revenue"),
        round(avg("fare_amount"), 2).alias("avg_fare_amount"),
        round(avg("trip_distance"), 2).alias("avg_trip_distance"),
        round(avg("tip_amount"), 2).alias("avg_tip_amount"),
        round(avg("passenger_count"), 2).alias("avg_passenger_count")
    ) \
    .orderBy("pickup_year", "pickup_month", "pickup_hour")

# -------------------------------------------------------
# Write Gold Delta table
# -------------------------------------------------------
print(f"Writing Gold Delta table: {GOLD_TABLE}")

df_gold.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(GOLD_TABLE)

# -------------------------------------------------------
# Validation
# -------------------------------------------------------
gold_count = spark.table(GOLD_TABLE).count()
print(f"Gold KPI table created successfully.")
print(f"Total KPI rows  : {gold_count:,}")
print(f"Table location  : {GOLD_TABLE}")

# Preview top 5 rows
print("\nPreview:")
spark.table(GOLD_TABLE).show(5, truncate=False)