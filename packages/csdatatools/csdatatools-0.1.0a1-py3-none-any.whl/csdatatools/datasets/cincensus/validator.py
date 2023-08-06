from pathlib import Path

import xmlschema

from csdatatools.spec import cin


class CinValidator:

    def __init__(self, version='2022'):
        self._version = version
        schema_file = Path(cin.__file__).parent / f"cin-{version}.xsd"
        self._schema = xmlschema.XMLSchema(schema_file)

    def validate(self, filename):
        errors = list(self._schema.iter_errors(filename))

        for error in errors:
            print(error)

        if len(errors) == 0:
            print(f"{filename} is valid")
