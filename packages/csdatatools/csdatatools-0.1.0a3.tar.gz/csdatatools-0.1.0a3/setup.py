# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csdatatools',
 'csdatatools.datasets',
 'csdatatools.datasets.cincensus',
 'csdatatools.spec',
 'csdatatools.spec.cin',
 'csdatatools.stream']

package_data = \
{'': ['*'], 'csdatatools.spec.cin': ['samples/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'click>=8.1.2,<9.0.0',
 'lxml>=4.8.0,<5.0.0',
 'more-itertools>=8.12.0,<9.0.0',
 'sfdata-stream-parser==0.4.0',
 'tablib[cli,xlsx]>=3.2.0,<4.0.0',
 'xmlschema>=1.10.0,<2.0.0']

setup_kwargs = {
    'name': 'csdatatools',
    'version': '0.1.0a3',
    'description': "Children's Services Data Tools - Utilities for cleaning and normalising CS data by Social Finance",
    'long_description': None,
    'author': 'Michael Hanks',
    'author_email': 'michael.hanks@socialfinance.org.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
