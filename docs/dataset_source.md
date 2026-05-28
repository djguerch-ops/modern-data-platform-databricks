# Dataset Source

This project uses official NYC Yellow Taxi Trip Records published by the NYC Taxi & Limousine Commission.

Official source:
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

Dataset format:
- Parquet

Recommended files for this project:
- yellow_tripdata_2024-01.parquet
- yellow_tripdata_2024-02.parquet
- yellow_tripdata_2024-03.parquet

Main fields:
- tpep_pickup_datetime
- tpep_dropoff_datetime
- passenger_count
- trip_distance
- fare_amount
- tip_amount
- total_amount
- payment_type
- PULocationID
- DOLocationID

The raw Parquet files are not committed to this repository due to their size.
They should be downloaded from the official NYC TLC website and stored locally or in cloud storage before running the Databricks notebooks.
