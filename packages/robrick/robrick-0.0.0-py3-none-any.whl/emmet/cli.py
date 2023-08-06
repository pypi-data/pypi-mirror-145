import click


@click.group()
def emmet():
    pass


@emmet.command()
def install():
    click.echo("Installing...")
