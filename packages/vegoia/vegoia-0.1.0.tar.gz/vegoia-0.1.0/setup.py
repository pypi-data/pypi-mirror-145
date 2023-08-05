# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['vegoia']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.0,<4.0',
 'numpy>=1.21,<2.0',
 'scipy>=1.7.0,<2.0.0',
 'typing-extensions>=4.1.1,<5.0.0']

extras_require = \
{'beartype': ['beartype>=0.10.4,<0.11.0'],
 'docs': ['myst-nb>=0.13.2,<0.14.0',
          'sphinx==4.3.2',
          'sphinx-autodoc-typehints>=1.17.0,<2.0.0',
          'sphinx-book-theme>=0.2.0,<0.3.0']}

setup_kwargs = {
    'name': 'vegoia',
    'version': '0.1.0',
    'description': 'Python adaptive plotting library',
    'long_description': None,
    'author': 'Denis Rosset',
    'author_email': 'physics@denisrosset.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
