# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytest_markdown_docs']

package_data = \
{'': ['*']}

install_requires = \
['markdown-it-py>=1.1.0,<1.2.0']

entry_points = \
{'pytest11': ['pytest_markdown_docs = pytest_markdown_docs.plugin']}

setup_kwargs = {
    'name': 'pytest-markdown-docs',
    'version': '0.1.0',
    'description': 'Run markdown code fences through pytest',
    'long_description': None,
    'author': 'Modal Labs',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/modal-com/pytest-markdown-docs',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
