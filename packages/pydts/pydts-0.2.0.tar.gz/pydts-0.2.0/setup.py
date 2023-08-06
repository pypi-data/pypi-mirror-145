# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pydts', 'pydts.examples_utils']

package_data = \
{'': ['*'], 'pydts': ['datasets/*']}

install_requires = \
['lifelines>=0.26.4,<0.27.0',
 'mkdocs-material>=8.2.4,<9.0.0',
 'mkdocs>=1.2.3,<2.0.0',
 'mkdocstrings>=0.18.1,<0.19.0',
 'mknotebooks>=0.7.1,<0.8.0',
 'pandarallel>=1.5.7,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'scipy>=1.8.0,<2.0.0',
 'statsmodels>=0.13.2,<0.14.0',
 'tqdm>=4.63.0,<5.0.0']

setup_kwargs = {
    'name': 'pydts',
    'version': '0.2.0',
    'description': 'Discrete time survival analysis with competing risks',
    'long_description': "[![pypi version](https://img.shields.io/pypi/v/pydts)](https://pypi.org/project/pydts/)\n[![Tests](https://github.com/tomer1812/pydts/workflows/Tests/badge.svg)](https://github.com/tomer1812/pydts/actions?workflow=Tests)\n[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://tomer1812.github.io/pydts)\n\n# Discrete Time Survival Analysis  \nA Python package for discrete time survival data analysis with competing risks.\n\n![PyDTS](docs/icon.png)  \n\n[Tomer Meir](https://tomer1812.github.io/), [Rom Gutman](https://github.com/RomGutman), [Malka Gorfine](https://www.tau.ac.il/~gorfinem/) 2022\n\n[Documentation](https://tomer1812.github.io/pydts/)  \n\n## Installation\n```console\npip install pydts\n```\n\n## Quick Start\n\n```python\nfrom pydts.fitters import TwoStagesFitter\nfrom pydts.examples_utils.generate_simulations_data import generate_quick_start_df\nfrom sklearn.model_selection import train_test_split\n\npatients_df = generate_quick_start_df(n_patients=10000, n_cov=5, d_times=30, j_events=2, pid_col='pid', seed=0)\ntrain_df, test_df = train_test_split(patients_df, test_size=0.25)\n\nfitter = TwoStagesFitter()\nfitter.fit(df=train_df.drop(['C', 'T'], axis=1))\nfitter.print_summary()\n\n```\n\n## Other Examples\n1. [Simple Example](https://tomer1812.github.io/pydts/Simple%20Simulation/)\n2. [Hospital Length of Stay Simulation Example](https://tomer1812.github.io/pydts/SimulatedDataset/)\n",
    'author': 'Tomer Meir',
    'author_email': 'tomer1812@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tomer1812/pydts',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
