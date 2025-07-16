
  
    

  create  table "nyc_dwh"."public"."trip_enriched__dbt_tmp"
  
  
    as
  
  (
    

SELECT
    t.passenger_count,
    t.trip_distance,
    t.tpep_pickup_datetime,
    t.tpep_dropoff_datetime,
    t.payment_type,
    t.fare_amount,
    t.tip_amount,
    t.tip_percentage,
    t.distance_bucket,
    t.pickup_hour,
    t.pickup_day_of_week,
    w.weather_category,
    w.temperature,
    w.humidity,
    w.wind_speed
FROM "nyc_dwh"."public"."source_fact_taxi_trips" t
LEFT JOIN "nyc_dwh"."public"."source_dim_weather" w
    ON date_trunc('hour', t.tpep_pickup_datetime) = date_trunc('hour', w.event_time)
  );
  