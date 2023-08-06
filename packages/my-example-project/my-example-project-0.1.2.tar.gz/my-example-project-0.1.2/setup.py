# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['my-example-project', 'my-example-project.my-example-project']

package_data = \
{'': ['*']}

install_requires = \
['poetry-version-plugin>=0.1.3,<0.2.0']

entry_points = \
{'poetry.plugin': ['poetry-version-plugin = '
                   'poetry_version_plugin.plugin:VersionPlugin']}

setup_kwargs = {
    'name': 'my-example-project',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Lingling',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
