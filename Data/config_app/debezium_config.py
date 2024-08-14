import json

import psycopg2
import requests


def config_debezium_connector():
    """
    Set debezium postgres connector with a curl
    """
    url = "http://connect:8083/connectors/"
    data = {
    "name": "db-connector",
    "config": {
        "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
        "tasks.max": "1",
        "plugin.name": "pgoutput",
        "topic.prefix" : "blu",
        "database.hostname": "db",
        "database.port": "5432",
        "database.user": "postgres",
        "database.password": "comeng2002",
        "database.dbname": "postgres",
        "database.server.name": "db",
        "key.converter": "org.apache.kafka.connect.json.JsonConverter",
        "value.converter": "org.apache.kafka.connect.json.JsonConverter",
        "key.converter.schemas.enable": "false",
        "value.converter.schemas.enable": "false",
        "snapshot.mode": "always"
    }
   }

    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 201:
        print("\nDebezium connector successfully created!\n")
    else:
        print("Debezium Connector Failed!")


config_debezium_connector()
