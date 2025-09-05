from airflow import DAG
from airflow.operators.python import PythonOperator
import requests
from datetime import datetime

# Best practice: Define default_args for the DAG to pass integrity tests.
default_args = {
    'owner': 'utility-team', # Passes the 'owner' check
    'retries': 2,            # Passes the 'retries' check
}


def get_external_ip():
    """Gets the external IP using an online service and logs it."""
    try:
        response = requests.get("https://api.ipify.org")  # or another service like "https://ifconfig.me"
        response.raise_for_status()  
        ip = response.text
        print(f"The Airflow worker's external IP is: {ip}")
        return ip
    except requests.exceptions.RequestException as e:
        print(f"Error getting external IP: {e}")
        raise

with DAG(
    dag_id='detect_airflow_external_ip',
    default_args=default_args,
    schedule=None,  # This DAG runs only when triggered manually
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['utility', 'example'],
) as dag:
    get_ip_task = PythonOperator(
        task_id='get_external_ip',
        python_callable=get_external_ip,
    )
