import os
from datetime import datetime

from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryExecuteQueryOperator,
)

# Best practice: Define default_args for the DAG to pass integrity tests.
default_args = {
    "owner": "data-team",  # Passes the 'owner' check
    "retries": 1,  # Passes the 'retries' check
}

with DAG(
    dag_id="example_bigquery_query",
    default_args=default_args,
    schedule=None,
    start_date=datetime(2025, 8, 21),
    catchup=False,
    tags=["example", "gcp", "bigquery"],
) as dag:
    # This task runs a query against a public BigQuery dataset.
    # The query is small and filtered, making it fast and free to run.
    run_example_query = BigQueryExecuteQueryOperator(
        task_id="run_example_query",
        sql="""
        SELECT name, number
        FROM `bigquery-public-data.usa_names.usa_1910_current`
        WHERE name = 'David'
        LIMIT 10;
        """,
        use_legacy_sql=False,
        location="US",
        gcp_conn_id="bigquery_default",
    )