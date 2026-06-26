# Modern Data Platform with Databricks & Delta Lake

[![Azure](https://img.shields.io/badge/Azure-Cloud-0078D4?logo=microsoftazure&logoColor=white)](https://azure.microsoft.com)
[![Databricks](https://img.shields.io/badge/Databricks-Lakehouse-FF3621?logo=databricks&logoColor=white)](https://databricks.com)
[![PySpark](https://img.shields.io/badge/PySpark-BigData-E25A1C?logo=apachespark&logoColor=white)](https://spark.apache.org)
[![Delta Lake](https://img.shields.io/badge/Delta_Lake-ACID-00ADD8)](https://delta.io)
[![Power BI](https://img.shields.io/badge/PowerBI-Analytics-F2C811?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

End-to-end cloud Lakehouse platform built on Azure Databricks, processing **14M+ NYC Taxi records** through a Medallion Architecture with Delta Lake, Unity Catalog, and Auto Loader.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Medallion Architecture](#medallion-architecture)
- [Technology Stack](#technology-stack)
- [Project Scale](#project-scale)
- [Databricks Execution Evidence](#databricks-execution-evidence)
- [Analytics Dashboard](#analytics-dashboard)
- [Advanced Features](#advanced-features)
- [Spark Optimization](#spark-optimization)
- [Business Use Case](#business-use-case)
- [Project Structure](#project-structure)
- [Future Improvements](#future-improvements)
- [Author](#author)

---

## Overview

This project implements a production-grade Lakehouse Data Platform on Azure Databricks.

It ingests real-world **NYC Yellow Taxi trip records** in Parquet format, processes them through Bronze, Silver, and Gold layers using PySpark and Delta Lake, and exposes analytics-ready KPI datasets via a Databricks SQL Dashboard.

The dataset is sourced from the official NYC Taxi & Limousine Commission (TLC) trip records.

---

## Architecture

![Architecture](images/architecture.png)

The platform follows a layered Lakehouse architecture:

- **Ingestion** — Parquet files loaded via Unity Catalog Volumes and Auto Loader
- **Bronze** — Raw data persisted as Delta tables, no transformation
- **Silver** — Cleaned, standardized, and deduplicated data
- **Gold** — Business aggregations and KPIs for analytics
- **Serving** — Databricks SQL Dashboard + Power BI

---

## Medallion Architecture

### Bronze Layer

- Raw ingestion of NYC Taxi Parquet files
- Stored as Delta Lake managed tables in Unity Catalog
- Full historical preservation — no data loss
- Incremental ingestion via Auto Loader (`cloudFiles`)

### Silver Layer

- Data cleansing: null handling, outlier filtering
- Standardization of column types and naming conventions
- Deduplication using PySpark transformations
- Business rules applied for data quality

### Gold Layer

- Business-level aggregations and KPI computation
- Analytics-ready Delta tables optimized for querying
- Powers the Databricks SQL Dashboard and Power BI reports

---

## Technology Stack

| Technology            | Role                                    |
| --------------------- | --------------------------------------- |
| Azure Databricks      | Distributed processing & orchestration  |
| Apache Spark / PySpark| Data transformation at scale            |
| Delta Lake            | ACID transactions & time travel         |
| Unity Catalog         | Data governance, access control & lineage |
| Unity Catalog Volumes | Raw file storage (landing zone)         |
| Auto Loader           | Incremental file ingestion              |
| Databricks SQL        | Interactive querying & dashboards       |
| Power BI              | Reporting & business dashboards         |

---

## Project Scale

| Metric            | Value                  |
| ----------------- | ---------------------- |
| Records processed | 14,163,317             |
| Source format     | Parquet                |
| Storage format    | Delta Lake             |
| Processing engine | Apache Spark           |
| Platform          | Azure Databricks       |
| Governance        | Unity Catalog          |
| Architecture      | Bronze / Silver / Gold |

---

## Databricks Execution Evidence

### Unity Catalog Tables

The full pipeline was executed in Databricks with managed Delta tables registered in Unity Catalog.

![Unity Catalog Tables](images/catalog_tables.png)

Tables created:

| Table               | Layer  | Description                        |
| ------------------- | ------ | ---------------------------------- |
| `nyc_taxi_bronze`   | Bronze | Raw ingested Parquet data          |
| `nyc_taxi_silver`   | Silver | Cleaned and standardized records   |
| `nyc_taxi_kpis`     | Gold   | Business KPIs and aggregations     |

### Gold KPI Table

The Gold layer aggregates over 14 million records into analytics-ready KPI tables.

![Gold KPI Table](images/gold_kpis.png)

---

## Analytics Dashboard

The Gold layer feeds a **Databricks SQL Dashboard** for real-time business analytics and KPI monitoring.

![NYC Taxi Dashboard](images/nyc_taxi_dashboard.png)

Dashboard metrics:

- Total Trips & Total Revenue
- Average Fare Amount
- Average Trip Distance & Tip Amount
- Trips by Hour of Day
- Trips by Payment Method
- Monthly Revenue Trend

---

## Advanced Features

### Auto Loader

The platform includes an Auto Loader ingestion pipeline for incremental file processing from Unity Catalog Volumes.

**Auto Loader configuration used:**

```python
spark.readStream \
  .format("cloudFiles") \
  .option("cloudFiles.format", "parquet") \
  .option("cloudFiles.schemaLocation", schema_path) \
  .load(raw_volume_path) \
  .writeStream \
  .trigger(availableNow=True) \
  .option("checkpointLocation", checkpoint_path) \
  .toTable("catalog.schema.nyc_taxi_bronze")
```

Features enabled:
- `cloudFiles` source format
- Schema inference and evolution
- Checkpointing for fault tolerance
- `availableNow` trigger for micro-batch execution
- Delta table output in Unity Catalog

---

## Spark Optimization

Several Spark optimization techniques were applied across the pipeline:

| Technique                  | Implementation                                      |
| -------------------------- | --------------------------------------------------- |
| Delta Lake Z-Ordering      | `OPTIMIZE table ZORDER BY (pickup_datetime)`        |
| Partition pruning          | Partitioned Silver table by `year` / `month`        |
| Predicate pushdown         | Filters pushed before joins and aggregations        |
| Avoid wide transformations | Minimized shuffles by broadcasting small DataFrames |
| Caching                    | Intermediate Silver DataFrames cached before Gold   |

---

## Business Use Case

The platform simulates a real-world **transportation analytics system** for NYC Yellow Taxi operations.

**Key objectives:**

- Ingest large-scale Parquet trip records at scale
- Preserve raw data in Bronze for auditability
- Clean and standardize trip records in Silver
- Generate Gold-level KPIs for business decision-making
- Analyze revenue, trip volume, distance, tips, and payment behavior

**Sample KPIs generated:**

- Total trips & monthly trends
- Total revenue and average fare
- Average trip distance and tip rate
- Trip distribution by hour of day
- Revenue breakdown by payment type

---

## Project Structure

```
modern-data-platform-databricks/
│
├── architecture/          # Architecture diagrams (draw.io / PNG)
├── datasets/              # Sample datasets or data references
├── docs/                  # Supplementary documentation
├── images/                # Screenshots and dashboard captures
├── notebooks/             # Databricks notebooks (Bronze / Silver / Gold / Auto Loader)
├── .gitignore
├── LICENSE
└── README.md
```

---

## Future Improvements

- [ ] Power BI full dashboard integration (DirectQuery on Gold layer)
- [ ] CI/CD pipeline with GitHub Actions + Databricks Asset Bundles
- [ ] dbt integration for SQL-based transformations on Gold layer
- [ ] Terraform deployment for infrastructure as code (IaC)
- [ ] Real-time streaming pipeline with Databricks Structured Streaming
- [ ] Data quality framework (Great Expectations or Databricks Data Quality)
- [ ] End-to-end monitoring with Databricks Lakehouse Monitoring

---

## Author

**Djamel Guerchouche**  
Senior Data Engineer

Specialized in cloud-native data platforms, distributed processing, and Lakehouse architecture.

- 🔗 [LinkedIn](https://www.linkedin.com/in/djamel-guerchouche-863559b6/)
- 🐙 [GitHub](https://github.com/djguerch-ops)

**Core expertise:**
Azure · Databricks · Apache Spark · Delta Lake · Python · Enterprise Data Platforms

---

*Built with ❤️ using Azure Databricks, PySpark, and Delta Lake.*
