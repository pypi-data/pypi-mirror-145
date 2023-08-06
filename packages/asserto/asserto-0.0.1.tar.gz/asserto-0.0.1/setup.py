# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asserto', 'asserto.mixins']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'asserto',
    'version': '0.0.1',
    'description': 'A fluent DSL for python assertions.',
    'long_description': '![Asserto](.github/images/logo.png)\n\n# Todo: Badges\n\n### Asserto\n\nPython assertions made fluent and easy.\n\n    - Chained and fluent assertions.\n    - Soft & Hard assertions.\n    - Rich diffs for easily identifying mistakes quickly.\n    - Extensibility, add your own easily.\n    - More...\n\nAsserto is current in its early development stages; contributions are extremely welcome!\nCheck out our `CONTRIBUTING.md` to get started.\n',
    'author': 'symonk',
    'author_email': 'jackofspaces@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
