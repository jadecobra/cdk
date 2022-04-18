import boto3
import pymysql
import os
import json
import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)

secrets_manager = boto3.client('secretsmanager')

def response(status=200, body=None):
    return {
        'statusCode': status,
        'headers': {"Content-Type": "text/html"},
        'body': json.dumps(body) if isinstance(body, dict) else body
    }

def execute_sql(connection=None, query=None):
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()
    connection.commit()

def get_username_and_password(rds_secret_name):
    print(f'Getting secret for {rds_secret_name}')
    secret = secrets_manager.get_secret_value(
        SecretId=rds_secret_name
    )
    return secret.get('SecretString')

def create_connection(username=None, password=None):
    try:
        return pymysql.connect(
            host=os.environ['PROXY_ENDPOINT'],
            user=username,
            passwd=password,
        )
    except pymysql.MySQLError as error:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(error)
        sys.exit()

def setup_database(connection=None, event=None):
    for query in (
        'CREATE DATABASE IF NOT EXISTS cdkpatterns',
        'CREATE TABLE IF NOT EXISTS rds_proxy (id INT AUTO_INCREMENT PRIMARY KEY, url VARCHAR(20))',
        f'INSERT INTO rds_proxy(url) VALUES (\'{event["rawPath"]}\')'
    ):
        execute_sql(connection=connection, query=query)

def get_url_queries(connection):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM rds_proxy')
        connection.commit()
        url_queries = "<table><tr><th>ID</th><th>URL</th></tr>"
        for row in cursor:
            url_queries += f'<tr><td>{row["id"]}</td><td>{row["url"]}</td></tr>'
            url_queries += "</table>"
            print(f'All Current Data in rds_proxy Table (url is whatever url you hit on the HTTP API, try another random url like /hello) {url_queries}')
    connection.commit()
    return url_queries

def handler(event, context):
    print(f'request: {event}')
    if event['rawPath'] == '/favicon.ico':
        return response(404, 'no favicon here')

    connection = create_connection(
        get_username_and_password(
            os.environ['RDS_SECRET_NAME']
        )
    )

    setup_database(connection=connection, event=event)
    url_queries = get_url_queries(connection)

    return response(
        body=f'You have connected with the RDS Proxy! <br /><br /> {url_queries}'
    )