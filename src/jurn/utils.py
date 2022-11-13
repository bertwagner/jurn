import sqlite3
import os
from datetime import datetime, date
from dateutil import relativedelta
import click

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

def last_entry_timestamp(con):
    
    dt_string = "0001-01-01 00:00:00" 
    format = "%Y-%m-%d %H:%M:%S"
    default_entry_timestamp = datetime.strptime(dt_string, format)
    last_entry_timestamp = default_entry_timestamp

    with con:
        cur = con.cursor()
        res = cur.execute("SELECT MAX(insert_date) FROM entry")
        last_entry_timestamp = res.fetchone()[0]

        if last_entry_timestamp==None:
            last_entry_timestamp=default_entry_timestamp
    
    return datetime.strptime(last_entry_timestamp, format)

def calculate_date_range(duration,date_start,date_end):
    if date_start==None and date_end:
        click.echo("Must specify --date_start if providing --date_end")
        exit()

    elif (duration and (date_start or date_end)):
        click.echo("Must specify either --duration or --date_start and --date_end")
        exit()

    elif (duration==None and date_start==None and date_end==None):
        #click.echo(f'using default duration {duration}')
        duration="day"
        date_start=date.today()
        date_end=datetime.now()
        
    elif (duration):
        #click.echo(f'using duration {duration}')
        date_end=datetime.now()

        if duration=="day":
            date_start=date.today()
        elif duration=="week":
            date_start=date.today()+relativedelta.relativedelta(weeks=-1)
        elif duration=="month":
            date_start=date.today()+relativedelta.relativedelta(months=-1)
        elif duration=="year":
            date_start=date.today()+relativedelta.relativedelta(years=-1)
        else:
            raise Exception("Invalid duration value passed.")

    elif (date_start):
        #click.echo(f'using date_start {date_start}')

        if (date_end):
            #click.echo(f'using date_end {date_end}')
            pass
        else:
            date_end = datetime.now()
            #click.echo(f'using default date_end today {date_end}')
    
    return (date_start,date_end)

