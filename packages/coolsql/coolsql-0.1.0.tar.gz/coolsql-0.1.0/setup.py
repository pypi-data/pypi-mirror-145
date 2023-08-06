# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coolsql']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'coolsql',
    'version': '0.1.0',
    'description': 'Makes it easier to write raw SQL in Python.',
    'long_description': '# CoolSQL\n\n![PyPI](https://img.shields.io/pypi/v/coolsql?style=flat-square)\n\nMakes it easier to write raw SQL in Python.\n\n## Usage\n\n### Quick Start\n\n```python\nfrom coolsql import Field\n\nname = Field("name")\n\ncondition = name.isnull() & field_age.between(18, 24)\n...\ncursor.execute(f"SELECT * FROM table WHERE {condition}", condition.p())\n...\n```\n',
    'author': 'abersheeran',
    'author_email': 'me@abersheeran.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abersheeran/coolsql',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
