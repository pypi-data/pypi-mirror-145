# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pwdsafe']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'pwdsafe',
    'version': '1.0.0',
    'description': 'Python package to check if a given password is safe to use.',
    'long_description': '<div align="center">\n  <h2>pwdsafe</h2>\n</div>\n\nPython package to check if a given password is safe to use.\n\npwdsafe is a thin wrapper around [have i been pwned](https://haveibeenpwned.com/) that checks if a given password is compromised.\n\n### Install\n\n```sh\npip install pwdsafe\n```\n\n### Usage\n\n```python\nfrom pwdsafe import is_safe\n\nis_pwd_safe = is_safe("password")\n```\n',
    'author': 'Arun Nalla',
    'author_email': 'hello@arunnalla.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/arunnalla/pwdsafe/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
