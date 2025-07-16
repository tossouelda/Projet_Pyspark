
{{ config(materialized='view') }}

SELECT *
FROM {{ source('nyc', 'fact_taxi_trips') }}
