from datetime import datetime, timedelta

import psycopg2
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

postgres_conn_config = {
    "user": "postgres",
    "password": "comeng2002",
    "host": "db",
    "port": "5432",
    "database": "stagedb",
}

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def update_transaction_fact():
    connection = psycopg2.connect(**postgres_conn_config)
    cursor = connection.cursor()

    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)

    try:
        # Fetch records from the all_transactions table in the staging schema
        cursor.execute(
            """
            SELECT
            id, amount, transaction_date, account_number, customer_name,
            destination_account_number, destination_customer_name, destination_account_type_name,
            credit, is_juridical
            FROM
                staging.all_transactions
            WHERE
                transaction_date >= %s AND transaction_date < %s
        """,
            (start_date, end_date),
        )

        records = cursor.fetchall()
        cursor.close()
        connection.close()

        # Update transaction_fact table in the facts schema
        DB_NAME = "finaldb"
        DB_USER = "postgres"
        DB_PASSWORD = "comeng2002"
        DB_HOST = "db"
        DB_PORT = "5432"

        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        cursor = connection.cursor()

        for record in records:
            cursor.execute(
                """
                UPDATE facts.transaction_fact
                SET
                    amount = %s,
                    transaction_date = %s,
                    account_number = %s,
                    customer_name = %s,
                    destination_account_number = %s,
                    destination_customer_name = %s,
                    destination_account_type_name = %s,
                    credit = %s,
                    is_juridical = %s
                WHERE
                    id = %s
            """,
                (
                    record[1],
                    record[2],
                    record[3],
                    record[4],
                    record[5],
                    record[6],
                    record[7],
                    record[8],
                    record[9],
                    record[0],
                ),
            )

        connection.commit()

    except Exception as e:
        print(f"Error fetching records: {e}")

    finally:
        cursor.close()
        connection.close()


with DAG(
    dag_id="daily_transaction_fact",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    (
        PythonOperator(
            task_id="update_transaction_fact",
            python_callable=update_transaction_fact,
        )
    )
