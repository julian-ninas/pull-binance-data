from airflow import DAG
import datetime
import os
from airflow.operators.python import PythonOperator
from dotenv import load_dotenv
from airflow.providers.postgres.operators.postgres import PostgresOperator
from scripts.extract_crypto_data_script import load_to_postgres
from scripts.create_crypto_table import create_table_query

load_dotenv('../.env')

date_cur =  datetime.datetime(2023, 6, 7)

default_arg = {
                'owner': 'airflow',
                'start_date': date_cur, 
}

dag = DAG('crypto_etl', default_args =default_arg , schedule="*/5 * * * *", catchup=False) 


# create_table = PostgresOperator(
#     sql = create_table_query,
#     task_id = "create_table_task",
#     postgres_conn_id =  os.getenv('CON_STRING'),
#     dag = dag
#     )

extract_load = PythonOperator(
    task_id = 'extract_load_postgres', 
    python_callable=load_to_postgres,
    dag=dag
)