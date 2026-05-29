from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp

# Create Spark session
spark = SparkSession.builder \
    .appName("NYCTaxiSilverTransformations") \
    .getOrCreate()

# Read Bronze Delta table
df_bronze = spark.read \
    .format("delta") \
    .load("output/bronze/nyc_taxi_bronze")

# Data quality filtering
df_silver = df_bronze \
    .filter(col("trip_distance") > 0) \
    .filter(col("fare_amount") > 0) \
    .filter(col("passenger_count") > 0)

# Timestamp conversion
df_silver = df_silver \
    .withColumn(
        "pickup_timestamp",
        to_timestamp(col("tpep_pickup_datetime"))
    ) \
    .withColumn(
        "dropoff_timestamp",
        to_timestamp(col("tpep_dropoff_datetime"))
    )

# Remove duplicate rows
df_silver = df_silver.dropDuplicates()

# Write Silver Delta table
df_silver.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("output/silver/nyc_taxi_silver")

print("Silver layer transformation completed successfully.")
