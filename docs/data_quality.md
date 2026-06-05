# Data Quality Results

| Check | Result |
|---|---:|
| Total records | 14,163,317 |
| Null pickup timestamps | 0 |
| Null dropoff timestamps | 0 |
| Negative fares | 0 |
| Invalid trip distances | 0 |
| Invalid trip durations | 0 |
| Duplicate records | 0 |
| Invalid passenger count | 49,962 |

## Notes

Invalid passenger count records were detected but not removed from the Silver layer because the current Gold KPIs are based on trip count, revenue, fare amount, tip amount and trip distance.

Passenger count validation is documented as a known data quality issue and can be addressed in a future refinement depending on business requirements.
