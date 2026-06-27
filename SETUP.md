# Setup Guide — Modern Data Platform with Databricks & Delta Lake

This guide walks you through every step to reproduce this project from scratch, from creating your AWS Databricks workspace to running the full pipeline and connecting Power BI.

---

## Prerequisites

Before starting, make sure you have:

- An **AWS account** (free tier works for initial setup)
- A **Databricks account** — sign up at https://www.databricks.com
- **Power BI Desktop** installed on your PC — download at https://powerbi.microsoft.com/desktop
- **Python 3.8+** installed (optional, for local testing)

---

## Step 1 — Create your AWS Databricks Workspace

1. Go to **https://accounts.cloud.databricks.com**
2. Sign in or create a Databricks account
3. Click **Create workspace**
4. Select **AWS** as your cloud provider
5. Fill in:
   - **Workspace name**: `nyc-taxi-platform` (or any name)
   - **AWS Region**: choose the closest to you (e.g. `us-east-1`)
6. Click **Start quickstart** — Databricks will automatically provision the workspace on AWS
7. Wait 5-10 minutes for the workspace to be ready
8. Click **Open workspace** to access your Databricks environment

> **Note**: Databricks on AWS requires linking your AWS account. Follow the on-screen instructions to create the necessary IAM roles automatically via CloudFormation.

---

## Step 2 — Create a Cluster

Once inside your workspace:

1. Click **Compute** in the left menu
2. Click **Create compute**
3. Configure your cluster:
   - **Policy**: Unrestricted
   - **Single node** (sufficient for this project)
   - **Databricks Runtime**: 13.0 LTS or higher (includes Spark 3.4 + Delta Lake)
   - **Node type**: `i3.xlarge` (recommended for cost efficiency on AWS)
4. Click **Create compute**
5. Wait 3-5 minutes for the cluster to start (status turns green)

---

## Step 3 — Enable Unity Catalog (if not already enabled)

Unity Catalog is usually enabled by default on new Databricks workspaces. To verify:

1. Click **Catalog** in the left menu
2. If you see a catalog tree with `main`, `system`, etc. → Unity Catalog is enabled ✅
3. If not, go to **Account Console** → **Data** → **Unity Catalog** and follow the setup wizard

---

## Step 4 — Create the Unity Catalog Structure

In your Databricks workspace, open a new notebook and run the following SQL commands:

```sql
-- Create the catalog
CREATE CATALOG IF NOT EXISTS nyc_taxi;

-- Create the schema
CREATE SCHEMA IF NOT EXISTS nyc_taxi.taxi;

-- Create the volume (for raw file storage)
CREATE VOLUME IF NOT EXISTS nyc_taxi.taxi.nyc_taxi_data;
```

To run SQL in a notebook:
1. Click **New** → **Notebook**
2. Change the language to **SQL** (top left dropdown)
3. Paste and run each command

After running, you should see in the Catalog panel:
```
nyc_taxi/
└── taxi/
    └── Volumes/
        └── nyc_taxi_data/   ← your landing zone
```

---

## Step 5 — Download the NYC Taxi Dataset

1. Go to the official NYC TLC website:
   👉 **https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page**

2. Scroll down to **Yellow Taxi Trip Records**

3. Download the following monthly Parquet files:
   - `yellow_tripdata_2026-01.parquet` (January 2026)
   - `yellow_tripdata_2026-02.parquet` (February 2026)
   - `yellow_tripdata_2026-03.parquet` (March 2026)
   - `yellow_tripdata_2026-04.parquet` (April 2026)

> These 4 files total approximately **244 MB** and contain **14.9 million trip records**.

---

## Step 6 — Upload Data to the Unity Catalog Volume

1. In your Databricks workspace, click **Catalog** in the left menu
2. Navigate to **nyc_taxi** → **taxi** → **Volumes** → **nyc_taxi_data**
3. Click **Upload to this volume**
4. Drag and drop your 4 Parquet files
5. Wait for the upload to complete

To verify the upload, run in a notebook:
```python
dbutils.fs.ls("/Volumes/nyc_taxi/taxi/nyc_taxi_data/")
```

You should see:
```
yellow_tripdata_2026-01.parquet   61.19 MB
yellow_tripdata_2026-02.parquet   55.96 MB
yellow_tripdata_2026-03.parquet   64.75 MB
yellow_tripdata_2026-04.parquet   61.82 MB
```

---

## Step 7 — Clone the Repository into Databricks

1. In your workspace, click **Workspace** in the left menu
2. Click **Repos** → **Add Repo**
3. Enter the repository URL:
   ```
   https://github.com/djguerch-ops/modern-data-platform-databricks
   ```
4. Click **Create Repo**

The repo will appear under **Workspace → Repos → your-email → modern-data-platform-databricks**

---

## Step 8 — Run the Notebooks in Order

Open the `Notebooks/` folder in the cloned repo and run each notebook **in this exact order**:

### Notebook 1 — Bronze Ingestion

