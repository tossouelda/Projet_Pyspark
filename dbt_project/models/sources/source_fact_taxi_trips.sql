-- models/sources/source_fact_taxi_trips.sql
{{ config(materialized='view') }}

SELECT *
FROM {{ source('nyc', 'fact_taxi_trips') }}
