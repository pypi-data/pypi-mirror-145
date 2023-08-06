# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['annorepo']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['version = poetry_scripts:version']}

setup_kwargs = {
    'name': 'annorepo-client',
    'version': '0.1.2a0',
    'description': 'A Python client for accessing an AnnoRepo server',
    'long_description': '# annorepo-client\n\nA Python client for accessing an [AnnoRepo](https://github.com/brambg/annorepo) server\n\n## installing\n\n### using poetry\n\n```\npoetry add annorepo-client\n```\n\n### using pip\n\n```\npip install annorepo-client\n```\n\n\n\n## contributing\n\nSee [CONTRIBUTING](CONTRIBUTING.md)',
    'author': 'Bram Buitendijk',
    'author_email': 'bram.buitendijk@di.huc.knaw.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/brambg/annorepo-python-client',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
