import click
from datetime import date


# jurn log -m 'wrote some docs' -t work#jurn
# jurn log -m 'emailed customers' -t work#customers#social
# jurn log -m 'helped teach ideas' -t work#education -t work#social
# jurn print -d week
# jurn print -d month
# jurn print -d 2022-05-03 -d 2022-05-10

@click.group()
@click.option("--early-end", "-ee", type=int, help="Stop jurn from executing if this amount of time has not passed since the last journal entry. Useful to supress jurn prompting too frequently if adding to a .bashrc file or schedule.")
def cli(early_end):
    last_entry=5
    if early_end==None or last_entry < early_end:
        pass
    else:
        exit()

@cli.command()
@click.option("--message", "-m", prompt=True, help="Message to save to the journal.")
def log(message):
    """Adds a journal entry to the database."""
    click.echo(f"MESSAGE={message}")

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

