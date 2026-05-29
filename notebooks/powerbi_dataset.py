from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("PowerBIDataset") \
    .getOrCreate()

# Read Gold KPI table
df_gold = spark.read \
    .format("delta") \
    .load("output/gold/nyc_taxi_kpis")

# Dataset exposed to BI tools
df_powerbi = df_gold.select(
    "pickup_month",
    "pickup_hour",
    "payment_type",
    "total_trips",
    "total_revenue",
    "avg_trip_distance",
    "avg_tip_amount",
    "avg_fare_amount"
)

# Save Power BI dataset
df_powerbi.write \
    .format("delta") \
    .mode("overwrite") \
    .save("output/powerbi/nyc_taxi_dashboard")

print("Power BI dataset created successfully.")
