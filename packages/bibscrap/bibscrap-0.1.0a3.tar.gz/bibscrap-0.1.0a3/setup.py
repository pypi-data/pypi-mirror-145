# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bibscrap',
 'bibscrap.cli',
 'bibscrap.cli.commands',
 'bibscrap.core',
 'bibscrap.util']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0',
 'cleo>=1.0.0a4,<2.0.0',
 'pyquery>=1.4.3,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'single-source>=0.2.0,<0.3.0']

extras_require = \
{'devtools': ['black>=22.3.0,<23.0.0',
              'pre-commit>=2.18.1,<3.0.0',
              'tox>=4.0.0b1,<5.0.0',
              'darglint>=1.8.1,<2.0.0',
              'pytest>=7.1.1,<8.0.0',
              'coverage>=6.3.2,<7.0.0',
              'codecov>=2.1.12,<3.0.0',
              'towncrier>=21.9.0,<22.0.0'],
 'docs': ['Sphinx>=4.5.0,<5.0.0',
          'sphinx-rtd-theme>=1.0.0,<2.0.0',
          'sphinxcontrib-bibtex>=2.4.1,<3.0.0',
          'sphinx-panels>=0.6.0,<0.7.0']}

entry_points = \
{'console_scripts': ['bibscrap = bibscrap.cli.app:main']}

setup_kwargs = {
    'name': 'bibscrap',
    'version': '0.1.0a3',
    'description': 'Semi-automated tools for systematic literature reviews.',
    'long_description': "========\nbibscrap\n========\n\n.. image:: https://img.shields.io/pypi/v/bibscrap?style=flat\n   :target: https://pypi.org/project/bibscrap/\n   :alt: PyPI version\n\n.. image:: https://readthedocs.org/projects/bibscrap/badge/?version=latest\n   :target: https://bibscrap.readthedocs.io/en/latest/\n   :alt: bibscrap's documentation\n\n.. image:: https://badges.gitter.im/bibscrap/community.svg\n   :alt: Join the chat at https://gitter.im/bibscrap/community\n   :target: https://gitter.im/bibscrap/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge\n\n.. image:: https://app.travis-ci.com/cotterell/bibscrap.svg\n   :target: https://app.travis-ci.com/cotterell/bibscrap\n   :alt: Continuous integration\n\n.. image:: https://codecov.io/gh/cotterell/bibscrap/branch/main/graph/badge.svg?token=TQQWS0OQ0E\n   :target: https://codecov.io/gh/cotterell/bibscrap\n   :alt: Code coverage\n\n.. image:: https://img.shields.io/pypi/l/bibscrap.svg\n   :target: https://github.com/cotterell/bibscrap/blob/master/LICENSE.rst\n   :alt: License: MIT\n\n.. image:: https://img.shields.io/badge/code%20style-black-161b22.svg\n   :target: https://github.com/psf/black\n   :alt: Code style: black\n\nOverview\n========\n\nThe **bibscrap** package provides semi-automated tools for systematic literature reviews.\n\nRequirements\n============\n\n* Python 3.9+\n\nInstall\n=======\n\nTo install Bibscrap, use one of the commands below:\n\n.. table:: Bibscrap install commands\n   :widths: auto\n\n   ===============  ==========================================\n   Package Manager  Install Command\n   ===============  ==========================================\n   |pip|_           ``pip install --pre bibscrap``\n   |pipenv|_        ``pipenv install --pre bibscrap``\n   |poetry|_        ``poetry add --allow-prerelease bibscrap``\n   ===============  ==========================================\n\n.. |pip| replace:: ``pip``\n.. _pip: https://pip.pypa.io/en/stable/\n\n.. |pipenv| replace:: ``pipenv``\n.. _pipenv: https://pipenv.pypa.io/en/latest/\n\n.. |poetry| replace:: ``poetry``\n.. _poetry: https://python-poetry.org/\n\nDocumentation\n=============\n\nDocumentation is available online at https://bibscrap.readthedocs.io/ and in the\n``docs`` directory.\n\nContributors: Getting Started\n=============================\n\nTo download the development version of **bibscrap** and install its dependencies\ninto a virtual environment, follow the instructions provided below::\n\n  $ git clone https://github.com/cotterell/bibscrap.git\n  $ cd bibscrap\n  $ poetry install -E devtools -E docs\n\nTo activate the virtual environment, use the following command::\n\n  $ poetry shell\n\nIf you are part of the **bibscrap** development team, then you should also\ninstall the pre-commit hooks once your virtual environment is activated.\nYou only need to do this once. Here is the command::\n\n  $ pre-commit install\n\nContributors\n============\n\n=====================  ==========================================================  ============\nContributor            GitHub                                                      Role\n=====================  ==========================================================  ============\nAidan Killer           `@aikill <https://github.com/aikill>`_                      Developer\nJack Solomon           `@jbs26156 <https://github.com/jbs26156>`_                  Developer\nMatthew Pooser         `@mpooser <https://github.com/mpooser>`_                    Developer\nMichael E. Cotterell   `@mepcotterell <https://github.com/mepcotterell>`_          Maintainer\nMitchell Casleton      `@MitchellCasleton <https://github.com/MitchellCasleton>`_  Developer\nMy Nguyen              `@mynguyen0628 <https://github.com/mynguyen0628>`_          Developer\n=====================  ==========================================================  ============\n",
    'author': 'Michael E. Cotterell',
    'author_email': 'mepcotterell@gmail.com',
    'maintainer': 'Michael E. Cotterell',
    'maintainer_email': 'mepcotterell@gmail.com',
    'url': 'https://github.com/cotterell/bibscrap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
