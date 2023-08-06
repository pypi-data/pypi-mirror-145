# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['guard_exception']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'guard-exception',
    'version': '0.1.4',
    'description': 'Catch fatal errors or any type of error, used to easily normalize executions in swift calls with PythonKit',
    'long_description': '# guard_exception\n    - guard all exception for swift run python',
    'author': 'Rafael Garcia Sagastume',
    'author_email': 'rafael.garcia@ciberc.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
