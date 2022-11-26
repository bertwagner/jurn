from email.policy import default
import click
from datetime import date, datetime, timedelta
import src.jurn.utils as u
import pprint

@click.group()
@click.option("--early-end", "-ee", type=int, help="Stop jurn from executing if this amount of time has not passed since the last journal entry. Useful to supress jurn prompting too frequently if adding to a .bashrc file or schedule.")
@click.option("--db-path", "-dp", help="The folder path for jurn's sqlite3 database. Defaults to ~/.jurn/ .", default="~/.jurn/")
@click.option("--db-filename", "-df", help="The filename for jurn's sqlite3 database. Defaults to jurn.db .", default="jurn.db")
def cli(early_end,db_path,db_filename):
    global DB_CONNECTION 
    DB_CONNECTION = u.init_db(db_path,db_filename)

    # determine if the prompt should be skipped based on the --early-end parameter and the last entry's timestamp.
    last_entry_timestamp=u.last_entry_timestamp(DB_CONNECTION)

    if early_end==None:
        pass
    else:
        delay_until_timestamp = last_entry_timestamp + timedelta(minutes=early_end)
        if delay_until_timestamp < datetime.utcnow():
            pass
        else:
            exit()

@cli.command()
@click.option("--message", "-m", prompt=True, is_flag=False, flag_value="", help="Message to save to the journal.")
@click.option("--tag", "-t", prompt=True,  help="Tags to use for your journal entry. Hierarchies can be denoted with hashtags, eg. parent-cateogry#sub-category#child-category")
def log(message,tag):
    """Adds a journal entry to the database."""

    with DB_CONNECTION:
        DB_CONNECTION.execute("INSERT INTO entry (entry,tag) VALUES(?,?)",(message,tag,))

@cli.command()
@click.option("--duration", "-d", type=click.Choice(['day','week','month','year'], case_sensitive=False), help="Inclusive time period to print journal entries for.")
@click.option('--date-start', "-ds", type=click.DateTime(formats=["%Y-%m-%d"]), help="Inclusive start date range.")
@click.option('--date-end', "-de", type=click.DateTime(formats=["%Y-%m-%d"]), help="Inclusive end date range.")
def print(duration,date_start,date_end):
    """Outputs journal entries to the terminal for a specified date range (defaults to today)."""
    
    (date_start,date_end)=u.calculate_date_range(duration,date_start,date_end)
    entries = u.retrieve_entries(date_start,date_end,DB_CONNECTION)
    
    previous_tag = ''
    parent_tag = ''
    current_level = 0
    for entry in entries:
        current_tag = entry['tag']
        split_tags = current_tag.split('#')

        if current_tag != previous_tag:
            click.echo('- '+str(entry['tag']))
            previous_tag = current_tag
        
        click.echo('    - ' + str(entry['entry']))

