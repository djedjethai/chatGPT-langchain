import sqlite3
from pydantic.v1 import BaseModel
from typing import List
from langchain.tools import Tool

conn = sqlite3.connect("db.sqlite")

def list_tables():
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = c.fetchall()
    return "\n".join(row[0] for row in rows if row[0] is not None)

# sqlite run a query(python way)
def run_sqlite_query(query):
    c = conn.cursor()
    try:
        c.execute(query)
        return c.fetchall()
    except sqlite3.OperationalError as err: # catch the err and send it back to chatGPT
        return f"The following error occured: {str(err)}"


# create some kind of record inside the program
# that say when calling RunQueryArgsSchema it must provide a query attibut of type string
class RunQueryArgsSchema(BaseModel):
    query: str

run_query_tool = Tool.from_function(
    name="sqlite_query_query", # name can not have spaces
    description="Run a sqlite query.",
    func=run_sqlite_query,
    args_schema=RunQueryArgsSchema
)

def describe_tables(table_names):
    c = conn.cursor()
    # format the list of tables
    tables = ', '.join("'" + table + "'" for table in table_names)
    rows = c.execute(f"SELECT sql FROM sqlite_master WHERE type='table' and name IN ({tables});")
    return '\n'.join(row[0] for row in rows if row[0] is not None)

# same as RunQueryArgsSchema... will help to describe the function schema
class DescribeTablesArgsSchema(BaseModel):
    table_names: List[str]

describe_tables_tool = Tool.from_function(
    name="describe_tables", # name can not have spaces
    description="Given a list of table names, returns the schema of those tables.",
    func=describe_tables,
    args_schema=DescribeTablesArgsSchema
)

# import sqlite3
# from langchain.tools import Tool
# 
# conn = sqlite3.connect("db.sqlite")
# 
# 
# def run_sqlite_query(query):
#     c = conn.cursor()
#     c.execute(query)
#     return c.fetchall()
# 
# 
# run_query_tool = Tool.from_function(
#     name="run_sqlite_query",
#     description="Run a sqlite query.",
#     func=run_sqlite_query
# )


