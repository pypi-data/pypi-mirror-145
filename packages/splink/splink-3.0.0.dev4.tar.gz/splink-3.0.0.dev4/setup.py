# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['splink', 'splink.duckdb', 'splink.spark', 'splink.sqlite']

package_data = \
{'': ['*'],
 'splink': ['files/*',
            'files/chart_defs/*',
            'files/chart_defs/del/*',
            'files/external_js/*',
            'files/splink_comparison_viewer/*',
            'files/templates/*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0',
 'altair>=4.2.0,<5.0.0',
 'duckdb>=0.3.2,<0.4.0',
 'jsonschema>=3.2,<4.0',
 'pandas>=1.0.0,<2.0.0',
 'pyspark>=3.2.1,<4.0.0',
 'rapidfuzz>=2.0.3,<3.0.0',
 'sqlglot==1.23.1']

setup_kwargs = {
    'name': 'splink',
    'version': '3.0.0.dev4',
    'description': "Implementation of Fellegi-Sunter's canonical model of record linkage in Apache Spark, including EM algorithm to estimate parameters",
    'long_description': '',
    'author': 'Robin Linacre',
    'author_email': 'robinlinacre@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/moj-analytical-services/splink',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
