import sqlite3
import os

def init_db(db_path, db_filename):
    # sqlite3 doens't like the ~ alias so we have to expand it first
    home_directory = os.path.expanduser('~')
    expanded_db_path = db_path.replace('~',home_directory)

    # try to make the directory if it doesn't exist
    if not os.path.exists(expanded_db_path):
        os.makedirs(expanded_db_path)

    db_file_path = os.path.join(expanded_db_path,db_filename)

    # connect and create the db if it doesn't exist. create the table if it doesn't exist.
    con = sqlite3.connect(db_file_path)
    con.execute("CREATE TABLE IF NOT EXISTS entry (id INTEGER PRIMARY KEY, insert_date DEFAULT CURRENT_TIMESTAMP, entry TEXT, tag)")

    return con