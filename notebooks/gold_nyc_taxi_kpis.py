from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    count,
    sum,
    avg,
    date_format,
    hour,
    round
)

# Create Spark session
spark = SparkSession.builder \
    .appName("NYCTaxiGoldKPIs") \
    .getOrCreate()

# Read Silver Delta table
df_silver = spark.read \
    .format("delta") \
    .load("output/silver/nyc_taxi_silver")

# Create business KPI table
df_gold = df_silver \
    .withColumn("pickup_month", date_format(col("pickup_timestamp"), "yyyy-MM")) \
    .withColumn("pickup_hour", hour(col("pickup_timestamp"))) \
    .groupBy("pickup_month", "pickup_hour", "payment_type") \
    .agg(
        count("*").alias("total_trips"),
        round(sum("total_amount"), 2).alias("total_revenue"),
        round(avg("trip_distance"), 2).alias("avg_trip_distance"),
        round(avg("tip_amount"), 2).alias("avg_tip_amount"),
        round(avg("fare_amount"), 2).alias("avg_fare_amount")
    ) \
    .orderBy("pickup_month", "pickup_hour", "payment_type")

# Write Gold Delta table
df_gold.write \
    .format("delta") \
    .mode("overwrite") \
    .save("output/gold/nyc_taxi_kpis")

print("Gold KPI table created successfully.")
