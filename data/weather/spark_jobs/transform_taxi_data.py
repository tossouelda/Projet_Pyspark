
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, unix_timestamp, when, create_map, lit, hour, date_format

def main():
    spark = SparkSession.builder \
        .appName("Transform Yellow Taxi Data") \
        .config("spark.jars", "/opt/airflow/jars/postgresql-42.2.24.jar") \
        .getOrCreate()

    df = spark.read.parquet("/opt/airflow/data/yellow_taxi/yellow_tripdata_2023-01.parquet")

    # Durée du trajet en minutes
    df = df.withColumn(
        "trip_duration_minutes",
        (unix_timestamp("tpep_dropoff_datetime") - unix_timestamp("tpep_pickup_datetime")) / 60
    )

    # Tranches de distance
    df = df.withColumn(
        "distance_bucket",
        when(col("trip_distance") <= 2, "0–2 km")
        .when((col("trip_distance") > 2) & (col("trip_distance") <= 5), "2–5 km")
        .otherwise(">5 km")
    )

    # Mapping type de paiement
    payment_mapping = {
        1: "Credit card", 2: "Cash", 3: "No charge",
        4: "Dispute", 5: "Unknown", 6: "Voided trip"
    }
    mapping_expr = create_map([lit(x) for x in sum(payment_mapping.items(), ())])
    df = df.withColumn("payment_type_label", mapping_expr[col("payment_type")])

    # Pourcentage de pourboire
    df = df.withColumn("tip_percentage", (col("tip_amount") / col("fare_amount")) * 100)

    
    df = df.withColumn("pickup_hour", hour("tpep_pickup_datetime"))
    df = df.withColumn("pickup_day_of_week", date_format("tpep_pickup_datetime", "EEEE"))

    
    df.select(
        "tpep_pickup_datetime", "tpep_dropoff_datetime", "trip_duration_minutes",
        "trip_distance", "distance_bucket", "payment_type", "payment_type_label",
        "tip_amount", "fare_amount", "tip_percentage", "pickup_hour", "pickup_day_of_week"
    ).write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/nyc_dwh") \
        .option("dbtable", "fact_taxi_trips") \
        .option("user", "nyc_user") \
        .option("password", "nyc_pass") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()

    spark.stop()

if __name__ == "__main__":
    main()
