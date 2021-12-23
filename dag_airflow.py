# Dag is a directed  acyclic Graph, is a representation of a series of event
# each dag represents a collections of task you want to run organized in a way that reflects  dependecis and relationship
# each node represent 1 task/code


from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

from data_scrapping_2 import run_bbc_etl

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021, 23, 12),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'bbc_dag',
    default_args=default_args,
    description='Our first DAG with ETL process!',
    # how often do we want our program to run in this case daily
    schedule_interval=timedelta(days=1),
)

def just_a_function():
    print("I'm going to show you something :)")


# Operators

# operators determine what actually get done by a task
# one operator = one task, in my case i will use python operator, operater are atomics
# standalone, that means that you cannot pass the data from one operator to another, airfloww have a feature called cross comunications   Xcom
run_etl = PythonOperator(
    task_id='whole_BBC_etl',
    python_callable=data_scrapping_2,
    dag=dag,
)


# We define the order of execution of  the taks by simpling putting  the names at the bottom of the file
# if we have more task t1 >> [t2, t3]
run_etl

#  if the airflow is running the data will get automatically donwloaded and saved to your database



