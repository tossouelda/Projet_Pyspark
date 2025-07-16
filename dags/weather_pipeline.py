from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
}

dag = DAG(
    'weather_pipeline',
    default_args=default_args,
    description='Pipeline météo : ingestion + Spark Streaming',
    schedule_interval='@hourly',
    catchup=False,
)

download_weather = BashOperator(
    task_id='download_weather_data',
    bash_command='python3 /opt/airflow/scripts/download_weather_data.py',
    dag=dag,
)

start_weather_streaming = BashOperator(
    task_id='start_weather_streaming',
    bash_command=(
        'spark-submit '
        '--jars /opt/airflow/jars/postgresql-42.2.24.jar '
        '/opt/airflow/spark_jobs/transform_weather_streaming.py'
    ),
    dag=dag,
)


download_weather >> start_weather_streaming
