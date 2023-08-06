# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['splitpdf']

package_data = \
{'': ['*']}

install_requires = \
['PyPDF2>=1.26.0,<2.0.0', 'click>=8.0.1,<9.0.0', 'pdfreader>=0.1.10,<0.2.0']

entry_points = \
{'console_scripts': ['splitpdf = splitpdf:split_pdf']}

setup_kwargs = {
    'name': 'splitpdf',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'MrTango',
    'author_email': 'md@derico.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
