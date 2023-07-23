import click


@click.group(short_help="tour CLI.")
def tour():
    """tour CLI.
    """
    pass


@tour.command()
@click.argument("name", default="tour")
def command(name):
    """Docs.
    """
    click.echo("Hello, {name}!".format(name=name))


def get_commands():
    return [tour]
