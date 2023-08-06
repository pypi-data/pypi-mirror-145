# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynblint']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.26,<4.0.0',
 'ipython<8',
 'nbconvert>=6.4.0,<7.0.0',
 'nbformat>=5.1.3,<6.0.0',
 'pydantic[dotenv]>=1.9.0,<2.0.0',
 'rich>=11.1.0,<12.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['pynblint = pynblint.main:app']}

setup_kwargs = {
    'name': 'pynblint',
    'version': '0.1.5',
    'description': 'A linter for Jupyter notebooks written in Python.',
    'long_description': '![Logo](https://user-images.githubusercontent.com/13979989/158653487-149633b8-ba85-4a11-976a-70eabc7d0df0.svg)\n\n<div align="center">\n\n[![PyPI version](https://badge.fury.io/py/pynblint.svg)](https://badge.fury.io/py/pynblint)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pynblint)\n\n[![CI](https://github.com/collab-uniba/pynblint/actions/workflows/CI.yml/badge.svg)](https://github.com/collab-uniba/pynblint/actions/workflows/CI.yml)\n[![Documentation Status](https://readthedocs.org/projects/pynblint/badge/?version=latest)](https://pynblint.readthedocs.io/en/latest/?badge=latest)\n[![codecov](https://codecov.io/gh/collab-uniba/pynblint/branch/master/graph/badge.svg?token=CSX10BJ1CU)](https://codecov.io/gh/collab-uniba/pynblint)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n</div>\n\nMany professional data scientists use Jupyter Notebook to accomplish their daily tasks, from preliminary data exploration to model prototyping. Notebooks\' interactivity is particularly convenient for data-centric programming and their self-documenting nature provides excellent support for the communication of analytical results.\n\nNevertheless, Jupyter Notebook has been often criticized for inducing bad programming habits and scarcely supporting Software Engineering best practices. To really benefit from notebooks, users should be aware of their common pitfalls and learn how to prevent them.\n\nIn previous work (see ["Eliciting Best Practices for Collaboration with Computational Notebooks"](https://arxiv.org/abs/2202.07233) [\\[1\\]](#references)), we introduced a catalog of 17 empirically-validated guidelines for the collaborative use of notebooks in a professional context.\n\nTo foster the adoption of these best practices, we have created Pynblint, a static analysis tool for Jupyter notebooks written in Python. Pynblint reveals potential notebook defects and recommends corrective actions. It can be operated either as a standalone CLI application or as part of a CI/CD pipeline.\n\n![Pynblint screens](https://user-images.githubusercontent.com/13979989/158661765-7a71e646-cde7-4e69-957d-a8f3af440101.svg)\n\nThe core linting rules of Pynblint have been derived as operationalizations of the best practices from our catalog. Nonetheless, the plug-in architecture of Pynblint enables its users to easily extend the core set of checks with their own linting rules.\n\n## Requirements\n\nPython 3.7+.\n\n## Installation\n\nPynblint can be installed with `pip` or another PyPI package manager:\n\n```bash\npip install pynblint\n```\n\nAfter installation, we recommend exploring the command-line interface of the tool:\n\n```bash\npynblint --help\n```\n\n<!-- To use Pynblint, clone this repository and install it with [Poetry](https://python-poetry.org):\n\n```bash\npoetry install --no-dev\n```\n\nTo install Pynblint for development purposes, simply omit the `--no-dev` option:\n\n```bash\npoetry install\n``` -->\n\n## Usage\n\nPynblint can be used to analyze:\n\n- a standalone notebook:\n\n    ```bash\n    pynblint path/to/the/notebook.ipynb\n    ```\n\n- a code repository containing notebooks:\n\n    ```bash\n    pynblint path/to/the/project/dir/\n    ```\n\n  - (possibly also compressed as a `.zip` archive):\n\n      ```bash\n      pynblint path/to/the/compressed/archive.zip\n      ```\n\n- a _public_ GitHub repository containing notebooks\n  (support for private repositories is on our roadmap 🙂):\n\n    ```bash\n    pynblint --from-github https://github.com/collab-uniba/pynblint\n    ```\n\nFor further information on the available options, please refer to the project [documentation](https://pynblint.readthedocs.io/en/latest/?badge=latest).\n\n## Catalog of best practices\n\nIn the following, we report the catalog of empirically-validated best practices on which Pynblint is based [\\[1\\]](#references).\n\nFor each guideline, we specify the current state of implementation within Pynblint:\n\n- :white_check_mark: = "implemented"\n- :hourglass_flowing_sand: = "partially implemented / work in progress"\n- :x: = "not on our roadmap"\n\n| State                    | Best Practice from [\\[1\\]](#references)                  |\n| ------------------------ | -------------------------------------------------------- |\n| :white_check_mark:       | Use version control                                      |\n| :white_check_mark:       | Manage project dependencies                              |\n| :hourglass_flowing_sand: | Use self-contained environments                          |\n| :white_check_mark:       | Put imports at the beginning                             |\n| :white_check_mark:       | Ensure re-executability (re-run notebooks top to bottom) |\n| :hourglass_flowing_sand: | Modularize your code                                     |\n| :hourglass_flowing_sand: | Test your code                                           |\n| :white_check_mark:       | Name your notebooks consistently                         |\n| :hourglass_flowing_sand: | Stick to coding standards                                |\n| :hourglass_flowing_sand: | Use relative paths                                       |\n| :white_check_mark:       | Document your analysis                                   |\n| :white_check_mark:       | Leverage Markdown headings to structure your notebook    |\n| :white_check_mark:       | Keep your notebook clean                                 |\n| :white_check_mark:       | Keep your notebook concise                               |\n| :x:                      | Distinguish production and development artifacts         |\n| :hourglass_flowing_sand: | Make your notebooks available                            |\n| :white_check_mark:       | Make your data available                                 |\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n\n## References\n\n[1] Luigi Quaranta, Fabio Calefato, and Filippo Lanubile. 2022. [Eliciting Best Practices for Collaboration with Computational Notebooks.](https://arxiv.org/abs/2202.07233) _Proc. ACM Hum.-Comput. Interact. 6_, CSCW1, Article 87 (April 2022), 41 pages. <https://doi.org/10.1145/3512934>\n',
    'author': 'Luigi Quaranta',
    'author_email': 'luigi.quaranta@uniba.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pynblint.readthedocs.io/en/latest/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
