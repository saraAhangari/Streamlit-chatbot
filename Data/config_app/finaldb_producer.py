import psycopg2

# Database connection parameters
db_config = {
    "dbname": "finaldb",
    "user": "postgres",
    "password": "comeng2002",
    "host": "db",
    "port": "5432",
}


def connect_db():
    """
    Connect to database
    """
    return psycopg2.connect(**db_config)


def insert_data(table_name, columns, values):
    """
    Generic function to insert data into a table
    """
    conn = connect_db()
    cursor = conn.cursor()
    query = f"INSERT INTO facts.{table_name} ({columns}) VALUES {values};"
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()


def insert_default_data():
    """
    Insert default data into tables
    """
    tables_data = {
        "TRANSACTION_FACT": (
            "id, amount, transaction_date, account_number, customer_name, destination_account_number, destination_customer_name, destination_account_type_name, credit, is_juridical",
            "(1, 1000, '2023-01-01', '10022', 'John Doe', '987654321', 'Jane Doe', 'حقیقی', true, false),"
            "(2, 1500, '2023-01-02', '10024', 'Jane Doe', '123456789', 'John Doe', 'حقوقی', false, true),"
            "(3, 500, '2023-01-03', '10026', 'John Doe', '555555555', 'Child User', 'کودک', false, false)",
        ),
        "TURNOVER_PER_ACCOUNT_TYPE": (
            "ACCOUNT_TYPE_NAME, TURNOVER, TRANSACTION_DATE",
            "('B2B', '540000', '2023-01-01'),"
            "('B2B', '650000', '2023-01-01'),"
            "('B2B', '483300','2023-01-01')",
        ),
        "ACCOUNT_TURNOVER": (
            "CUSTOMER_NAME, ACCOUNT_NO, TURNOVER, TRANSACTION_DATE",
            "('ali mohamadi', '10022', '540000','2023-01-01')",
        ),
    }

    for table_name, (columns, values) in tables_data.items():
        insert_data(table_name, columns, values)


insert_default_data()
print("finaldb - Data produced successfully.\n")
