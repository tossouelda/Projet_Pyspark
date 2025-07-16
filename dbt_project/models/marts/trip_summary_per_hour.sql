{{ config(materialized='table') }}

SELECT
    date_trunc('hour', tpep_pickup_datetime) AS hour,
    weather_category,
    COUNT(*) AS trip_count,
    AVG(trip_duration_minutes) AS avg_duration,
    AVG(tip_percentage) AS avg_tip
FROM {{ ref('trip_enriched') }}
GROUP BY hour, weather_category
