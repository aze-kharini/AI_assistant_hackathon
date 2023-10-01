# Test for libraries and just what the hell is going on
# NumPy

# import numpy as np

# matrix_1 = np.arange(1, 11, 1).reshape(5,2)
# matrix_2 = np.arange(10).reshape(2,5)
# product = matrix_1@matrix_2

# print(product)

# print(product.sum(axis=1))

# print(np.sin(product))

# TensorFlow
# result = [('Gesha',), ('Typica',), ('Bourbon',), ('Caturra',), ('Maragogipe',), ('Mundo Nuovo',), ('SL-28',)]
# def data_to_text(data, question):
#     answer = 'Here are the results for ' + question + ':\n'
#     for row in data:
#         line = ""
#         for info in row:
#             line += str(info) + " "
#         answer += str(line) + "\n"
#     return "Bot:\n" + answer

# print(data_to_text(result, 'list all varieties that have a higher rating than 3'))

# query = 'test'

# def user_confirm(query):
#     user_conf = input("Bot:\nThis is the SQLite query I wrote, would you like me to proceed?\nY/n\n" + query + "\nUser: ")
#     while (user_conf != 'Y' or user_conf != 'n') == False:
#         user_conf = input("Bot:\nSorry, that is not a valid input, Type 'Y' for yes, 'n' for no.")
#     if user_conf == 'Y':
#         return True
#     elif user_conf == 'n':
#         return False
    
# print(user_confirm(query))


# import pandas as pd
# import os
# import torch
# from transformers import T5Tokenizer, T5ForConditionalGeneration
# from transformers.optimization import Adafactor
# import time
# import warnings

# warnings.filterwarnings('ignore')

# tokenizer = T5Tokenizer.from_pretrained('Sachinkelenjaguri/sa_T5_Table_to_text')

# model = T5ForConditionalGeneration.from_pretrained('Sachinkelenjaguri/sa_T5_Table_to_text', return_dict=True)

# def generate(text):
#     model.eval()
#     input_ids = tokenizer.encode("WebNLG:{} </s>".format(text), return_tensors="pt")  # Batch size 1
#     s = time.time()
#     outputs = model.generate(input_ids)
#     gen_text=tokenizer.decode(outputs[0]).replace('<pad>','').replace('</s>','')
#     elapsed = time.time() - s
#     print('Generated in {} seconds'.format(str(elapsed)[:4]))
  
#     return gen_text

# print(generate(' Russia | leader | Putin'))
# import re

# query = "SELECT COUNT(DISTINCT name) FROM varieties"
# result = [('Gesha',), ('Typica',), ('Bourbon',), ('Caturra',), ('Maragogipe',), ('Mundo Nuovo',), ('SL-28',)]

# def result_to_table(result):
#     table = ""
#     for row in result:
#         line = ''
#         for element in row:
#             line += element + " | "
#         table += line[:-3] + '\n'
#     return table

# print(result_to_table(result))

# sqlite_select_keywords = [
#     "SELECT",
#     "DISTINCT",
#     "FROM",
#     "WHERE",
#     "GROUP BY",
#     "HAVING",
#     "ORDER BY",
#     "LIMIT",
#     "OFFSET",
#     "AS",
#     "INNER JOIN",
#     "LEFT JOIN",
#     "RIGHT JOIN",
#     "OUTER JOIN",
#     "ON",
#     "AND",
#     "OR",
#     "NOT",
#     "IS",
#     "NULL",
#     "BETWEEN",
#     "LIKE",
#     "IN",
#     "CASE",
#     "WHEN",
#     "THEN",
#     "ELSE",
#     "END",
#     "EXISTS",
#     "COUNT", 
#     "SUM", 
#     "MAX",
#     "MIN",
#     "AVG"
# ]

# def split(delimiters, string, maxsplit=0):
#     import re
#     regex_pattern = '|'.join(map(re.escape, delimiters))
#     return re.split(regex_pattern, string, maxsplit)



# def query_to_column(query):
#     select_clause = query.split('FROM')[0]
#     columns = []
#     delimiters = [' ', '(', ')']
#     sqlite_select_keywords = [
#     "SELECT",
#     "DISTINCT",
#     "FROM",
#     "WHERE",
#     "GROUP BY",
#     "HAVING",
#     "ORDER BY",
#     "LIMIT",
#     "OFFSET",
#     "AS",
#     "INNER JOIN",
#     "LEFT JOIN",
#     "RIGHT JOIN",
#     "OUTER JOIN",
#     "ON",
#     "AND",
#     "OR",
#     "NOT",
#     "IS",
#     "NULL",
#     "BETWEEN",
#     "LIKE",
#     "IN",
#     "CASE",
#     "WHEN",
#     "THEN",
#     "ELSE",
#     "END",
#     "EXISTS",
#     "COUNT", 
#     "SUM", 
#     "MAX",
#     "MIN",
#     "AVG"]
#     for word in split(delimiters, select_clause):
#         if word not in sqlite_select_keywords and word != "":
#             columns.append(word)
#     return columns

# print(query_to_column(query))
import sqlite3

def connect_fun(database_name):
    try:
        connection = sqlite3.connect(database_file)
        print("Connected to the database")
        return connection
    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")
        return None


database_file = '/home/viridis/VSCode/CK401/AI_dev/jupyter_db.db' # this is where you need to put in the absolute path to the db

# conn = connect_fun(database_file)
# cursor = conn.cursor()
# cursor.execute("SELECT schema_code FROM schemas;")
# db_schema = cursor.fetchone()[0]
# conn.close()

# print(db_schema)

def get_sqlite_schema(db_filename):
    try:
        # Connect to the SQLite database
        conn = connect_fun(db_filename)
        cursor = conn.cursor()

        # Fetch the schema information
        cursor.execute("SELECT * FROM sqlite_master;")
        table_master = cursor.fetchall()
        print(table_master)

        # Fetch the schema information
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = cursor.fetchall()
        schema = {}

        # Iterate through the tables and fetch their schema
        for table_name in table_names:
            table_name = table_name[0]
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            print(columns)
            column_names = [column[1] for column in columns]
            schema[table_name] = column_names

        return schema

    except sqlite3.Error as e:
        print(f"Error reading database schema: {e}")
        return None

    finally:
        if conn:
            conn.close()

# Replace 'your_database.db' with the path to your SQLite database file
# database_file = 'jupyter_db.db'
database_schema = get_sqlite_schema(database_file)

if database_schema:
    print("Database Schema:")
    for table_name, columns in database_schema.items():
        print(f"Table: {table_name}")
        print("Columns:", columns)
else:
    print("Failed to retrieve the database schema.")
