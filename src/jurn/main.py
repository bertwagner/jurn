import click


# jurn log -m 'wrote some docs' -t work#jurn
# jurn log -m 'emailed customers' -t work#customers#social
# jurn log -m 'helped teach ideas' -t work#education -t work#social
# jurn print -d week
# jurn print -d month
# jurn print -d 2022-05-03 -d 2022-05-10

@click.group()
def cli():
    pass

@cli.command()
@click.option("--message", "-m", prompt=True, help="Message to save to the log.")
def log(message):
    """Adds a journal entry to the database."""
    click.echo(f"MESSAGE={message}")

@cli.command()
def print():
    """Outputs journal entries to the terminal."""
    click.echo(f"PRINTING")

if __name__ == '__main__':
    pass

