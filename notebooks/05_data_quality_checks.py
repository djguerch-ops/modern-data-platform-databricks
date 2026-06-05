# Read Silver table
df_silver = spark.table(
    "workspace_7474648309056393.default.nyc_taxi_silver"
)

# Total records
print(f"Total records: {df_silver.count()}")

# Null checks
print(
    "Null pickup timestamps:",
    df_silver.filter(
        col("pickup_timestamp").isNull()
    ).count()
)

print(
    "Null dropoff timestamps:",
    df_silver.filter(
        col("dropoff_timestamp").isNull()
    ).count()
)

# Negative fare checks
print(
    "Negative fares:",
    df_silver.filter(
        col("fare_amount") < 0
    ).count()
)

# Invalid trip distance
print(
    "Invalid distances:",
    df_silver.filter(
        col("trip_distance") <= 0
    ).count()
)
