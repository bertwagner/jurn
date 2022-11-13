from email.policy import default
import click
from datetime import date, datetime, timedelta
import src.jurn.utils as u

# jurn log -m 'wrote some docs' -t work#jurn
# jurn log -m 'emailed customers' -t work#customers#social
# jurn log -m 'helped teach ideas' -t work#education
# jurn print -d week
# jurn print -d month
# jurn print -d 2022-05-03 -d 2022-05-10

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
@click.option("--message", "-m", prompt=True, help="Message to save to the journal.")
@click.option("--tag", "-t",  help="Tags to use for your journal entry. Hierarchies can be denoted with hashtags, eg. parent-cateogry#sub-category#child-category")
def log(message,tag):
    """Adds a journal entry to the database."""

    with DB_CONNECTION:
        DB_CONNECTION.execute("INSERT INTO entry (entry,tag) VALUES(?,?)",(message,tag,))

@cli.command()
@click.option("--duration", "-d", type=click.Choice(['day','week','month','year'], case_sensitive=False), help="Inclusive time period to print journal entries for.")
@click.option('--date-start', "-ds", type=click.DateTime(formats=["%Y-%m-%d"]), help="Inclusive start date range.")
@click.option('--date-end', "-de", type=click.DateTime(formats=["%Y-%m-%d"]), help="Inclusive end date range.")
def print(duration,date_start,date_end):
    """Outputs journal entries to the terminal."""
    
    if date_start==None and date_end:
        click.echo("Must specify --date_start if providing --date_end")
    elif (duration and (date_start or date_end)):
        click.echo("Must specify either --duration or --date_start and --date_end")
    elif (duration==None and date_start==None and date_end==None):
        duration="day"
        click.echo(f'using default duration {duration}')
    elif (duration):
        click.echo(f'using duration {duration}')
    elif (date_start):
        click.echo(f'using date_start {date_start}')

        if (date_end):
            click.echo(f'using date_end {date_end}')
        else:
            date_end = date.today()
            click.echo(f'using default date_end today {date_end}')

if __name__ == '__main__':
    cli()

