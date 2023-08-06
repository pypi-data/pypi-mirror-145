# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyemer']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyemer',
    'version': '0.1.0',
    'description': 'Python API for Emercoin blockchain.',
    'long_description': '# PyEmer\nPython API for Emercoin blockchain.\n\n## Usage\n\n```python\nfrom pyemer import Emer\n\n# Emer(user, password, host, port)\nemer = Emer("emccoinrpc", "emcpassword")\n\nemer.name_show("dns:flibusta.lib").record.value\nemer.name_new("some:name", "some value", 365)\nemer.name_new("some:name2", b"byte value", 365, emer.get_account_address())\nemer.name_history("some:name")[0].tx.height\nemer.get_names_by_type("dns")[0].record.name\nemer.get_block_count()\n\n# You can call RPC manually\nemer.rpc_connection.signmessage(\n    emer.rpc_connection.getaccountaddress(""),\n    "some message"\n)\n```\n',
    'author': 'Vasiliy Petrov',
    'author_email': 'cofob@riseup.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fire-squad/PyEmer',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
