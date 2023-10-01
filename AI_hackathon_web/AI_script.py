

# Imports 

import sqlite3

# import sentencepiece
# import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration # text to sql
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer #data to text
# from pysentimiento import create_analyzer # sentiment

import re


# import dload
import os

class Database():
    def __init__(self, database_name):
        self._database_name = database_name
        self._database_file = os.path.join(os.getcwd(), database_name)
        self._connection = sqlite3.connect(self._database_file)
        self._db_schema = self.get_schema()

    def get_schema(self):
        try:
            # Connect to the SQLite database
            cursor = self._connection.cursor()

            # Fetch the table names
            cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
            schemas = cursor.fetchall()

            format_schema_dic = {}

            # Iterate through the tables and fetch their schema
            for schema in schemas:
                format_schema_dic[schema[0]] = self.remove_sql_comments(schema[1])

            formatted_schema = self.format_schema_func(format_schema_dic)

            self._db_schema = formatted_schema
            # return formatted_schema

        except sqlite3.Error as e:
            print(f"Error getting database schema: {e}")
            return None

    def format_schema_func(self, schema_dic):
        formatted_schema = ''
        if schema_dic:
            for table_name,schema in schema_dic.items():
                formatted_schema += '"' + table_name + '"' + " "

                # schema converter
                string_to_remove = ["\n","PRIMARY KEY", "AUTOINCREMENT", "NOT NULL", "FOREIGN KEY"]

                schema = self.cut_schema(schema)
                # schema table name + cols

                table_name_cols_schema = schema

                for string in string_to_remove:
                    table_name_cols_schema = table_name_cols_schema.replace(string,"")

                table_name_cols_schema = table_name_cols_schema.replace("`", '"')

                mod_table_name_cols_schema = ""
                for seq in table_name_cols_schema.split(","):
                    if '"' not in seq:
                        words_list = seq.split(" ")
                        
                        mod_seq = '"' + " ".join(words_list[0:-1]).strip(" ") + '" ' + words_list[-1]
                        mod_table_name_cols_schema += mod_seq + ", "
                    else:
                        mod_table_name_cols_schema += seq + ", "


                table_name_cols_schema = mod_table_name_cols_schema
                    


                # Foreing Key

                foreign_key_schema = self.get_foreign_key(schema, string_to_remove)

                foreign_key_schema = foreign_key_schema.replace("`", '"')

                # Primary Key
                primary_key_schema = self.get_primary_key(schema, string_to_remove)

                primary_key_schema = primary_key_schema.replace("`", '"')

                # Final schema

                formatted_schema += table_name_cols_schema + " " + foreign_key_schema + " " + primary_key_schema + " [SEP] "

        return formatted_schema

    def get_primary_key(self, schema, string_to_remove):
        primary_key_schema = ""

        for col in schema.split(","):
            if "PRIMARY KEY" in col:
                primary_key_schema = col
                for string in (string_to_remove+["TEXT", "INTEGER", " "]):
                    primary_key_schema = primary_key_schema.replace(string,"")
            primary_key_schema = primary_key_schema.replace("    ","")

        # if there are no primary keys, it tries to find the value with _id in
        # very unreliable, mostly here to work with the db we have
        # if primary_key_schema == "":
        #     for col in schema.split(","):
        #       if "_id" in col or "key" in col:
        #         primary_key_schema = col
        #         for string in (string_to_remove+["TEXT", "INTEGER", " "]):
        #           primary_key_schema = primary_key_schema.replace(string,"")

        #       primary_key_schema = primary_key_schema.replace("    ","")

        primary_key_schema = "primary key: " + primary_key_schema

        return primary_key_schema

    def get_foreign_key(self, schema, string_to_remove):
        foreign_key_schema = schema.split(",")

        foreign_keys_list = []

        for col in foreign_key_schema:
            if "FOREIGN KEY" in col:
                for string in (string_to_remove + ["(", ")"]):
                    col = col.replace(string,"")

                col = col.replace("REFERENCES", "from")

                foreign_keys_list.append(col)


        foreign_key_schema ="foreign key: " +  "".join(foreign_keys_list)

        return foreign_key_schema

    def cut_schema(self, schema):
        schema = schema[schema.index("(")+1:]
        schema = schema[::-1]
        schema = schema[schema.index(")")+1:]
        schema = schema[::-1]
        return schema
    

    def remove_sql_comments(self, sql_code):
        # Remove single-line comments (e.g., -- This is a comment)
        sql_code = re.sub(r'--.*?(\n|$)', '', sql_code, flags=re.DOTALL)
        
        # Remove multi-line comments (e.g., /* This is a comment */)
        sql_code = re.sub(r'/\*.*?\*/', '', sql_code, flags=re.DOTALL)
        
        return sql_code
    
    # Getters
    def getSchema(self):
        return self._db_schema

    def getConnection(self):
        return self._connection


# Handling the input

