# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cadquery_server']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.1.1,<3.0.0',
 'cadquery-massembly>=0.9.0,<0.10.0',
 'jupyter-cadquery>=3.0.0,<4.0.0',
 'matplotlib>=3.5.1,<4.0.0']

entry_points = \
{'console_scripts': ['cq-server = cadquery_server.server:run']}

setup_kwargs = {
    'name': 'cadquery-server',
    'version': '0.1.1',
    'description': 'A web server that listen for a CadQuery code and return a low-level threejs object representing the generated model.',
    'long_description': '# CadQuery server\n\nA web server that listen for a CadQuery code and return a low-level threejs object representing the generated model.\n\nIt has been created for the Cadquery VSCode extension, but could fit other needs.\n',
    'author': 'Roipoussiere',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://open-vsx.org/extension/roipoussiere/cadquery',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