**File**: `01_bronze_nyc_taxi_ingestion.py`

1. Open the notebook
2. Attach it to your cluster (top right dropdown)
3. Click **Run all**

Expected output:
```
Reading Parquet files from: /Volumes/nyc_taxi/taxi/nyc_taxi_data/*.parquet
Raw records read: 14,908,446
Writing Bronze Delta table: nyc_taxi.taxi.nyc_taxi_bronze
Bronze ingestion completed successfully.
Total records in Bronze table: 14,908,446
Table location: nyc_taxi.taxi.nyc_taxi_bronze
```

### Notebook 2 — Silver Transformations

**File**: `silver_nyc_taxi_transformations.py`

1. Open the notebook
2. Attach it to your cluster
3. Click **Run all**

Expected output:
```
Reading Bronze table: nyc_taxi.taxi.nyc_taxi_bronze
Bronze records: 14,908,446
Silver transformation completed successfully.
Bronze records  : 14,908,446
Silver records  : 10,771,325
Rejected records: 4,137,121 (27.8%)
Table location  : nyc_taxi.taxi.nyc_taxi_silver
```

### Notebook 3 — Gold KPIs

**File**: `gold_nyc_taxi_kpis.py`

1. Open the notebook
2. Attach it to your cluster
3. Click **Run all**

Expected output:
```
Reading Silver table: nyc_taxi.taxi.nyc_taxi_silver
Silver records: 10,771,325
Gold KPI table created successfully.
Total KPI rows  : 2,689
Table location  : nyc_taxi.taxi.nyc_taxi_kpis
```

---

## Step 9 — Connect Power BI (Optional)

### 9.1 Get your Connection Details

1. In Databricks, click **SQL Warehouses** in the left menu
2. Click on your warehouse (e.g. `Serverless Starter Warehouse`)
3. Click the **Connection details** tab
4. Copy:
   - **Server hostname** (e.g. `dbc-xxxxxxxx-xxxx.cloud.databricks.com`)
   - **HTTP Path** (e.g. `/sql/1.0/warehouses/xxxxxxxxx`)

### 9.2 Generate a Personal Access Token

1. Click your profile icon (top right) → **Settings**
2. Go to **Developer** → **Access tokens**
3. Click **Generate new token**
4. Name it `powerbi-connection` and click **Generate**
5. **Copy the token immediately** — it won't be shown again

### 9.3 Connect Power BI Desktop

1. Open **Power BI Desktop**
2. Click **Get Data** → search for **Databricks**
3. Select **Databricks** → click **Connect**
4. Fill in:
   - **Server hostname**: paste your hostname
   - **HTTP Path**: paste your HTTP path
   - **Data Connectivity mode**: **DirectQuery**
5. Click **OK**
6. For authentication: choose **Token** → paste your Personal Access Token
7. Click **Connect**

### 9.4 Load the Gold Table

1. In the Navigator, expand **nyc_taxi** → **taxi**
2. Check **nyc_taxi_kpis**
3. Click **Load**

### 9.5 Build the Dashboard

Create the following visuals:

| Visual | Type | X-axis / Legend | Y-axis / Values |
|--------|------|-----------------|-----------------|
| Total Trips | Card | — | `total_trips` (Sum) |
| Total Revenue | Card | — | `total_revenue` (Sum) |
| Avg Fare | Card | — | `avg_fare_amount` (Average) |
| Trips by Month | Bar Chart | `pickup_month` | `total_trips` (Sum) |
| Trips by Hour | Line Chart | `pickup_hour` | `total_trips` (Sum) |
| Revenue by Payment | Pie Chart | `payment_type` | `total_revenue` (Sum) |

---

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `Path not found` | Wrong volume path | Check `/Volumes/nyc_taxi/taxi/nyc_taxi_data/` exists |
| `UC_COMMAND_NOT_SUPPORTED` | Using `input_file_name()` with Unity Catalog | Use `col("_metadata.file_path")` instead |
| `Table not found` | Wrong catalog/schema | Run `USE CATALOG nyc_taxi; USE SCHEMA taxi;` first |
| Power BI connection fails | Wrong token or hostname | Regenerate token and double-check hostname |
| Aberrant years in Gold | Bad data in source | Silver filter `year == 2026` must be applied |

---

## Delta Tables Summary

After running all notebooks, you will have 3 managed Delta tables in Unity Catalog:

| Table | Layer | Records | Description |
|-------|-------|---------|-------------|
| `nyc_taxi.taxi.nyc_taxi_bronze` | Bronze | 14,908,446 | Raw ingested data |
| `nyc_taxi.taxi.nyc_taxi_silver` | Silver | 10,771,325 | Cleaned & enriched data |
| `nyc_taxi.taxi.nyc_taxi_kpis` | Gold | 2,689 | Business KPI aggregations |

---

*For questions or issues, feel free to open a GitHub issue or reach out on [LinkedIn](https://www.linkedin.com/in/djamel-guerchouche-863559b6/).*
