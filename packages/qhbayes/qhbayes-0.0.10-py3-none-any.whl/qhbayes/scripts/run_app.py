import click
from qhbayes.app import make_dashboard


@click.command()
def run_app():
    make_dashboard()
