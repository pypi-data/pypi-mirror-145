# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wordlebee']

package_data = \
{'': ['*'], 'wordlebee': ['data/*']}

install_requires = \
['numpy>=1.22.3,<2.0.0', 'rich>=12.0.1,<13.0.0']

entry_points = \
{'console_scripts': ['wordlebee = wordlebee.__main__:cli'],
 'pipx.run': ['wordlebee = wordlebee.__main__:cli']}

setup_kwargs = {
    'name': 'wordlebee',
    'version': '0.7.4',
    'description': 'wordle word guessing helper bee',
    'long_description': '<div align="center">\n\n<h1>\n    <img width="500" align="center" src="https://raw.githubusercontent.com/lento234/wordlebee/main/assets/wordlebee-logo.svg">\n</h1>\n\n[![PyPi Version](https://img.shields.io/pypi/v/wordlebee.svg?style=flat-square&labelColor=000000)](https://pypi.org/project/wordlebee/)\n[![PyPi Python versions](https://img.shields.io/pypi/pyversions/wordlebee.svg?style=flat-square&labelColor=000000)](https://pypi.org/project/wordlebee/)\n![License](https://img.shields.io/github/license/lento234/wordlebee?style=flat-square&color=blue&labelColor=000000)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square&labelColor=000000)](#black)\n[![Downloads](https://static.pepy.tech/personalized-badge/wordlebee?period=total&units=international_system&left_color=black&right_color=blue&left_text=Downloads)](https://pepy.tech/project/wordlebee)\n\n***A cli wordle word guessing helper bee to solve the wordle puzzle of the day.***\n\n</div>\n\n## Usage\n\n```\npython -m wordlebee\n```\n\n## Installation\n\nInstall `wordlebee` in isolated environment:\n\n```\npipx install wordlebee\n```\n\nInstall `wordlebee`:\n\n```\npip install wordlebee\n```\n\n## Development\n\nInstall conda enviroment:\n\n```\nconda env create -f environment.yml\n```\n\nInstall using `poetry`:\n\n```\npoetry install\n```\n',
    'author': 'Mrlento234',
    'author_email': 'lento.manickathan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
