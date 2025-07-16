from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
}

dag = DAG(
    'yellow_taxi_pipeline',
    default_args=default_args,
    description='Pipeline taxi + météo + dbt (centralisé)',
    schedule_interval='@daily',
    catchup=False,
)

download_taxi_data = BashOperator(
    task_id='download_taxi_data',
    bash_command='python3 /opt/airflow/scripts/download_taxi_data.py',
    dag=dag,
)

# Étape 2: Transformer les données taxi avec Spark
transform_taxi_data = BashOperator(
    task_id='transform_taxi_data',
    bash_command='spark-submit --jars /opt/airflow/jars/postgresql-42.2.24.jar /opt/airflow/spark_jobs/transform_taxi_data.py',
    dag=dag,
)

# Étape 3: Transformer les données météo (streaming ou batché par fichier horaire)
transform_weather_data = BashOperator(
    task_id='transform_weather_data',
    bash_command='spark-submit --jars /opt/airflow/jars/postgresql-42.2.24.jar /opt/airflow/spark_jobs/transform_weather_streaming.py',
    dag=dag,
)

# Étape 4: Exécuter dbt une fois les données préparées
run_dbt_models = BashOperator(
    task_id='run_dbt_models',
    bash_command='cd /opt/airflow/dbt_project && dbt run --select trip_enriched trip_summary_per_hour high_value_customers source_dim_weather',
    dag=dag,
)

download_taxi_data >> transform_taxi_data
[transform_taxi_data, transform_weather_data] >> run_dbt_models
