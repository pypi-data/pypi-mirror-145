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
{'console_scripts': ['cq-server = cadquery_server.server:main']}

setup_kwargs = {
    'name': 'cadquery-server',
    'version': '0.1.2',
    'description': 'A web server that executes a given CadQuery code and returns the generated model as a threejs object.',
    'long_description': '# CadQuery server\n\nA web server that executes a given CadQuery code and returns the generated model as a threejs object.\n\nIt has been created for the [Cadquery VSCode extension](https://open-vsx.org/extension/roipoussiere/cadquery), but could fit other needs.\n\n## Installation\n\n    pip install cq-server\n\nNote that you must have CadQuery installed on your system (if not, you might be interested by [the docker image](https://hub.docker.com/r/cadquery/cadquery-server)).\n\n## Usage\n\n### Starting the server\n\nOnce installed, the `cq-server` command should be available on your system:\n\nCLI options:\n\n- `-p`, `--port`: server port (default: 5000)\n\nExample:\n\n    cq-server -p 5000\n\n### Writing a CadQuery code\n\nThe Python script must contain the `show()` method.\n\nExample:\n\n```py\nimport cadquery as cq\n\nmodel = cq.Workplane("XY").box(1, 2, 3)\n\nshow(model)\n```\n\nNote that the `import cadquery as cq` part is optional (`cadquery` is already imported at server start), but can be useful to enable syntax check and code completion in your IDE.\n\nPlease read the [CadQuery documentation](https://cadquery.readthedocs.io/en/latest/) for more details about the CadQuery library.\n\n### Using the server\n\nOnce the server is started, a CadQuery Python code can be send in a `POST` request payload.\n\nExample:\n\n    curl -X POST --data-binary "@./examples/test.py" 127.0.0.1:5000\n\nIt should return the model as a threejs object.\n',
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
