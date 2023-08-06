# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyimg4']

package_data = \
{'': ['*']}

install_requires = \
['asn1>=2.5.0,<3.0.0',
 'lzss>=0.3,<0.4',
 'pycryptodome>=3.14.1,<4.0.0',
 'pyliblzfse>=0.4.1,<0.5.0']

setup_kwargs = {
    'name': 'pyimg4',
    'version': '0.3',
    'description': "A Python library/CLI tool for parsing Apple's IMG4 format.",
    'long_description': '<p align="center">\n<img src=".github/assets/icon.png" alt="https://github.com/m1stadev/PyIMG4" width=256px> \n</p>\n\n<h1 align="center">\nPyIMG4\n</h1>\n<p align="center">\n  <a href="https://github.com/m1stadev/PyIMG4/blob/master/LICENSE">\n    <image src="https://img.shields.io/github/license/m1stadev/PyIMG4">\n  </a>\n  <a href="https://github.com/m1stadev/PyIMG4/stargazers">\n    <image src="https://img.shields.io/github/stars/m1stadev/PyIMG4">\n  </a>\n  <a href="https://github.com/m1stadev/PyIMG4">\n    <image src="https://img.shields.io/tokei/lines/github/m1stadev/PyIMG4">\n  </a>\n    <br>\n</p>\n\n<p align="center">\nA Python library/CLI tool for parsing Apple\'s <a href="https://www.theiphonewiki.com/wiki/IMG4_File_Format">IMG4 format</a>.\n</p>\n\n## Requirements\n- Python 3.9 or higher\n\n## Installation\n- Install from [PyPI](https://pypi.org/project/pyimg4/):\n    - ```python3 -m pip install -U pyimg4```\n- Local installation:\n    - `./install.sh`\n    - Requires [Poetry](https://python-poetry.org)\n\n## TODO\n- Implement IMG4 creation\n- Write CLI tool\n\n## Support\n\nFor any questions/issues you have, [open an issue](https://github.com/m1stadev/PyIMG4/issues) or join my [Discord](https://m1sta.xyz/discord).\n',
    'author': 'm1stadev',
    'author_email': 'adamhamdi31@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/m1stadev/PyIMG4',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
