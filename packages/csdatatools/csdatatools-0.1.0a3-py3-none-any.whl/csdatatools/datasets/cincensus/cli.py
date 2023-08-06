import shutil
from pathlib import Path

import click as click
import tabulate
from sfdata_stream_parser.parser.xml import parse

from csdatatools.datasets.cincensus.cin_record import message_collector, export_table
from csdatatools.datasets.cincensus.config import Config
from csdatatools.datasets.cincensus.filters import strip_text, add_context, add_config, clean
from csdatatools.datasets.cincensus.validator import CinValidator
from csdatatools.spec import cin as cin_spec

__formats = {
    '.csv': ('csv', 't'),
    '.tsv': ('tsv', 't'),
    '.yml': ('yaml', 't'),
    '.yaml': ('yaml', 't'),
    '.json': ('json', 't'),
    '.xls': ('xls', 'b'),
    '.xlsx': ('xlsx', 'b'),
}


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


@cin.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('-o', '--output')
@click.option('-f', '--format',  default=None, type=click.Choice(tabulate._table_formats))
def eventreport(filename, output, format):
    """Create a table of events from a CIN Census file."""

    stream = parse(filename)
    stream = strip_text(stream)
    stream = add_context(stream)
    stream = add_config(stream, Config().fields_with_prefix(['Message', 'Children', 'Child']))
    stream = clean(stream)
    stream = message_collector(stream)

    data = export_table(stream)

    if output is None or output == "" or output == "-":
        print(data.export('cli', tablefmt=format))
    else:
        output = Path(output)
        format, stream_format = __formats[output.suffix]
        with open(output, f'w{stream_format}') as f:
            f.write(data.export(format))


@cin.command(name='export-sample')
@click.argument('filename', type=click.Path(exists=False))
def exportsample(filename):
    """Export a sample file for testing."""

    sample_file = Path(cin_spec.__file__).parent / 'samples/cin-2022.xml'
    assert sample_file.exists(), "Sample file not found"

    shutil.copy(sample_file, filename)
    click.echo(f"Sample file written to {filename}")
