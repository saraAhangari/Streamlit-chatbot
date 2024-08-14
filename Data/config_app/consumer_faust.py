import faust
import asyncpg
from datetime import datetime
import pytz

app = faust.App("faust_streaming", broker="kafka://kafka:9092")

db_config = {
    "database": "stagedb",
    "user": "postgres",
    "password": "comeng2002",
    "host": "db",
    "port": "5432",
}


class Event(faust.Record):
    before: dict
    after: dict
    op: str
    source: dict


async def run_query(query, read: bool, conn=None):
    conn = await asyncpg.connect(**db_config)
    if read:
        row = await conn.fetchrow(query)
        return row
    else:
        insert = await conn.execute(query)
        return insert


async def create_postgres_record(event: Event) -> dict:
    # id, amount, transaction_date
    record = {
        "id": event.after["id"],
        "amount": event.after["amount"],
    }

    # type_name
    transaction_type_id = event.after["type"]
    type_name_query = (
        f"SELECT name FROM staging.transaction_type WHERE id={transaction_type_id}"
    )
    type_name = (await run_query(type_name_query, True))["name"]
    record["type_name"] = type_name

    des_account_id = event.after["to_account_id"]
    des_account_query = f"select account_no, client_id, type from staging.account where id={des_account_id}"
    des_account = await run_query(des_account_query, True)

    account_id = event.after["from_account_id"]
    account_query = (
        f"select account_no, client_id, type from staging.account where id={account_id}"
    )
    account = await run_query(account_query, True)

    # transaction_date
    transaction_date_query = f"SELECT * FROM staging.transaction WHERE from_account_id={account_id} AND to_account_id={des_account_id}"
    transaction_date = (await run_query(transaction_date_query, True))[
        "transaction_date"
    ]
    record["transaction_date"] = transaction_date
    print(record["transaction_date"])

    # account_number
    accountNumber_query = f"SELECT * FROM staging.account WHERE id={account_id}"
    account_no = (await run_query(accountNumber_query, True))["account_no"]
    record["account_number"] = account_no

    # customer_name
    customer_name_query = (
        f"select name, type from staging.customer where id={account['client_id']}"
    )
    customer_name = (await run_query(customer_name_query, True))["name"]
    record["customer_name"] = customer_name

    # destination_account_number
    des_accountNumber_query = f"SELECT * FROM staging.account WHERE id={des_account_id}"
    destination_account_number = (await run_query(des_accountNumber_query, True))[
        "account_no"
    ]
    record["destination_account_number"] = destination_account_number

    # destination_customer_name
    des_customer_name_query = (
        f"select name, type from staging.customer where id={des_account['client_id']}"
    )
    destination_customer_name = (await run_query(des_customer_name_query, True))["name"]
    record["destination_customer_name"] = destination_customer_name

    # destination_account_type_name
    des_account_type_query = (
        f"select name from staging.account_types where id={des_account['type']}"
    )
    destination_account_type_name = (await run_query(des_account_type_query, True))[
        "name"
    ]
    record["destination_account_type_name"] = destination_account_type_name

    # credit
    record["credit"] = event.after["credit"]

    # isJuridical
    customer_type = (await run_query(customer_name_query, True))["type"]
    if customer_type == 2:
        record["is_Juridical"] = True
    else:
        record["is_Juridical"] = False

    return record


async def insert_postgres(record: dict):
    conn = await asyncpg.connect(**db_config)
    id = record["id"]
    amount = record["amount"]
    td = record["transaction_date"]
    tn = record["type_name"]
    an = record["account_number"]
    cn = record["customer_name"]
    dan = record["destination_account_number"]
    dcn = record["destination_customer_name"]
    datn = record["destination_account_type_name"]
    credit = record["credit"]
    ij = record["is_Juridical"]
    query = f"INSERT INTO staging.all_transactions (id, amount, transaction_date, type_name, account_number,\
            customer_name, destination_account_number, destination_customer_name,\
            destination_account_type_name, credit, is_juridical) values( {id} , {amount} , '{td}'::timestamp without time zone,'{tn}',{an} ,'{cn}' ,{dan}, '{dcn}','{datn}',{credit},{ij})"

    await conn.execute(query)
    conn.close()


blu_task_account_topic = app.topic("blu.task.transaction", value_type=Event)


@app.agent(blu_task_account_topic)
async def mytask(stream):
    async for event in stream:
        # events captured in snapshot
        if (event.op == "r" and event.source["snapshot"] != "false") or (
            event.op == "c"
        ):
            record = await create_postgres_record(event)
            await insert_postgres(record)


if __name__ == "__main__":
    app.main()
