# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['guard_exception']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'guard-exception',
    'version': '1.0.0',
    'description': 'Catch fatal errors or any type of error, used to easily normalize executions in swift calls with PythonKit',
    'long_description': '# guard_exception\n    - guard all exception for swift run python\n\n## install\n    - pip install guard-exception\n\n\n## example\n```python\nimport guard_exception as ge\n\ngg = ge.guard_exception()\n\n\ndef dividir(a, b):\n    return a / b\n\n\nprint(gg.guardException(dividir, a=1, b=0))\n\n\n# result cli\n# {\'data:\': None, \'error\': \'division by zero\'}\n\n```\n\n\n## example on swift with PythonKit\n```swift\nimport PythonKit\nlet hvac = Python.import("hvac")\nlet ge = Python.import("guard_exception")\nlet gg = ge.guard_exception()\n\nlet client = hvac.Client(url: "http://0.0.0.0:8200")\n\nlet user = "incorrect_user"\nlet params = Python.dict()\nparams["username"] = PythonObject(user)\nparams["password"] = PythonObject("incorrect_password")\n\nprint(gg.guardException(client.login, url: "v1/auth/userpass/login/\\(user)", use_token: true, json: params))\n\n// result: cli\n//{\'data:\': None, \'error\': \'invalid username or password, on post http://0.0.0.0:8200/v1/auth/userpass/login/incorrect_user\'}\n```',
    'author': 'Rafael Fernando Garcia Sagastume',
    'author_email': 'rafael.garcia@ciberc.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
