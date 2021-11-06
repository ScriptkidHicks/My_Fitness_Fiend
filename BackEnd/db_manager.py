import mysql.connector
from mysql.connector import errorcode
from os import getenv
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

"""
DB_Manager:
Class to directly talk and interact with the MySQL server.
Handles operations such as creating/using databases, table creations/insertions, etc.
"""
class DB_Manager:
    """
    Initialization function

    @params: database_name (str) - The name of the database you want to use. If it does not exist, then one will be created with that name
    """
    def __init__(self, database_name):
        self.cnx = mysql.connector.connect(
            host=getenv("DB_HOST"),
            user=getenv("DB_USER"),
            password=getenv("DB_PSWD")
        )

        self.cursor = self.cnx.cursor()

        self.db = database_name
        self.use_database(self.db)

    """
    Function to use a given database
    Tries to use the database, if the database does not exist, we try to create it

    @params: database_name (str) - Name of the database to use 
    @returns None
    """
    def use_database(self, database_name):
        try:
            self.cursor.execute(f"USE {database_name}")
        except mysql.connector.Error as err:
            print(f"Database {database_name} does not exist.")
            self.create_database(database_name)

    """
    Function to create a given database
    If the creation fails, then the program exits

    @params: database_name (str) - Name of the database to create
    @returns: None
    """
    def create_database(self, database_name):
        try:
            self.cursor.execute(f"CREATE DATABASE {database_name} DEFAULT CHARACTER SET 'utf8'")
        except mysql.connector.Error as err:
            print(f"Failed creating database: {err}")
            exit(1)

    """
    Function to get all tables for a given database

    @params: None
    @returns: A list of strings containing the names of the tables
    """
    def get_tables(self):
        try:
            self.cursor.execute("SHOW TABLES")
            return [table[0] for table in self.cursor.fetchall()]
        except mysql.connector.Error as err:
            print(f"Something went wrong! {err}")
            return False

    """
    Given a list of table names (str), will try to drop each table in the list. 

    @params: tables (str list) - A list of the table names to be deleted
    @returns: None
    """
    def drop_tables(self, tables):
        for table in tables:
            try:
                self.cursor.execute(f"DROP TABLE {table}")
                print(f"Table '{table}' has been dropped")
            except mysql.connector.Error as err:
                print(f"Table {table} could not be dropped: {err}")

    """
    Function to create a table
    Takes a table name as a string and a description of the new table's columns as a dictionary
        -> table_description = {
            col_1: column information [varchar(11) etc]
        }
    NOTE: table_description's last entry must be 'primary_key': 'xxx' for some column 'xxx'

    @params: table_name (str) - Name of the table to be created
             table_description (dict str) - A dictionary containing the column names as the keys
                                            and the column item type and configs as the values
    @returns: None
    """
    def create_table(self, table_name, table_description):
        # Create the SQL query to create the given table
        sql = f"CREATE TABLE `{table_name}` ("
        for column, desc in table_description.items():
            if column != 'primary_key':
                sql += f"`{column}` {desc},"
            else:
                sql += f"PRIMARY KEY (`{desc}`)"
        sql += ") ENGINE=InnoDB"

        # Try to create the table (unless it already exists or for some other error)
        try:
            print(f"Creating table '{table_name}': ", end="")
            self.cursor.execute(sql)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")


    """
    Function to add a row to a table
    The provided data is assumed to be JSON formatted (python dictionary)


    @params: table_name (str) - The name of the table you want to add the data into
             row_data (dict) - The data to be inserted into the 
    @returns: None
    """
    def add_row(self, table_name, row_data):
        # Get a comma separated list of the row names
        # then, reformat so each char is surrounded by ` (ex. name => `name`)
        # and turn that reformatted list into a comma separated string 
        list_of_cols = list(row_data.keys())
        formatted_cols = ["`" + col + "`" for col in list_of_cols]
        query_cols = ", ".join(formatted_cols)

        # Tuple of values to insert
        tupled_values = tuple(list(row_data.values()))  
        
        # Get the proper number of "%s"'s based on the number of columns
        # We want [:-2] to slice the last ", " from the string
        f_strings = ("%s, " * len(tupled_values))[:-2]

        sql = f"INSERT IGNORE INTO {table_name} (" + query_cols + ") VALUES (" + f_strings + ")"

        # Try to run the query
        try:
            self.cursor.execute(sql, tupled_values)
            self.cnx.commit() 
        except mysql.connector.Error as err:
            print(f"Row could not be inserted: {err}")

    """
    Function to get the column names from the INFO. SCHEMA for
    a given table.

    @params: table_name (str) - The name of the desired table
    @returns: A list of strings containing the names of the columns for the table
    """
    def get_table_columns(self, table_name):
        query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'{table_name}'"
        try:
            self.cursor.execute(query)
            return [column[0] for column in self.cursor.fetchall()]
        except mysql.connector.Error as err:
            print(f"Table columns could not be retrieved: {err}")
            return False

    """
    Function to take a query and submit it directly to the database

    @params: query (str) - An SQL query
    @returns: The result of the query
    """ 
    def submit_query(self, query):
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            return f"Something went wrong: {err}"


    """
    Private function to generate an SQL query based on given parameters

    @params: table_name (str) - The name of the table to get the data from
             columns (str list) - A list of the column names in the table to get the data from
             where_options (dict, optional) - A dictionary containing our where clauses for the query.
                                              The keys are the columns to specify, and their value is the
                                              specified value.
             where_connectors (str list, optional) - A list of strings (specifically AND and OR)
                                                     that connect the `where_options` options
    @return: An SQL query in a string
    """
    def _generate_query(self, table_name, columns, where_options={}, where_connectors=[]):
        query = "SELECT "
        query += ", ".join(columns)
        query += " FROM " + table_name

        if (where_options != {}):
            assert len(where_options) == (len(where_connectors) - 1), "Error: There must be 1 less connector between where options"
            query += " WHERE "
            for count, column_name in enumerate(where_options):
                if (count != 0):
                    query += f" {where_connectors[count].upper()} "
                query += f"`{column_name}` = '{where_options[column_name]}"

        return query + ";"


    """
    Function to get all of the rows from given parameters
    
    @params: table_name (str) - The name of the table to get the data from
             columns (str list) - A list of the column names in the table to get the data from
             where_options (dict, optional) - A dictionary containing our where clauses for the query.
                                              The keys are the columns to specify, and their value is the
                                              specified value.
             where_connectors (str list, optional) - A list of strings (specifically AND and OR)
                                                     that connect the `where_options` options
    @returns: A list of tuples, where each tuple is a row in the table
    """
    def get_all_rows(self, table_name, columns, where_options={}, where_connectors=[]):
        query = self._generate_query(table_name, columns, where_options, where_connectors)        

        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Rows could not be retrieved: {err}")

    """
    Function to get the first row from given parameters
    
    @params: table_name (str) - The name of the table to get the data from
             columns (str list) - A list of the column names in the table to get the data from
             where_options (dict, optional) - A dictionary containing our where clauses for the query.
                                              The keys are the columns to specify, and their value is the
                                              specified value.
             where_connectors (str list, optional) - A list of strings (specifically AND and OR)
                                                     that connect the `where_options` options
    @returns: A tuple containing the resulting row data
    """
    def get_one_row(self, table_name, columns, where_options={}, where_connectors=[]):
        query = self._generate_query(table_name, columns, where_options, where_connectors)        

        try:
            self.cursor.execute(query)
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Rows could not be retrieved: {err}")
                 

        
# Initialize the db_mgr
db_mgr = DB_Manager(getenv("DB_NAME"))