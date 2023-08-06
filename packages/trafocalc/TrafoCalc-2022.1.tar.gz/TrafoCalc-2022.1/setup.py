# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src']

package_data = \
{'': ['*']}

install_requires = \
['altair-saver>=0.5.0,<0.6.0',
 'altair>=4.2.0,<5.0.0',
 'bokeh>=2.4.2,<3.0.0',
 'dataclasses-json>=0.5.6,<0.6.0',
 'importlib-resources>=5.4.0,<6.0.0',
 'jupyter>=1.0.0,<2.0.0',
 'marshmallow-dataclass>=8.5.3,<9.0.0',
 'scipy>=1.8.0,<2.0.0',
 'seaborn>=0.11.2,<0.12.0',
 'typer']

setup_kwargs = {
    'name': 'trafocalc',
    'version': '2022.1',
    'description': 'Python project with teaching and scientific projects for Transformer Design and Optimization.',
    'long_description': None,
    'author': 'Tamás Orosz',
    'author_email': 'orosz.tamas@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.8.10',
}


setup(**setup_kwargs)
