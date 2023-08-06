# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tune', 'tune.db_workers', 'tune.db_workers.dbmodels']

package_data = \
{'': ['*']}

install_requires = \
['Click>=7.1.2,<=8.0.4',
 'atomicwrites>=1.4.0',
 'bask>=0.9.3,<1.0.0',
 'dill>=0.3.4',
 'numpy>=1.19.1',
 'scikit-learn>=0.22,<0.24',
 'scikit-optimize>=0.8,<0.9',
 'scipy>=1.5.2']

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['importlib_metadata>=1.4'],
 'dist': ['joblib>=0.16.0',
          'psycopg2>=2.8.5',
          'sqlalchemy>=1.3.18',
          'pandas>=1.1.0'],
 'docs': ['Sphinx>=3', 'sphinx-book-theme>=0.0.35', 'myst-nb>=0.9']}

entry_points = \
{'console_scripts': ['tune = tune.cli:cli']}

setup_kwargs = {
    'name': 'chess-tuning-tools',
    'version': '0.9.3',
    'description': 'A collection of tools for local and distributed tuning of chess engines.',
    'long_description': '\n.. image:: https://raw.githubusercontent.com/kiudee/chess-tuning-tools/master/docs/_static/CTT-Plots.png\n\n.. image:: https://raw.githubusercontent.com/kiudee/chess-tuning-tools/master/docs/_static/logo.png\n\n.. image:: https://readthedocs.org/projects/chess-tuning-tools/badge/?version=latest&style=flat-square\n        :target: https://chess-tuning-tools.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n.. image:: https://zenodo.org/badge/234719111.svg?style=flat-square\n   :target: https://zenodo.org/badge/latestdoi/234719111\n\n\nA collection of tools for local and distributed tuning of chess engines.\n\n\n* Free software: Apache Software License 2.0\n* Documentation: https://chess-tuning-tools.readthedocs.io.\n\n\nFeatures\n--------\n\n\n\n* Optimization of chess engines using state-of-the-art `Bayesian optimization <https://github.com/kiudee/bayes-skopt>`_.\n* Support for automatic visualization of the optimization landscape.\n* Scoring matches using a Bayesian-pentanomial model for paired openings.\n\nQuick Start\n-----------\n\nIn order to be able to start the tuning, first create a python\nenvironment (at least Python 3.7) and install chess-tuning-tools by typing::\n\n   pip install chess-tuning-tools\n\nFurthermore, you need to have `cutechess-cli <https://github.com/cutechess/cutechess>`_\nin the path. The tuner will use it to run matches.\n\nTo execute the local tuner, simply run::\n\n   tune local -c tuning_config.json\n\nTake a look at the `usage instructions`_ and the `example configurations`_ to\nlearn how to set up the ``tuning_config.json`` file.\n\nInstallation on Windows\n^^^^^^^^^^^^^^^^^^^^^^^\n\nTo get chess-tuning-tools to work on Windows, the easiest way is to install\nthe `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_ distribution.\nThen, create a new environment and install chess-tuning-tools::\n\n   conda create -n myenv python=3.9 scikit-learn=0.23\n   activate myenv\n   pip install chess-tuning-tools\n\n.. _example configurations: https://github.com/kiudee/chess-tuning-tools/tree/master/examples\n.. _usage instructions: https://chess-tuning-tools.readthedocs.io/en/latest/usage.html\n',
    'author': 'Karlson Pfannschmidt',
    'author_email': 'kiudee@mail.upb.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kiudee/chess-tuning-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
