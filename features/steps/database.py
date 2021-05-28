import sqlite3
import json
import os
from behave import given, when, then


TEST_DATA_PATH = os.path.dirname(os.path.abspath('test_data'))


@given(u'A temporary Person database is created')
def create_db(context):
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    statement = "CREATE TABLE Person(first_name varchar(255), last_name varchar(255))"
    cursor.execute(statement)
    context.cursor = cursor


@when(u'Test data from "{file_name}" is populated to Person table')
def insert_to_person_table(context, file_name):
    with open(f'{TEST_DATA_PATH}/{file_name}') as f:
        data = json.load(f)
    for key, value in data.items():
        first_name = value['first_name']
        last_name = value['last_name']
        statement = f"INSERT INTO Person values('{first_name}','{last_name}')"
        context.cursor.execute(statement)
        context.cursor.execute("COMMIT")


@then(u'Print all records in PERSON table')
def select_to_person_table(context):
    statement = "SELECT * FROM Person"
    context.cursor.execute(statement)
    rows = context.cursor.fetchall()
    print(rows)


@then(u'Database connection is closed')
def close_db_connection(context):
    context.cursor.close()
