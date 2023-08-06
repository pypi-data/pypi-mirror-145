# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['plz', 'plz.schema']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=3.0', 'colorama>=0.4.0']

extras_require = \
{':python_version < "3.7"': ['jsonschema>=3.2.0,<4.0.0'],
 ':python_version >= "3.7"': ['jsonschema>=4.2.0']}

entry_points = \
{'console_scripts': ['plz = plz.main:main']}

setup_kwargs = {
    'name': 'plz-cmd',
    'version': '1.2.1',
    'description': 'command line app for running configurable shell commands',
    'long_description': "## plz-cmd\n\n[![Build Status](https://github.com/m3brown/plz/actions/workflows/python-app.yml/badge.svg)](https://github.com/m3brown/plz/actions?query=workflow%3Abuild)\n[![Coverage Status](https://coveralls.io/repos/github/m3brown/plz/badge.svg?branch=master)](https://coveralls.io/github/m3brown/plz?branch=master)\n\nA shell command to execute standard/repeatable commands in a git repo\n\n### Installation\n\nInstall plz at the system level so that it only has to be installed once.\n\n```bash\npip install plz-cmd\n\n# sudo may be required on your machine\nsudo pip install plz-cmd\n```\n\nIt can also be installed inside a virtualenv.  However, this means you'll have\nto install plz-cmd for each each virtualenv in use.\n\n```bash\nvirtualenv venv\n. venv/bin/activate\n\npip install plz-cmd\n```\n\n### Example\n\nplz looks for a `plz.yaml` file either in the current directory or in the root\nof the git repo you're currently in. This file can (and should) be checked into\nversion control.\n\nFor a plz.yaml file located in the git root directory, commands run will be\nexecuted relative to that directory, not the current directory.\n\nSuppose we have the following `plz.yaml` file:\n\n```yaml\ncommands:\n  # String command\n  run: ./manage.py runserver\n  # Array of command\n  test:\n    - ./manage.py test\n    - yarn test\n  # Object command, which supports string and array `cmd`\n  setup:\n    description: Set up the development environment\n    cmd:\n    - poetry install\n    - poetry run ./manage.py migrate\n    - yarn install\n  # ls example is referenced further down in this README\n  ls: ls\n```\n\nThe following commands would be available:\n\n```bash\nplz run\nplz test\nplz setup\nplz ls\n```\n\n### Getting help\n\nList all the available commands with:\n\n```bash\nplz\n# or\nplz help\n```\n\nPrint the yaml schema for any defined command with `plz help <command>`:\n\n```\n> plz help test\n[INFO] Using config: plz.yaml\n\ntest:\n  cmd:\n  - poetry run python -m pytest\n```\n\n### Description\n\nSetting a description attribute for a command will display the description in the\nconsole output. This can be useful if the command is not self explanatory.\n\n```yaml\ncommands:\n  echo:\n    cmd: echo hello\n    description: This is a sample description\n```\n\n```\n> plz echo\n\n[INFO] Using config: plz.yaml\n\nDescription: This is a sample description\n\n===============================================================================\nRunning command: echo hello\n===============================================================================\n\nhello\n```\n\n### Environment variables\n\nEnvironment variables can be set for an individual command or globally for all commands.\n\n```yaml\n# env variable for an individual command\ncommands:\n  test:\n    cmd: ./manage.py test\n    env:\n      DJANGO_SETTINGS_MODULE: myapp.settings.test\n```\n\n```yaml\nglobal_env:\n  DJANGO_SETTINGS_MODULE: myapp.settings.test\ncommands:\n  test: ./manage.py test\n```\n\n### Shortcuts\n\nSimilar to environment variables, shortcuts can be created witin the plz.yaml\nfile for reference by individual commands.\n\n```yaml\nshortcuts:\n  dc: docker-compose\n  commands:\n    start:\n      cmd: ${dc} up\n    shell:\n      cmd: ${dc} run web bash\n```\n\n### Globbing\n\nplz supports asterisk expansion.  For example, the cmd `ls *.py` will work as expected.\n\n### Runtime arguments\n\nplz supports passing custom arguments when running the plz command. For example:\n\n```\n# bind to port 8001 instead of the default 8000\nplz run 127.0.0.1:8001\n```\n\nAny passed arguments will be tested to see if they are file paths relative to\nthe current directory when running the command. Using this repo as an example:\n\n```\nbash$ ls .*.yaml\nplz.yaml               .pre-commit-config.yaml\n\nbash$ cd plz\n\nbash$ plz ls ../.*.yaml\n\n[INFO] Using config: /path/plz/plz.yaml\n\n===============================================================================\nRunning command: ls\n===============================================================================\n\nplz.yaml\n.pre-commit-config.yaml\n\n[INFO] Process complete, return code: 0\n\nbash$ plz ls __*.py\n\n[INFO] Using config: /path/plz/plz.yaml\n\n===============================================================================\nRunning command: ls\n===============================================================================\n\nplz/__init__.py\n\n[INFO] Process complete, return code: 0\n```\n\n### Development\n\nSetting up for development is easy when plz is already installed!\n\n```\ngit clone https://github.com/m3brown/plz\ncd plz\nplz setup\nplz test\n```\n",
    'author': 'Mike Brown',
    'author_email': 'mike.brown@excella.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/m3brown/plz',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
