# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pupil', 'pupil.db', 'pupil.models', 'pupil.sampling']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'faiss-cpu>=1.7.2,<2.0.0',
 'ipywidgets>=7.7.0,<8.0.0',
 'marshmallow-dataclass>=8.5.3,<9.0.0',
 'nptyping>=1.4.4,<2.0.0',
 'numpy>=1.22.2,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'pytest>=7.0.1,<8.0.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'typeguard>=2.13.3,<3.0.0']

extras_require = \
{'docs': ['myst-parser>=0.17.0,<0.18.0']}

setup_kwargs = {
    'name': 'pupil',
    'version': '0.2.0',
    'description': 'Active learning platform',
    'long_description': None,
    'author': 'hadi-gharibi',
    'author_email': 'hady.gharibi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
