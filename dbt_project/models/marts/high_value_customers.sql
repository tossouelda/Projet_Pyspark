{{ config(materialized='table') }}

WITH trips AS (
    SELECT
        passenger_count,
        fare_amount,
        tip_amount
    FROM {{ ref('trip_enriched') }}
    WHERE passenger_count IS NOT NULL AND passenger_count > 0
),

agg AS (
    SELECT
        passenger_count,
        COUNT(*) AS total_trips,
        SUM(fare_amount + tip_amount) AS total_spent,
        AVG(tip_amount) AS avg_tip
    FROM trips
    GROUP BY passenger_count
)

SELECT *
FROM agg
WHERE total_trips > 10 AND total_spent > 300
