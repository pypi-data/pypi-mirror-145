# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fppanalysis']

package_data = \
{'': ['*']}

install_requires = \
['PyWavelets>=1.2.0,<2.0.0',
 'numpy>=1.18,<2.0',
 'scipy>=1.8.0,<2.0.0',
 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'fppanalysis',
    'version': '0.1.2',
    'description': 'Analysis tools for time series',
    'long_description': '# fpp-analysis-tools\nCollection of tools designed to analyse time series of intermittent fluctuations.\n\n## Installation\nThe package is published to PyPI and can be installed with\n```sh\npip install fppanalysis\n```\n\nIf you want the development version you must first clone the repo to your local machine,\nthen install the project in development mode:\n\n```sh\ngit clone git@github.com:uit-cosmo/fpp-analysis-tools.git\ncd fpp-analysis-tools\npoetry install\n```\n\nIf you plan to use the GPUs, specifically for the deconvolution then setup the following conda environment:\n```sh\nconda create --name my-env\nconda activate my-env\nconda install -c rapidsai -c nvidia -c conda-forge \\\n    cusignal=21.08 python=3.8 cudatoolkit=11.0\nconda install poetry \npoetry install\n```\n\n## Usage\nYou can import all functions directly from `fppanalysis`, such as\n\n```Python\nimport fppanalysis as fa\n\nbin_centers, hist = fa.get_hist(Data, N)\n```\n',
    'author': 'gregordecristoforo',
    'author_email': 'gregor.decristoforo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/uit-cosmo/fpp-analysis-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
