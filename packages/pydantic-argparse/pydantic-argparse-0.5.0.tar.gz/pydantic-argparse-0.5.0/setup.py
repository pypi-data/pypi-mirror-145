# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_argparse',
 'pydantic_argparse.argparse',
 'pydantic_argparse.parsers',
 'pydantic_argparse.utils']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'pydantic-argparse',
    'version': '0.5.0',
    'description': 'Typed Argument Parsing with Pydantic',
    'long_description': '<div align="center">\n    <h1>\n        Pydantic Argparse\n    </h1>\n    <p>\n        <em>Typed Argument Parsing with Pydantic</em>\n    </p>\n    <a href="https://pypi.python.org/pypi/pydantic-argparse">\n        <img src="https://img.shields.io/pypi/v/pydantic-argparse.svg">\n    </a>\n    <a href="https://pepy.tech/project/pydantic-argparse">\n        <img src="https://pepy.tech/badge/pydantic-argparse">\n    </a>\n    <a href="https://github.com/SupImDos/pydantic-argparse">\n        <img src="https://img.shields.io/pypi/pyversions/pydantic-argparse.svg">\n    </a>\n    <a href="https://github.com/SupImDos/pydantic-argparse/blob/master/LICENSE">\n        <img src="https://img.shields.io/github/license/SupImDos/pydantic-argparse.svg">\n    </a>\n</div>\n\n## Help\nSee [documentation](https://pydantic-argparse.supimdos.com) for help.\n\n## Installation\nInstallation with `pip` is simple:\n```console\n$ pip install pydantic-argparse\n```\n\n## Example\n```py\nimport pydantic\nimport pydantic_argparse\n\n\nclass Arguments(pydantic.BaseModel):\n    # Required Args\n    string: str = pydantic.Field(description="a required string")\n    integer: int = pydantic.Field(description="a required integer")\n    flag: bool = pydantic.Field(description="a required flag")\n\n    # Optional Args\n    second_flag: bool = pydantic.Field(False, description="an optional flag")\n    third_flag: bool = pydantic.Field(True, description="an optional flag")\n\n\ndef main() -> None:\n    # Create Parser and Parse Args\n    parser = pydantic_argparse.ArgumentParser(\n        model=Arguments,\n        prog="Example Program",\n        description="Example Description",\n        version="0.0.1",\n        epilog="Example Epilog",\n    )\n    args = parser.parse_typed_args()\n\n    # Print Args\n    print(args)\n\n\nif __name__ == "__main__":\n    main()\n```\n\n```console\n$ python3 example.py --help\nusage: Example Program [-h] [-v] --string STRING --integer INTEGER --flag |\n                       --no-flag [--second-flag] [--no-third-flag]\n\nExample Description\n\nrequired arguments:\n  --string STRING    a required string\n  --integer INTEGER  a required integer\n  --flag, --no-flag  a required flag\n\noptional arguments:\n  --second-flag      an optional flag (default: False)\n  --no-third-flag    an optional flag (default: True)\n\nhelp:\n  -h, --help         show this help message and exit\n  -v, --version      show program\'s version number and exit\n\nExample Epilog\n```\n\n```console\n$ python3 example.py --string hello --integer 42 --flag\nstring=\'hello\' integer=42 flag=True second_flag=False third_flag=True\n```\n\n## License\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Hayden Richards',
    'author_email': 'SupImDos@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pydantic-argparse.supimdos.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
