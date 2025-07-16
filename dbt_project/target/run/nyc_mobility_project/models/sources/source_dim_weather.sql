
  create view "nyc_dwh"."public"."source_dim_weather__dbt_tmp"
    
    
  as (
    

SELECT * FROM "nyc_dwh"."public"."dim_weather"
  );