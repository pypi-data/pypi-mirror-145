# Advent-of-code-py
[Advent of Code][advent_of_code_link] helper CLI and library for python projects.

**Status & Info:**

| Code style | License | Project Version |
| :---: | :---: | :---: |
| [![Code style][black_badge]][black_link] | [![License: MIT][license_badge]][license_link] | [![PyPI][project_badge]][project_link] |

## Usage

### Installation
To install advent-of-code-py run following command which installs advent-of-code-py CLI and advent_of_code_py library.
```bash
pip install advent-of-code-py
```

__OR__

```bash
poetry add advent-of-code-py
```

### Usage
Initially for advent-of-code-py to work it need session value or session ID which you can obtain by viewing cookie while visiting advent of code server.
After collecting session cookie value you need to add those values in config using advent-of-code-py CLI
```bash
advent-of-code-py config add <session-name> <session-value>
```

Now you can import library by using
```python
import advent_of_code_py
```

After importing a library you can use either two decorator present which are solve and submit decorator for a function of puzzle

For example:-
```python
@advent_of_code_py.submit(2018,3,1,session_list="<session-name>")
def puzzle_2018_3_1(data=None):
    # do some calculation with data and return final output
    return final_output
```

Now after decorating function now you can call function like regular function call
```python
puzzle_2018_3_1()
```
After calling function `final_output` value will be submitted by library to Advent of Code server for 2018 year day 3
problem, then returns whether the submitted answer was correct or not. If session value is not provided then
the solution will be submitted to all session value present in config file.

You can also use advent-of-code-py builtin Initializer and runner to create appropriate CLI for problem so
problem can be run from CLI instead of modifying python file every time to run appropriate function
To set advent-of-code-py puzzle as CLI
```python
@advent_of_code_py.advent_runner()
def main_cli():
    initializer = advent_of_code_py.Initializer()
    initializer.add(<function_alias>=<function>)
    # for example to run above function you can write
    initializer.add(p_3_1=puzzle_2018_3_1)
    # add other functions ...
    return initializer
```
Now you can set main_cli as entry points, and it will create CLI with the appropriate name and function which was added.
So for example to run function puzzle_2018_3_1() you have to run command as `entry-point-name run p_3_1` which
will run the appropriate function as well as submit as desired if the function was decorated by submit decorator or else
prints its output if the function was decorated by solve decorator.

[advent_of_code_link]: https://adventofcode.com

[black_badge]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
[black_link]: https://github.com/ambv/black

[license_badge]: https://img.shields.io/github/license/iamsauravsharma/advent-of-code-py.svg?style=for-the-badge
[license_link]: LICENSE

[project_badge]: https://img.shields.io/pypi/v/advent-of-code-py?style=for-the-badge&color=blue&logo=python
[project_link]: https://pypi.org/project/advent-of-code-py
