# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clagiordano', 'clagiordano.python3_logger']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'clagiordano.python3-logger',
    'version': '1.0.0',
    'description': 'Library for logging facility',
    'long_description': '# Overview\n\nIt is an utility library which allow you to use a common interface accross all its component\nto log messages with different levels.\n\n## Logging levels\n\nIt use the standard logging levels widely used on all systems:\n\n| # | Levels |\n|---|---|\n| 0 | EMERGENCY |\n| 1 | ALERT |\n| 2 | CRITICAL |\n| 3 | ERROR |\n| 4 | WARNING |\n| 5 | NOTICE |\n| 6 | INFO |\n| 7 | DEBUG |\n\n## Installation\n\nTODO\n\n## Logging components\n\n| Type | Status | Description |\n|---|---|---|\n| [CLILogger](#cli-logger) | Available | It outputs logging messsages to STDOUT |\n| FileLogger | Planned | It will outputs logging messages directly to file |\n\n### CLI Logger\n\nThis logging components allow you to outputs logging information and raises and exception from critical level and above.\n\n#### Usage\n\n```python\n# Import the dependency\nfrom clagiordano.python3_logger.CLILogger import CLILogger\n\n# Init the component\nlogger = CLILogger()\n\n# Use it to log something\nlogger.info("Sample info message")\nlogger.error("Sample error message")\nlogger.critical("Sample critical message")\n```\n\nAd default it uses ANSI colors but you can toggle the ansi flag but you can easily toggle off this feature using the following code:\n\n```python\nlogger.set_ansi(False)\n```\n\n#### Sample ANSI output (default)\n\n![Sample ANSI output](docs/clilogger_ansi.png)\n\n#### Sample ANSI OFF output\n\n![Sample ANSI OFF output](docs/clilogger_ansi_off.png)\n\n## Contributing\n\nPlease read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.\n\n## Versioning\n\nWe use [SemVer](http://semver.org/) for versioning. For the versions available, see the releases on this repository.\n\n## Authors\n\n* **Claudio Giordano** - *Initial work* - [clagiordano](https://github.com/clagiordano)\n\nSee also the list of [contributors](CONTRIBUTORS.md) who participated in this project.\n',
    'author': 'Claudio Giordano',
    'author_email': 'claudio.giordano@autistici.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/clagiordano/python3-logger',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
