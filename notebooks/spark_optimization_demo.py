from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, sum, avg, round

spark = SparkSession.builder \
    .appName("NYCTaxiSparkOptimizationDemo") \
    .getOrCreate()

# Read Silver Delta table
df_silver = spark.read \
    .format("delta") \
    .load("output/silver/nyc_taxi_silver")

# Select only useful columns for analytics workload
df_selected = df_silver.select(
    "pickup_timestamp",
    "payment_type",
    "trip_distance",
    "fare_amount",
    "tip_amount",
    "total_amount"
)

# Filter valid analytical records
df_filtered = df_selected \
    .filter(col("total_amount") > 0) \
    .filter(col("trip_distance") > 0)

# Repartition by payment_type to improve distributed aggregations
df_optimized = df_filtered.repartition("payment_type")

# Cache optimized DataFrame for repeated analytical queries
df_optimized.cache()

# Analytical aggregation
df_payment_summary = df_optimized.groupBy("payment_type") \
    .agg(
        count("*").alias("total_trips"),
        round(sum("total_amount"), 2).alias("total_revenue"),
        round(avg("trip_distance"), 2).alias("avg_trip_distance"),
        round(avg("tip_amount"), 2).alias("avg_tip_amount")
    )

df_payment_summary.show()

# Write optimized analytical dataset
df_payment_summary.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("output/gold/payment_type_analytics")

print("Spark optimization demo completed successfully.")
