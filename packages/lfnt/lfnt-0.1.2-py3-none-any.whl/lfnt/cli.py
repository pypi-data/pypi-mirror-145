import click
from pprint import pprint
from .app import app
from .digestion import DigestiveSystem


de = DigestiveSystem()
CONTEXT_SETTINGS = de.get()


@click.group(context_settings=CONTEXT_SETTINGS)
def lfnt():
    """For eating development-environment elephants."""
    pass


lfnt_group = lfnt.group(context_settings=CONTEXT_SETTINGS)
lfnt_command = lfnt.command(context_settings=CONTEXT_SETTINGS)


# browse
@lfnt_command
def browse():
    """Run in a web browser."""
    app.run()


# life-cycle
@lfnt_command
def new():
    """Initialize a configuration."""
    pass


# digestion
@lfnt_command
@click.option("-a", "--apt", multiple=True)
@click.option("-b", "--brew", multiple=True)
@click.option("-d", "--dnf", multiple=True)
def eat(apt, brew, dnf):
    """Ingest packages and applications."""
    pass


@lfnt_command
@click.option("-a", "--apt", multiple=True)
@click.option("-b", "--brew", multiple=True)
@click.option("-d", "--dnf", multiple=True)
def vomit():
    """Eject packages and applications."""
    pass


@lfnt_command
def dump():
    """Take a config dump."""
    pprint(de.dump())


if __name__ == "__main__":
    lfnt()
