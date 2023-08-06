# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '..'}

packages = \
['rob']

package_data = \
{'': ['*'], 'rob': ['config/*', 'dist/*']}

install_requires = \
['openai>=0.15.0,<0.16.0',
 'praw>=7.5.0,<8.0.0',
 'pydub>=0.25.1,<0.26.0',
 'pytaglib>=1.5.0,<2.0.0',
 'rich>=11.2.0,<12.0.0',
 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'robolson',
    'version': '0.3.52',
    'description': 'My collection of utilty scripts',
    'long_description': None,
    'author': 'Rob L Olson',
    'author_email': 'rob.louis@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
