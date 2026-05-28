# Pipeline Execution

This project follows a Medallion Architecture approach using Bronze, Silver and Gold Delta Lake layers.

---

# Execution Flow

```text
Raw Parquet Files
        ↓
Bronze Layer
        ↓
Silver Layer
        ↓
Gold Layer
        ↓
Analytics / Power BI
```

---

# 1. Bronze Layer

Notebook: `notebooks/bronze_nyc_taxi_ingestion.py`

## Purpose

The Bronze layer ingests raw NYC Yellow Taxi trip records from Parquet files and stores them in Delta Lake format.

## Main Processing

* Read multiple Parquet files
* Preserve raw source columns
* Add ingestion metadata
* Store raw records in Delta Lake

## Input

Raw NYC Taxi Parquet files.

Example:

```text
datasets/nyc_taxi/yellow_tripdata_2024-01.parquet
datasets/nyc_taxi/yellow_tripdata_2024-02.parquet
datasets/nyc_taxi/yellow_tripdata_2024-03.parquet
```

## Output

output/bronze/nyc_taxi_bronze
---

# 2. Silver Layer

Notebook: `notebooks/silver_nyc_taxi_transformations.py`

## Purpose

The Silver layer cleans and standardizes taxi trip records from the Bronze layer.

## Main Processing

* Filter invalid trips
* Remove inconsistent values
* Convert timestamps
* Remove duplicate rows
* Standardize records

## Input

output/bronze/nyc_taxi_bronze


## Output
output/silver/nyc_taxi_silver
---

# 3. Gold Layer

Notebook: `notebooks/gold_nyc_taxi_kpis.py`

## Purpose

The Gold layer generates business KPI tables optimized for analytics and reporting.

## Main Processing

* Aggregate trip statistics
* Calculate revenue metrics
* Generate hourly analytics
* Generate payment type analytics
* Create reporting-ready datasets

## Input
output/silver/nyc_taxi_silver

## Output
output/gold/nyc_taxi_kpis

