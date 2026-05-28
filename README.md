# Modern Data Platform with Azure Databricks

![Azure](https://img.shields.io/badge/Azure-Cloud-blue)
![Databricks](https://img.shields.io/badge/Databricks-Lakehouse-red)
![PySpark](https://img.shields.io/badge/PySpark-BigData-orange)
![Delta Lake](https://img.shields.io/badge/Delta-Lake-green)
![Power BI](https://img.shields.io/badge/PowerBI-Analytics-yellow)

---

# Project Overview

This project demonstrates the implementation of a modern cloud data platform using:

- Azure Databricks
- Apache Spark (PySpark)
- Delta Lake
- Azure Data Lake Storage
- Medallion Architecture
- Power BI

The platform ingests raw business data, processes and transforms it through Bronze, Silver, and Gold layers, and exposes business KPIs through analytical dashboards.

---

# Architecture

![Architecture](images/architecture.png)

---

# Medallion Architecture

## Bronze Layer
- Raw data ingestion
- Delta Lake storage
- Historical raw data preservation

## Silver Layer
- Data cleansing
- Standardization
- Deduplication
- PySpark transformations

## Gold Layer
- Business aggregations
- KPI generation
- Analytics-ready tables

---

# Technology Stack

| Technology | Purpose |
|---|---|
| Azure Data Lake Storage | Raw data storage |
| Azure Databricks | Distributed processing |
| PySpark | Data transformation |
| Delta Lake | ACID transactions & optimization |
| Power BI | Reporting & dashboards |

---

# Business Use Case

The project simulates a modern enterprise data platform for sales analytics.

Main objectives:
- Ingest raw sales datasets
- Clean and standardize customer data
- Generate business KPIs
- Provide analytics-ready datasets for reporting

---

# Features

- Incremental data ingestion
- Delta Lake tables
- Medallion Architecture
- PySpark transformations
- Business KPI generation
- Data quality checks
- Scalable cloud architecture

---

# Project Structure

```text
modern-data-platform-databricks/
│
├── architecture/
├── datasets/
├── docs/
├── images/
├── notebooks/
├── README.md
└── requirements.txt
```

---

# Sample KPIs

Examples of generated KPIs:
- Monthly sales revenue
- Top customers
- Product performance
- Sales trends
- Regional analytics

---

# Spark Optimization

This project includes several Spark optimization techniques:

- Partitioning
- Delta Lake optimization
- Efficient transformations
- Optimized joins
- Scalable processing patterns

---

# Future Improvements

- CI/CD integration
- dbt integration
- Streaming ingestion
- Terraform deployment
- Real-time analytics
- Azure Data Factory orchestration

---

# Screenshots

Future project screenshots will include:
- Databricks notebooks
- Delta tables
- Spark jobs
- Power BI dashboards

---

# Author

Djamel Guerchouche

Senior Data Engineer specialized in:
- Azure
- Databricks
- Apache Spark
- Delta Lake
- Enterprise Data Platform Modernization

