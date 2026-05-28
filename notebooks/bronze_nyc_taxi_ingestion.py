from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp

# Create Spark session
spark = SparkSession.builder \
    .appName("NYCTaxiBronzeIngestion") \
    .getOrCreate()

# Source path for NYC Taxi Parquet files
source_path = "datasets/nyc_taxi/*.parquet"

# Read raw Parquet files
df_raw = spark.read.parquet(source_path)

# Add ingestion metadata
df_bronze = df_raw.withColumn(
    "ingestion_timestamp",
    current_timestamp()
)

# Write Bronze Delta table
df_bronze.write \
    .format("delta") \
    .mode("overwrite") \
    .save("output/bronze/nyc_taxi_bronze")

print("Bronze ingestion completed successfully.")
