# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neurogenome']

package_data = \
{'': ['*']}

install_requires = \
['h5py==2.10', 'numpy==1.18.1']

setup_kwargs = {
    'name': 'neurogenome',
    'version': '0.1.2',
    'description': 'A universal API for create artificial neural networks with a genetic code.',
    'long_description': '<img src="https://raw.githubusercontent.com/Aiyyskhan/NeuroGenome/main/docs/NeuroGenome_1_1_white.jpeg" align="middle" width="1000"/>\n\n<p align="center">\n<img src="https://img.shields.io/badge/version-v0.1.2-blue.svg?style=flat&colorA=007D8A&colorB=E1523D">\n<img src="https://img.shields.io/badge/license-MIT-brightgreen">\n</p>\n\n**NeuroGenome** is a bioinspired open-source project that allows you to create artificial neural networks with a genetic code.\n\n- [Installation](#installation)\n- [Settings example](#settings-example)\n- [Examples](#examples)\n- [License](#license)\n\n## Installation\n```python\npip install neurogenome\n```\n## Settings example\n\n```python\n# gene localization scheme\nschema_0 = [\n\t[\n\t\t["i0","i1","i0","i1"],\n\t\t["h1","h0","h1","h0"]\n\t],\n\t[\n\t\t["i2","i3","i2","i3"],\n\t\t["h3","h2","h3","h2"]\n\t],\n\t[\n\t\t["o0","o1"],\n\t\t["o1","o0"]\n\t]\n]\n\n# hyperparameters\nSETTINGS = {\n\t"population size": 50,\n\t"number of leaders": 5,\n\t"select by": "max",\n\t"number of input nodes per gene": 5,\n\t"number of hidden nodes per gene": 4,\n\t"number of output nodes per gene": 3,\n\t"schema": schema_0,\n}\n```\n\n## Examples\n\n_in the pipeline_\n\n## License\n\n[MIT](https://opensource.org/licenses/MIT)',
    'author': 'Aiyyskhan Alekseev',
    'author_email': 'aiyykhan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Aiyyskhan/NeuroGenome',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
