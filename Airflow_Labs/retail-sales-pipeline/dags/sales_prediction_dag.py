from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

from src.data_loader import load_data
from src.eda_analyzer import perform_eda
from src.preprocessor import preprocess_data
from src.model_trainer import train_models

default_args = {
    'owner': 'ds_team',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'retail_sales_prediction',
    default_args=default_args,
    description='ML pipeline for retail sales prediction',
    schedule_interval='@daily',
    catchup=False
)

load_data_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag
)

eda_task = PythonOperator(
    task_id='exploratory_data_analysis',
    python_callable=perform_eda,
    op_args=[load_data_task.output],
    dag=dag
)

preprocess_task = PythonOperator(
    task_id='preprocess_data',
    python_callable=preprocess_data,
    op_args=[load_data_task.output],
    dag=dag
)

train_models_task = PythonOperator(
    task_id='train_models',
    python_callable=train_models,
    op_args=[preprocess_task.output, "model.sav"],
    dag=dag
)

load_data_task >> [eda_task, preprocess_task]
preprocess_task >> train_models_task 
