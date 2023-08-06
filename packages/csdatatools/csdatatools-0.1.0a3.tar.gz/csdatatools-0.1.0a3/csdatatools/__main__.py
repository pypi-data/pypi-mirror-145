import click as click

from csdatatools.datasets.cincensus.cli import cin


@click.group()
def cli():
    pass


cli.add_command(cin)


if __name__ == '__main__':
    cli()