class Query():
    def __init__(self, question, database_name, models):
        self._question = question
        self._database = Database(database_name)
        self._tables_hints = []
        self._models = models


    # Interface for the main query func
    def query(self):
        tables_hints = []
        answer = self.query_fun()
        return answer



    # Main query Function
    def query_fun(self, query_conf=False):

        ## Input checker
        if not self.check_question(self._question):
            answer = "nSorry, this query seems unfit for processing. Try rephrasing."
            return answer

        ## text=>sql
        generated_sql = self.generate_sql(self._question)

        ## Check with the user if we should proceed with the query
        if self.check_sql(generated_sql,query_conf):
        ## interrogate the database
            results = self.interrogate_db(self._question, generated_sql, self._database._connection)
            if "Error" in results:
                return results
        else:
            answer = 'You might want to rephrase your question and ideally include more information for better results.'
            return answer

        # Data Checker
        if not self.check_data(results):
            answer = "I have been unable to find an answer."
            return answer

        ## Ask user how he wants the asnwer converted to plain text input("Would you like the answer converted to plain text? it contains {cols}, {rows}")
        if self.get_user_format_pref(results):
        ## Data=>text func
            answer = self.data_to_text(self._question,results)

        else:
        ## Data Formating func (the default option if the )
            answer = self.data_format(results)

        return answer
    
    # Checking Question
    def check_question(self):
        if self._question == "" or not self.neutral(self._question):
            return False
        return True
    
    def neutral(self):
        sentiment = self.models._analyzer.predict(self._question)
        if sentiment.probas["NEU"] < 0.5:
            return False
        return True
    
    # LLM NLP -> SQL

    def generate_sql(self):
        input_text = " ".join(["Question:",self._question, "Schema:", self._database._db_schema])
        model_inputs = self._models.text_to_sql_tokenizer(input_text, return_tensors="pt")
        outputs = self._models.text_to_sql_model.generate(**model_inputs, max_length=512)
        output_ids_list = outputs.tolist()

        # Decode each generated sequence individually
        decoded_outputs = []
        for output_ids in output_ids_list:
            decoded_output = self._models.text_to_sql_tokenizer.decode(output_ids, skip_special_tokens=True)
            decoded_outputs.append(decoded_output)
        final_sql = "".join(decoded_outputs)
        return final_sql

    # Checking the sql output

    def check_sql(self, sql, query_conf):
        # general checks (injections, hallucinations, etc.)
        if "SELECT" not in sql.split(" ")[0]:
            return False

        # Users interaction
        if not query_conf:
            return True
        user_conf = input("This is the SQLite query I wrote, would you like me to proceed?\nY/n\n" + sql + "\n")
        while (user_conf != 'Y' or user_conf != 'n') == False:
            user_conf = input("Sorry, that is not a valid input, Type 'Y' for yes, 'n' for no.")
        if user_conf == 'Y':
            return True
        elif user_conf == 'n':
            return False
        
    # SQL engine
    def interrogate_db(self, generated_sql):
        try:
            cursor = self._database._connection.cursor()
            cursor.execute(generated_sql)
            results = cursor.fetchall()
            return results
        except sqlite3.Error as e:
            answer = f"Error reading database schema: {e}"
            return answer
    
    # Result checker
    def check_data(self, result):
        if len(result[0]) == 0 or result[0] is None or result is None or result == [(None,)]:
            return False
        return True

    # Answer format
    def get_user_format_pref(self, result):
        if len(result[0]) > 1:
            return False
        return True

    # Table formatter

    def data_format(self, data):
        answer = ""  # "Here are the results for your question:\n"
        col_lens = self.longest_words_per_col(data)
        for row in data:
            line = ""
            for index, info in enumerate(row):
                formatted_string = "{:<" + str(col_lens[index]) +"} | "
                line += formatted_string.format(str(info))
            answer += str(line)[:-3] + "\n"
        return answer

    def longest_words_per_col(self,data):
        max_lengths_per_col = []
        num_cols = len(data[0])

        for col_index in range(num_cols):
            column_data = []
            for row in data:
                column_data.append(row[col_index])
            longest_word = max(column_data, key=len)
            max_lengths_per_col.append(len(longest_word))

        return max_lengths_per_col
    
    # Data -> Text

    def data_to_text(self, table):

        result_list = []
        for row in table:
            result_list.append(row[0])

        data = ", ".join(result_list)
        input_text = f"Put the answer '{data}' into a full sentence to create a response to the question '{self._question}?'"
        input_ids = self._models.data_to_text_tokenizer(input_text, return_tensors="pt").input_ids

        outputs = self._models.data_to_text_model.generate(input_ids, max_new_tokens=150)

        answer = self._models.data_to_text_tokenizer.decode(outputs[0]).replace("</s>", "")
        return answer.replace("<pad>", "")



class Models():
    def __init__(self):
        # Init text to sql 
        self._text_to_sql_model = AutoModelForSeq2SeqLM.from_pretrained('gaussalgo/T5-LM-Large-text2sql-spider')
        self._text_to_sql_tokenizer = AutoTokenizer.from_pretrained('gaussalgo/T5-LM-Large-text2sql-spider')

        # Init data to text
        self._data_to_text_tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-large")
        self._data_to_text_model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large")

        # Sentiment Analysis
        # self._analyzer = create_analyzer(task="sentiment", lang="en")


# Initiating the models

models = Models()

# Testing
if __name__ == "__main__":
    query = Query('List all varieties', 'jupyter_db.db', models)
    print(query.query_fun())
 

