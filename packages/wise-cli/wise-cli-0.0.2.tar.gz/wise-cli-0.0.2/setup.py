# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src', 'src.commands', 'tests']

package_data = \
{'': ['*'], 'src': ['templates/*']}

install_requires = \
['Jinja2>=3.1.1,<4.0.0', 'click==8.1.2', 'fabric', 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['wise = src.cli:main']}

setup_kwargs = {
    'name': 'wise-cli',
    'version': '0.0.2',
    'description': 'Django deployments CLI.',
    'long_description': '# Wise CLI\n\n\n`wise` is a tool to deploy `Django` projects based on [django-wise template](https://github.com/victoraguilarc/django-wise)\n\n## Installation\n\n\n#### Stable Version\n```bash\npip install wise-cli\n```\n\n#### Development Version\n```bash\npip install git+https://github.com/victoraguilarc/wise-cli.git\n```\n\n## Usage\n\n- Clone wise Django template\n```\ngit clone https://github.com/victoraguilarc/wise.git\n```\n\n- **Configure Project**. The project must have a folder called `.envs` for environment variables por development and a file `.env` for production with virtualenv deployment mode.\n\n- Add config file to cloned project.\n\nBy default *wise* uses *django.json*, This file could contains configuration values, for example::\n\n    {\n        "deployment": "virtualenv",\n        "project": "wise",\n        "password": "CHANGE_THIS!!",\n        "domain": "www.xiberty.com",\n        "ipv4": "0.0.0.0",\n        "db_engine": "postgres",\n        "web_server": "nginx",\n        "https": true,\n        "superuser": "username",\n        "sshkey": "/Users/username/.ssh/id_rsa.pub"\n    }\n\n\n## Development\n```bash\npip install poetry\npoetry install\npip install -e .\n```\n\n## License\n\nThis code is licensed under the `MIT License`.\n\n.. _`MIT License`: https://github.com/victoraguilarc/suarm/blob/master/LICENSE\n\n\n\n',
    'author': 'Victor Aguilar C.',
    'author_email': 'vicobits@gmail.com',
    'maintainer': 'Victor Aguilar C.',
    'maintainer_email': 'vicobits@gmail.com',
    'url': 'https://github.com/victoraguilarc/wise-cli/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
