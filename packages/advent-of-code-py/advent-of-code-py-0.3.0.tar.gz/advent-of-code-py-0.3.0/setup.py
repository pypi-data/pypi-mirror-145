# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['advent_of_code_py']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'click>=8.0,<9.0',
 'python-dateutil>=2.8.0,<3.0.0',
 'requests>=2.22.0,<3.0.0']

entry_points = \
{'console_scripts': ['advent-of-code-py = advent_of_code_py.cli:main']}

setup_kwargs = {
    'name': 'advent-of-code-py',
    'version': '0.3.0',
    'description': 'Advent of Code helper CLI and library',
    'long_description': '# Advent-of-code-py\n[Advent of Code][advent_of_code_link] helper CLI and library for python projects.\n\n**Status & Info:**\n\n| Code style | License | Project Version |\n| :---: | :---: | :---: |\n| [![Code style][black_badge]][black_link] | [![License: MIT][license_badge]][license_link] | [![PyPI][project_badge]][project_link] |\n\n## Usage\n\n### Installation\nTo install advent-of-code-py run following command which installs advent-of-code-py CLI and advent_of_code_py library.\n```bash\npip install advent-of-code-py\n```\n\n__OR__\n\n```bash\npoetry add advent-of-code-py\n```\n\n### Usage\nInitially for advent-of-code-py to work it need session value or session ID which you can obtain by viewing cookie while visiting advent of code server.\nAfter collecting session cookie value you need to add those values in config using advent-of-code-py CLI\n```bash\nadvent-of-code-py config add <session-name> <session-value>\n```\n\nNow you can import library by using\n```python\nimport advent_of_code_py\n```\n\nAfter importing a library you can use either two decorator present which are solve and submit decorator for a function of puzzle\n\nFor example:-\n```python\n@advent_of_code_py.submit(2018,3,1,session_list="<session-name>")\ndef puzzle_2018_3_1(data=None):\n    # do some calculation with data and return final output\n    return final_output\n```\n\nNow after decorating function now you can call function like regular function call\n```python\npuzzle_2018_3_1()\n```\nAfter calling function `final_output` value will be submitted by library to Advent of Code server for 2018 year day 3\nproblem, then returns whether the submitted answer was correct or not. If session value is not provided then\nthe solution will be submitted to all session value present in config file.\n\nYou can also use advent-of-code-py builtin Initializer and runner to create appropriate CLI for problem so\nproblem can be run from CLI instead of modifying python file every time to run appropriate function\nTo set advent-of-code-py puzzle as CLI\n```python\n@advent_of_code_py.advent_runner()\ndef main_cli():\n    initializer = advent_of_code_py.Initializer()\n    initializer.add(<function_alias>=<function>)\n    # for example to run above function you can write\n    initializer.add(p_3_1=puzzle_2018_3_1)\n    # add other functions ...\n    return initializer\n```\nNow you can set main_cli as entry points, and it will create CLI with the appropriate name and function which was added.\nSo for example to run function puzzle_2018_3_1() you have to run command as `entry-point-name run p_3_1` which\nwill run the appropriate function as well as submit as desired if the function was decorated by submit decorator or else\nprints its output if the function was decorated by solve decorator.\n\n[advent_of_code_link]: https://adventofcode.com\n\n[black_badge]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge\n[black_link]: https://github.com/ambv/black\n\n[license_badge]: https://img.shields.io/github/license/iamsauravsharma/advent-of-code-py.svg?style=for-the-badge\n[license_link]: LICENSE\n\n[project_badge]: https://img.shields.io/pypi/v/advent-of-code-py?style=for-the-badge&color=blue&logo=python\n[project_link]: https://pypi.org/project/advent-of-code-py\n',
    'author': 'Saurav Sharma',
    'author_email': 'appdroiddeveloper@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/iamsauravsharma/advent-of-code-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
