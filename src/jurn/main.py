import click


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
    if last_entry < early_end:
        pass
    else:
        exit()

@cli.command()
@click.option("--message", "-m", prompt=True, help="Message to save to the journal.")
def log(message):
    """Adds a journal entry to the database."""
    click.echo(f"MESSAGE={message}")

@cli.command()
def print():
    """Outputs journal entries to the terminal."""
    click.echo(f"PRINTING")

if __name__ == '__main__':
    cli()

