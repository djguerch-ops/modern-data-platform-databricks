# Import required libraries
from pyspark.sql.functions import current_timestamp

# Source location containing incoming Parquet files
source_path = "/Volumes/workspace_7474648309056393/default/nyc_taxi_volume/raw_streaming"

# Checkpoint location used by Auto Loader
checkpoint_path = "/Volumes/workspace_7474648309056393/default/nyc_taxi_volume/checkpoints/autoloader"

# Target Bronze Delta table
target_table = "workspace_7474648309056393.default.nyc_taxi_bronze_autoloader"

# Read incoming files using Databricks Auto Loader
df_stream = (
    spark.readStream
    .format("cloudFiles").option("cloudFiles.schemaLocation", "/Volumes/workspace_7474648309056393/default/nyc_taxi_volume/schema")

    .option("cloudFiles.format", "parquet")
    .load(source_path)
)

# Add ingestion timestamp
df_stream = df_stream.withColumn(
    "ingestion_timestamp",
    current_timestamp()
)

# Write records into Delta table
(
    df_stream.writeStream
    .format("delta")
    .option("checkpointLocation", checkpoint_path)
    .trigger(availableNow=True)
    .toTable(target_table)
)
