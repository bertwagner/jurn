from email.policy import default
import click
from datetime import date, datetime, timedelta
import jurn.utils as u
import pprint

@click.group()
@click.option("--early-end", "-ee", type=int, help="Stop jurn from executing if this amount of time has not passed since the last journal entry. Useful to supress jurn prompting too frequently if adding to a .bashrc file or schedule.")
@click.option("--db-path", "-dp", help="The folder path for jurn's sqlite3 database. Defaults to ~/.jurn/ .", default="~/.jurn/")
@click.option("--db-filename", "-df", help="The filename for jurn's sqlite3 database. Defaults to jurn.db .", default="jurn.db")
@click.pass_context
def cli(ctx,early_end,db_path,db_filename):
    ctx.ensure_object(dict)
    ctx.obj['DB_CONNECTION'] = u.init_db(db_path,db_filename)

    # determine if the prompt should be skipped based on the --early-end parameter and the last entry's timestamp.
    last_entry_timestamp=u.last_entry_timestamp(ctx.obj['DB_CONNECTION'])

    if early_end==None:
        pass
    else:
        delay_until_timestamp = last_entry_timestamp + timedelta(minutes=early_end)
        if delay_until_timestamp < datetime.utcnow():
            pass
        else:
            exit()




@cli.command()
@click.option("--message", "-m", prompt=True, prompt_required=True, required=True, is_flag=False, help="Message to save to the journal.")
@click.option("--tag", "-t", prompt=True, prompt_required=False, default="", type=u.DistinctTags(), help="Tags to use for your journal entry. Hierarchies can be denoted with hashtags, eg. parent-cateogry#sub-category#child-category")
@click.pass_context
def log(ctx,message,tag):
    """Adds a journal entry to the database."""

    with ctx.obj['DB_CONNECTION']:
        ctx.obj['DB_CONNECTION'].execute("INSERT INTO entry (entry,tag) VALUES(?,?)",(message,tag,))

@cli.command()
@click.option("--duration", "-d", type=click.Choice(['day','week','month','year'], case_sensitive=False), help="Inclusive time period to print journal entries for.")
@click.option('--date-start', "-ds", type=click.DateTime(formats=["%Y-%m-%d"]), help="Inclusive start date range.")
@click.option('--date-end', "-de", type=click.DateTime(formats=["%Y-%m-%d"]), help="Inclusive end date range.")
@click.pass_context
def print(ctx,duration,date_start,date_end):
    """Outputs journal entries to the terminal for a specified date range (defaults to today)."""
    
    (date_start,date_end)=u.calculate_date_range(duration,date_start,date_end)
    entries = u.retrieve_entries(date_start,date_end,ctx.obj['DB_CONNECTION'])
    
    previous_tags = ['']
    
    if str(date_start)[:10] == str(date_end)[:10]:
        click.echo(str(date_start)[:10])
    else: 
        click.echo(str(date_start)[:10] + ' to ' + str(date_end)[:10])

    for entry in entries:
        current_level = 0
        current_tags = entry['tag'].split('#')

        for tag in current_tags:
            spaces = ' ' * (current_level * 2)
            if (current_level < len(previous_tags) and tag != previous_tags[current_level]) or (current_level >= len(previous_tags)):
                if tag != '':
                    click.echo(spaces+'  • '+tag)
            
            if tag != '':
                current_level+=1

        spaces = ' ' * (current_level * 2)
        click.echo(spaces + '  • ' + str(entry['entry']))

        previous_tags = current_tags

if __name__ == '__main__':
    cli(obj={})