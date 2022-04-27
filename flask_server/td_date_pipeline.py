from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

default_args = {
    "start_date": datetime(2022, 1, 1)
}

with DAG(dag_id="today-dating-date-pipeline",
         schedule_interval='* * * * *',
         default_args=default_args,
         tags=["python"],
         catchup=True) as dag:

    # upload_s3
    upload_s3 = BashOperator(
        task_id="upload_s3",
        bash_command="python3 flask_server/upload_s3.py"
    )

    # upload_s3
    transform_rds = BashOperator(
        task_id="transform_rds",
        bash_command="python3 flask_server/transform_rds.py"
    )

    upload_s3 >> transform_rds