#!/bin/bash

cd /config_app

#Install python requirements
echo 'Install python3 requirements'
pip install -r requirements.txt
# pip install confluent_kafka
# pip install psycopg2-binary
# pip install requests


# Run config and test files

#postgresdb
python3 postgresdb_creator.py
python3 debezium_config.py
sleep 5
python3 postgres_producer.py
sleep 5

python3 database_creator.py

#stagedb
python3 stagedb_creator.py

#finaldb
python3 finaldb_creator.py
python3 finaldb_producer.py


faust -A consumer_faust worker 


# wait for all background processes to finish!
wait