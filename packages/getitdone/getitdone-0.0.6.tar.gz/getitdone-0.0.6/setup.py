# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['getitdone']

package_data = \
{'': ['*']}

install_requires = \
['rich>=12.0.1,<13.0.0']

entry_points = \
{'console_scripts': ['getitdone = getitdone.getitdone:main',
                     'gid = getitdone.getitdone:main']}

setup_kwargs = {
    'name': 'getitdone',
    'version': '0.0.6',
    'description': 'Command line to-do list application',
    'long_description': '[![PyPI Version][pypi-image]][pypi-url]\n[![Black][black badge]][black]\n[![Flake8][flake8 badge]][flake8]\n[![Imports][isort badge]][isort]\n[![Tests Status][tests-image]][tests-url]\n[![Code Coverage][coverage-image]][coverage-url]\n[![Last Commit][commit badge]][commit]\n\n<!-- Links -->\n[pypi-url]: https://pypi.org/project/getitdone/\n[black]: https://github.com/psf/black\n[flake8]: https://github.com/PyCQA/flake8\n[isort]: https://pycqa.github.io/isort/\n[tests-url]: https://github.com/ryanleonbutler/getitdone/actions/workflows/tests.yml\n[coverage-url]: https://codecov.io/gh/ryanleonbutler/getitdone\n[commit]: https://github.com/ryanleonbutler/getitdone/commit/HEAD\n\n<!-- Badges -->\n[pypi-image]: https://img.shields.io/pypi/v/getitdone\n[black badge]: https://img.shields.io/badge/code%20style-black-000000.svg\n[flake8 badge]: https://github.com/ryanleonbutler/black_star/actions/workflows/lint.yml/badge.svg\n[isort badge]: https://img.shields.io/badge/%20imports-isort-%231674b1\n[tests-image]: https://github.com/ryanleonbutler/getitdone/actions/workflows/tests.yml/badge.svg\n[coverage-image]: https://codecov.io/gh/ryanleonbutler/getitdone/branch/main/graph/badge.svg?token=4CQG41WFF4\n[commit badge]: https://img.shields.io/github/last-commit/ryanleonbutler/getitdone\n\n\n# getitdone\n\n### About\n**getitdone** command line to-do list app... now let\'s make some lists!\n\nI was browsing on the Internet and wanted a really basic todo list application, which was free and opensource. Since I am in the process of learning more about software development I decided to create my own.\n\n\n### Installation\n```\n$ pip install getitdone\n```\n\n### Uninstall\n```\n$ pip uninstall getitdone\n```\n\n### Usage\n![](https://github.com/ryanleonbutler/getitdone/blob/master/images/image1.jpg?raw=true)\n\n\n\n### User Manual\n    OPTIONS\n        --new or -n \'<task-name>\'\n            Create a new task with name in first argument\n        --update or -u \'<task-name>\' \'<new-name>\'\n            Update task in first argument with value second argument\n        --delete or -d \'<task-name>\'\n            Delete task in first argument with value second argument\n        --list or -l\n            List all tasks\n        --help or -h\n            Shows man page for todolist\n\n### Report an issue\nCreate an issue on GitHub with as much supporting information and detail about the bug or issue as possible.\n\n### Contribute\nAnyone is welcome to contribute to the project. You can submit your pull request and the changes will be reviewed. When submitting changes, ensure your code is "Pythonic". Use only Stand Library modules. No module are allowed that need further installation.\n\n### License\nLicensing is AGPL.\n\n### Credits\nDuanne Mattheus - Thank you for providing the name for the application.\n',
    'author': 'Ryan Butler',
    'author_email': 'ryanleonbutler@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ryanleonbutler/getitdone',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
