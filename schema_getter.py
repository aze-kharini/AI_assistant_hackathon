import sqlite3

def connect_fun(database_name):
    try:
        connection = sqlite3.connect(database_file)
        print("Connected to the database")
        return connection
    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")
        return None


database_file = '/home/viridis/VSCode/CK401/AI_dev/csv_tables/education_db.sqlite' # this is where you need to put in the absolute path to the db

# def get_sqlite_schema(db_filename):
#     try:
#         # Connect to the SQLite database
#         conn = connect_fun(db_filename)
#         cursor = conn.cursor()

#         # Fetch the table names
#         cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
#         schemas = cursor.fetchall()

#         format_schema = {}

#         # Iterate through the tables and fetch their schema
#         for schema in schemas:
#             format_schema[schema[0]] = schema[1]

#         return format_schema_func(format_schema)

#     except sqlite3.Error as e:
#         print(f"Error reading database schema: {e}")
#         return None

#     finally:
#         if conn:
#             conn.close()


# database_schema_info = get_sqlite_schema(database_file)

# print(database_schema_info)


def format_schema_func(schema_dic):
    print(schema_dic)
    formatted_schema = ''
    if schema_dic:
        for table_name,schema in schema_dic.items():
            formatted_schema += table_name + " "

            # schema converter
            string_to_remove = ["\n","PRIMARY KEY", "AUTOINCREMENT", "NOT NULL", '"', "FOREIGN KEY", ","]

            schema = cut_schema(schema)
            # schema table name + cols

            table_name_cols_schema = schema
            
            for string in string_to_remove:
                table_name_cols_schema = table_name_cols_schema.replace(string,"")

            # Foreing Key

            foreign_key_schema = get_foreign_key(schema, string_to_remove)

            # Primary Key
            primary_key_schema = get_primary_key(schema, string_to_remove)

            # Final schema

            formatted_schema += table_name_cols_schema + " " + foreign_key_schema + " " + primary_key_schema + "[SEP]\n"

    return formatted_schema


def get_primary_key(schema, string_to_remove):
    primary_key_schema = schema.split(",")[0]

    for string in string_to_remove:
        primary_key_schema = primary_key_schema.replace(string,"")
    primary_key_schema = primary_key_schema.replace("    ","")

    primary_key_schema = "primary key: " + primary_key_schema.split(" ")[0]

    return primary_key_schema

def get_foreign_key(schema, string_to_remove):
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

def cut_schema(schema):
    schema = schema[schema.index("(")+1:]
    schema = schema[::-1]
    schema = schema[schema.index(")")+1:]
    schema = schema[::-1]
    return schema


# print(format_schema(database_schema_info))

def get_sqlite_schema(db_filename):
    try:
        # Connect to the SQLite database
        conn = connect_fun(db_filename)
        cursor = conn.cursor()

        # Fetch the table names
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
        schemas = cursor.fetchall()

        format_schema = {}

        # Iterate through the tables and fetch their schema
        for schema in schemas:
            format_schema[schema[0]] = schema[1]

        return format_schema_func(format_schema)

    except sqlite3.Error as e:
        print(f"Error reading database schema: {e}")
        return None

    finally:
        if conn:
            conn.close()


database_schema_info = get_sqlite_schema(database_file)

print(database_schema_info)