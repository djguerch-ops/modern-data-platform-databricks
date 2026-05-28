# Bronze Layer

The Bronze layer stores raw NYC Yellow Taxi trip records ingested from Parquet files.

## Objectives

- Preserve raw source data
- Store ingestion metadata
- Enable historical replay
- Build the foundation for Silver transformations

## Input

NYC Yellow Taxi trip records in Parquet format.

Example expected files:

```text
yellow_tripdata_2024-01.parquet
yellow_tripdata_2024-02.parquet
yellow_tripdata_2024-03.parquet
