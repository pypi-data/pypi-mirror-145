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
    'version': '2022.1.1',
    'description': 'Python project with teaching and scientific projects for Transformer Design and Optimization.',
    'long_description': '# TrafoCalc\n\n[![Build](https://github.com/tamasorosz/TrafoCalc/actions/workflows/ci.yml/badge.svg)](https://github.com/tamasorosz/TrafoCalc/actions/workflows/ci.yml)\n[![codecov](https://codecov.io/gh/tamasorosz/TrafoCalc/branch/master/graph/badge.svg?token=6SBI4COCOQ)](https://codecov.io/gh/tamasorosz/TrafoCalc)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/tamasorosz/TrafoCalc.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/tamasorosz/TrafoCalc/context:python)\n[![Total alerts](https://img.shields.io/lgtm/alerts/g/tamasorosz/TrafoCalc.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/tamasorosz/TrafoCalc/alerts/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)\n\n## Goal of the Project\n\nDesign and Optimization of a power transformer needs to handle and calculate many required technical parameters\nsimoultanously, while the econoimically or technically optimal design was searched. This python package contains the\nimplementations of many analytical functions, which can be used to calculate the geometrical, electrical, mechanical or\nthermal properties of three-phased power transformers.\n\nThe tool uses the implementation of a simple two-winding model calculations for the calculation of the transformer\nparameters. Beside the analytical formulas, this project contains a 2D axisymmetric, parametric FEM simulation for\ncalculation of the short circuit impedance of a power transformer. The proposed methodology can be useful to understand\nthe principles of transformer design, or transformer professionals. Because, all of the proposed calculations validated\nby measurements.\n\n## Quickstart\n\nThe `\\notes` library contains many sample designs in jupyter notebooks, which can be a good starting point to use this\npackage.\n\n## References\n\n[1] `Orosz, T., Borbély, B., Tamus, Z. Ádám  \nPerformance Comparison of Multi Design Method and Meta-Heuristic Methods for Optimal Preliminary Design of Core-Form Power Transformers , Periodica Polytechnica Electrical Engineering and Computer Science, 61(1), pp. 69–76, 2017. https://doi.org/10.3311/PPee.10207`\n',
    'author': 'Tamás Orosz',
    'author_email': 'orosz.tamas@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tamasorosz/TrafoCalc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.8.10',
}


setup(**setup_kwargs)
