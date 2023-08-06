# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['somepytools']

package_data = \
{'': ['*']}

extras_require = \
{'all': ['PyYAML>=6.0,<7.0',
         'toml>=0.10.2,<0.11.0',
         'numpy>=1.22.3,<2.0.0',
         'opencv-python-headless>=4.5.5,<5.0.0',
         'torch>=1.11.0,<2.0.0']}

setup_kwargs = {
    'name': 'somepytools',
    'version': '1.0.0',
    'description': 'Just some useful Python tools',
    'long_description': "# Template for Data Science Project\n\nThis repo aims to give a robust starting point to any Data Science related\nproject.\n\nIt contains readymade tools setup to start adding dependencies and coding.\n\nTo get yourself familiar with tools used here watch\n[my talk on Data Science project setup (in Russian)](https://youtu.be/jLIAiDMyseQ)\n\n**If you use this repo as a template - leave a star please** because template\nusages don't count in Forks.\n\n## Workflow\n\nExperiments and technology discovery are usualy performed on Jupyter Notebooks.\nFor them `notebooks` directory is reserved. More info on working with Notebooks\ncould be found in `notebooks/README.md`.\n\nMore mature part of pipeline (functions, classes, etc) are stored in `.py` files\nin main package directory (by default `ds_project`).\n\n## What to change?\n\n- project name (default: `ds_project`)\n  - in `pyproject.toml` - tool.poetry.name\n  - main project directory (`ds_project`)\n  - test in `tests` directory\n- line length (default: `90`) [Why 90?](https://youtu.be/esZLCuWs_2Y?t=1287)\n  - in `pyproject.toml` in blocks\n    - black\n    - isort\n  - in `setup.cfg` for `flake8`\n  - in `.pre-commit-config.yaml` for `prettier`\n\n## How to setup an environment?\n\nThis template use `poetry` to manage dependencies of your project. They\n\nFirst you need to\n[install poetry](https://python-poetry.org/docs/#installation).\n\nThen if you use `conda` (recommended) to manage environments (to use regular\nvirtualenvenv just skip this step):\n\n- tell `poetry` not to create new virtualenv for you\n\n  (instead `poetry` will use currently activated virtualenv):\n\n  `poetry config virtualenvs.create false`\n\n- create new `conda` environment for your project (change env name for your\n  desired one):\n\n  `conda create -n ds_project python=3.9`\n\n- actiave environment:\n\n  `conda activate ds_project`\n\nNow you are ready to add dependencies to your project. For this use\n[`add` command](https://python-poetry.org/docs/cli/#add):\n\n`poetry add scikit-learn torch <any_package_you_need>`\n\nNext run `poetry install` to check your final state are even with configs.\n\nAfter that add changes to git and commit them\n`git add pyproject.toml poetry.lock`\n\nFinally add `pre-commit` hooks to git: `pre-commit install`\n\nAt this step you are ready to write clean reproducible code!\n",
    'author': 'Vladilav Goncharenko',
    'author_email': 'vladislav.goncharenko@phystech.edu',
    'maintainer': 'Vladislav Goncharenko',
    'maintainer_email': 'vladislav.goncharenko@phystech.edu',
    'url': 'https://github.com/v-goncharenko/somepytools',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
