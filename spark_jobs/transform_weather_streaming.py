
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_unixtime, hour, date_format, when
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType

def main():
    spark = SparkSession.builder \
        .appName("Transform Weather Batch Data") \
        .config("spark.jars", "/opt/airflow/jars/postgresql-42.2.24.jar") \
        .getOrCreate()

    schema = StructType([
        StructField("weather", 
            StructType([
                StructField("main", StringType(), True)
            ]), True),
        StructField("main", 
            StructType([
                StructField("temp", DoubleType(), True),
                StructField("humidity", DoubleType(), True)
            ]), True),
        StructField("wind", 
            StructType([
                StructField("speed", DoubleType(), True)
            ]), True),
        StructField("dt", LongType(), True),
        StructField("name", StringType(), True)
    ])

    df_raw = spark.read \
        .schema(schema) \
        .json("/opt/airflow/data/weather/")

    df_transformed = df_raw.select(
        col("name").alias("city"),
        col("main.temp").alias("temperature"),
        col("main.humidity").alias("humidity"),
        col("wind.speed").alias("wind_speed"),
        col("weather.main").alias("weather_condition"),
        from_unixtime(col("dt")).cast("timestamp").alias("event_time")
    )

    df_transformed = df_transformed.withColumn(
        "weather_category",
        when(col("weather_condition").isin("Rain", "Drizzle", "Thunderstorm"), "Pluvieux")
        .when(col("weather_condition").isin("Clear"), "Clair")
        .when(col("weather_condition").isin("Clouds"), "Nuageux")
        .otherwise("Autre")
    )

    df_transformed = df_transformed \
        .withColumn("event_hour", hour("event_time")) \
        .withColumn("event_day_of_week", date_format("event_time", "EEEE"))

    df_transformed.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/nyc_dwh") \
        .option("dbtable", "dim_weather") \
        .option("user", "nyc_user") \
        .option("password", "nyc_pass") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()

    spark.stop()

if __name__ == "__main__":
    main()
