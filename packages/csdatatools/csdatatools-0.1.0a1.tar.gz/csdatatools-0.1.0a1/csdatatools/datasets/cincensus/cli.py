import click as click
from csdatatools.datasets.cincensus.validator import CinValidator


@click.group()
def cin():
    """CIN Census cleaner and validator"""
    pass


@cin.command()
@click.argument('filename', type=click.Path(exists=True))
def validate(filename):
    """Validate a CIN Census file."""
    validator = CinValidator()
    validator.validate(filename)

