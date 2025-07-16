{{ config(materialized='view') }}

SELECT * FROM {{ source('nyc', 'dim_weather') }}
