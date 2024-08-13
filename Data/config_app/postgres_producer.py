import psycopg2

# Database connection parameters
db_config = {
    "dbname": "postgres",
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
    query = f"INSERT INTO task.{table_name} ({columns}) VALUES {values};"
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()


def insert_default_data():
    """
    Insert default data into tables
    """
    tables_data = {
        "customer_type": (
            "id, name, description",
            "(1, 'حقیقی', 'کاربر حقیقی'),"
            "(2, 'حقوقی', 'کاربر حقوقی'),"
            "(3, 'کودک', 'کاربران زیر سن قانونی')",
        ),
        "customer": (
            "id, name, birth_date, customer_no, is_active, creation_date, last_modification_date, type",
            "(1, 'john smith', '1997-11-19', '354845', TRUE, '2021-05-07 21:15:42', '2022-09-06 21:16:03', 1),"
            "(2, 'ali mohammadi', '1981-05-07', 354822, TRUE, '2021-10-29 12:22:44', '2023-11-02 13:56:02', 1),"
            "(3, 'abbas alavi', '2000-11-09', 353412, TRUE, '2022-12-05 21:19:30', '2023-01-05 21:19:42', 1)",
        ),
        "account_types": (
            "id, name, description",
            "(1, 'سپرده کوتاه مدت', 'سپرده پس انداز کوتاه مدت'),"
            "(2, 'سپرده بلند مدت', 'سپرده پس انداز بلند مدت'),"
            "(3, 'قرض الحسنه', 'حساب پس انداز قرض الحسنه')",
        ),
        "account": (
            "id, client_id, type, account_no, is_active, creation_date, last_modification_date",
            "(1, 1, 1, 10022, TRUE, '2021-07-08 21:23:06', '2022-09-02 21:23:16'),"
            "(2, 1, 3, 10032, TRUE, '2020-02-26 14:24:02', '2022-03-01 11:24:14'),"
            "(3, 2, 1, 20021, TRUE, '2022-03-18 23:24:56', '2023-01-07 02:25:06')",
        ),
        "transaction_type": (
            "id, name, description",
            "(1, 'کارت به کارت', 'انتقال وجه کارت به کارت'),"
            "(2, 'پایا', 'انتقال وجه پایا'),"
            "(3, 'ساتنا', 'انتقال وجه ساتنا')",
        ),
        "transaction": (
            "id, amount, transaction_date, type, from_account_id, to_account_id, credit",
            "(1, 30000, '2023-12-14 12:29:54', 1, 1, 3, FALSE),"
            "(2, 60500000, '2023-12-15 13:30:46', 1, 3, 1, TRUE),"
            "(3, 520000000, '2023-12-12 22:31:27', 2, 2, 3, TRUE),"
            "(4, 640000000, '2023-12-13 14:43:27', 1, 1, 2, TRUE)",
        ),
    }

    for table_name, (columns, values) in tables_data.items():
        insert_data(table_name, columns, values)


insert_default_data()
print("postgredb - Data produced successfully.\n")
