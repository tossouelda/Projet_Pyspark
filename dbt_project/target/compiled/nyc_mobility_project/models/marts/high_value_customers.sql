

SELECT
    passenger_count,
    COUNT(*) AS total_trips,
    SUM(fare_amount + tip_amount) AS total_spent,
    AVG(tip_percentage) AS avg_tip_percentage
FROM "nyc_dwh"."public"."trip_enriched"
WHERE passenger_count IS NOT NULL AND passenger_count > 0
GROUP BY passenger_count
HAVING COUNT(*) > 10 AND SUM(fare_amount + tip_amount) > 300