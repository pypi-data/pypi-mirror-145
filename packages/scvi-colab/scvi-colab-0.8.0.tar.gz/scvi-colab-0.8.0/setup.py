# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scvi_colab']

package_data = \
{'': ['*']}

install_requires = \
['rich==10.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0'],
 'dev': ['black>=22.1',
         'codecov>=2.0.8',
         'flake8>=3.7.7',
         'isort>=5.7',
         'pre-commit>=2.7.1',
         'pytest>=4.4']}

setup_kwargs = {
    'name': 'scvi-colab',
    'version': '0.8.0',
    'description': 'Lightweight helper to install scvi-tools in Google Colab.',
    'long_description': '# scvi-colab\n\n```\n!pip install scvi-colab\n\nfrom scvi_colab import install\n\n# default\ninstall()\n\n# from a GitHub branch\ninstall(branch="0.14.x")\n\n# A specific PyPI version\ninstall(version="0.15.1")\n',
    'author': 'The scvi-tools development team',
    'author_email': 'adamgayoso@berkeley.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/scverse/scvi-colab',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
