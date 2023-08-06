# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['click_rich_help']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0,<9.0', 'rich>=10.0']

setup_kwargs = {
    'name': 'click-rich-help',
    'version': '22.1.1',
    'description': 'make a beautiful click app with rich',
    'long_description': '<div id="top"></div>\n\n<!-- PROJECT SHIELDS -->\n[![Forks][forks-shield]][forks-url]\n[![Stargazers][stars-shield]][stars-url]\n[![Issues][issues-shield]][issues-url]\n[![MIT License][license-shield]][license-url]\n[![CircleCI][circleci-shield]][circleci-url]\n\n<!-- PROJECT LOGO -->\n<br />\n<div align="center">\n  <a href="https://github.com/daylinmorgan/click-rich-help">\n    <img src="https://raw.githubusercontent.com/daylinmorgan/click-rich-help/main/assets/logo.png" alt="Logo" width=400 >\n  </a>\n\n<h2 align="center">click-rich-help</h2>\n\n  <p align="center">\n    make a beautiful click app with rich\n  </p>\n</div>\n\n\n<!-- TABLE OF CONTENTS -->\n<details>\n  <summary>Table of Contents</summary>\n  <ol>\n    <li>\n      <a href="#about-the-project">About The Project</a>\n      <ul>\n        <li><a href="#built-with">Built With</a></li>\n      </ul>\n    </li>\n    <li>\n      <a href="#getting-started">Getting Started</a>\n      <ul>\n        <li><a href="#installation">Installation</a></li>\n      </ul>\n    </li>\n    <li><a href="#usage">Usage</a></li>\n    <li><a href="#contributing">Contributing</a></li>\n    <li><a href="#acknowledgments">Acknowledgments</a></li>\n  </ol>\n</details>\n\n\n## About The Project\n\nI wanted a simple python package to make my click app\'s help more readable.\n\nSince writing this package the more opinionated [rich-click](https://github.com/ewels/rich-click) has been written.\nIf that output is more your speed, go check it out! This project aims to provide a slightly different API and set of features.\n\n![screenshot](https://github.com/daylinmorgan/click-rich-help/blob/main/assets/screenshots/base.png)\n\n## Getting Started\n\n### Installation\n\nwith pip:\n``` bash\npip install click-rich-help\n```\nwith conda/mamba:\n```bash\nconda install -c conda-forge click-rich-help\n```\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n## Usage\n\nAs of `v22.1.0` you may no longer generate styles using named args.\n\nAt a minimum you should apply `StyledGroup` to your `click` group.\nIf you have only one `Command` or `Multicommand` you may also use the included `StyledCommand` or `StyledMultiCommand`.\n\n```python\nimport click\nfrom click_rich_help import StyledGroup\n\n@click.group(\n    cls=StyledGroup,\n)\ndef cli():\n    pass\n```\n\n```python\nimport click\nfrom click_rich_help import StyledCommand\n\n@click.command(\n  cls=StyledCommand,\n)\ndef cmd():\n    pass\n```\n\nSee the [documentation](https://github.com/daylinmorgan/click-rich-help/blob/main/docs/usage.md) for more info\n\nTo non-interactively preview the included example module in your own terminal you can run\n\nW/ `click-rich-help`  and `curl`\n\n```bash\ncurl -s https://raw.githubusercontent.com/daylinmorgan/click-rich-help/main/scripts/example.sh | bash\n```\n\nYou can also run it yourself if you have installed `click-rich-help`. Which you should!\n\n```bash\npython -m click_rich_help.example -h\n```\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n\n## Contributing\nTo contribute please utilize `poetry` and `pre-commit`.\n\noptionally manage python installation with `conda`:\n\n```bash\nconda create -p ./env python poetry\n```\n\nThen follow the below steps\n1. Fork the Project\n2. Install the package and dev dependencies w/poetry(`cd click-rich-help; poetry install`)\n2. Create your Feature Branch (`git checkout -b feat/AmazingFeature`)\n3. Commit your Changes (`git commit -m \'Add some AmazingFeature\'`)\n4. Run the tests (`mypy click_rich_help; py.test tests`)\n5. Push to the Branch (`git push origin feat/AmazingFeature`)\n6. Open a Pull Request\n\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n## Acknowledgments\n\n* [click](https://github.com/pallets/click)\n* [rich](https://github.com/willmcgugan/rich)\n* [click-help-colors](https://github.com/click-contrib/click-help-colors)\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n\n\n<!-- MARKDOWN LINKS & IMAGES -->\n<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->\n[contributors-shield]: https://img.shields.io/github/contributors/daylinmorgan/click-rich-help.svg?style=flat\n[contributors-url]: https://github.com/daylinmorgan/click-rich-help/graphs/contributors\n[forks-shield]: https://img.shields.io/github/forks/daylinmorgan/click-rich-help.svg?style=flat\n[forks-url]: https://github.com/daylinmorgan/click-rich-help/network/members\n[stars-shield]: https://img.shields.io/github/stars/daylinmorgan/click-rich-help.svg?style=flat\n[stars-url]: https://github.com/daylinmorgan/click-rich-help/stargazers\n[issues-shield]: https://img.shields.io/github/issues/daylinmorgan/click-rich-help.svg?style=flat\n[issues-url]: https://github.com/daylinmorgan/click-rich-help/issues\n[license-shield]: https://img.shields.io/github/license/daylinmorgan/click-rich-help.svg?style=flat\n[license-url]: https://github.com/daylinmorgan/click-rich-help/blob/main/LICENSE.txt\n[circleci-shield]: https://img.shields.io/circleci/build/gh/daylinmorgan/click-rich-help?style=flat\n[circleci-url]: https://img.shields.io/circleci/build/gh/daylinmorgan/click-rich-help\n',
    'author': 'Daylin Morgan',
    'author_email': 'daylinmorgan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/daylinmorgan/click-rich-help',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
