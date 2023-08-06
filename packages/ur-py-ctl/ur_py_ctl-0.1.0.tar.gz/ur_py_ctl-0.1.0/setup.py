# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ur_py_ctl']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ur-py-ctl',
    'version': '0.1.0',
    'description': 'Python wrapper around URScript (for Universal Robotics robots).',
    'long_description': None,
    'author': 'Anton Tetov',
    'author_email': 'anton.johansson@control.lth.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.control.lth.se/robotlab/ur_py_ctl',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
