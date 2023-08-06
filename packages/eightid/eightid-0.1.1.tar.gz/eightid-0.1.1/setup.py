# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['eightid']

package_data = \
{'': ['*']}

install_requires = \
['Django>=4.0.3,<5.0.0']

setup_kwargs = {
    'name': 'eightid',
    'version': '0.1.1',
    'description': 'A short id based on 8 bytes (it fits in a PostgreSQL BigInt).',
    'long_description': "EightID: A (really) short id, that fits in 8 bytes.\n===============\n\n[![Build Status](https://github.com/barrachri/gid/workflows/Test/badge.svg)](https://github.com/barrachri/eightid/actions)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/eightid.svg)](https://pypi.python.org/pypi/eightid)\n\n```EightID``` is a short ID that fits in 8 bytes. 4 bytes are dedicated to the timestamp (second resolution) and the other are 4 random bytes.\n\nIt's only 8 bytes and as such it fits in a BigInt column.\n\nInstallation\n------------\n\nInstallation using pip:\n\n    pip install eightid\n\nQuick intro\n-------------\n\n```python\n>>> from eightid import EightID\n>>> short_id = EightID()\n\n# Displays as base64 by default\n>>> short_id\n<EightID 'AH4jTMKtwrXCr8OQ'>\n>>> print(short_id)\nAH4jTMKtwrXCr8OQ\n>>> short_id.integer\n35504659304394704\n\n# Access when the id was created\n>>> short_id.datetime\ndatetime.datetime(2022, 4, 6, 17, 16, 12)\n\n# Access with str() and .string\n>>> str(short_id)\n'AH4jTMKtwrXCr8OQ'\n>>> short_id.string\n'AH4jTMKtwrXCr8OQ'\n\n# Recreate the EightID from a string\n>>> EightID.from_string(short_id.string)\n<EightID 'AH4jTMKtwrXCr8OQ'>\n\n# Or from\n>>> EightID.from_int(short_id.integer)\n<EightID 'AH4jTMKtwrXCr8OQ'>\n```\n\nDjango integration\n-------------\n\n```python\nfrom eightid import django\n\n\nclass AppModel(models.Model):\n    id = django.EightIDField(primary_key=True)\n```\n\nLicense\n-------\n\nEightID is licensed under the MIT license (see the ```LICENSE``` file for details).\n",
    'author': 'Christian Barra',
    'author_email': 'me@christianbarra.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/barrachri/eightid',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
