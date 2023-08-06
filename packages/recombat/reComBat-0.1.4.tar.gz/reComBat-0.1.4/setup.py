# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['reComBat', 'reComBat.src']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.4.0,<0.5.0',
 'numpy>=1.20.0,<2.0.0',
 'pandas>=1.3.4,<2.0.0',
 'sklearn>=0.0,<0.1',
 'tqdm>=4.62.3,<5.0.0']

entry_points = \
{'console_scripts': ['reComBat = reComBat.cli:main']}

setup_kwargs = {
    'name': 'recombat',
    'version': '0.1.4',
    'description': 'regularised ComBat method to correct batch effects',
    'long_description': '# reComBat\n\n\n[![License: BSD](https://img.shields.io/github/license/BorgwardtLab/recombat)](https://opensource.org/licenses/BSD-3-Clause)\n[![Version](https://img.shields.io/pypi/v/recombat)](https://pypi.org/project/recombat/)\n[![PythonVersion](https://img.shields.io/pypi/pyversions/recombat)]()\n\nThis is the reComBat implementation as described in our [recent paper](https://doi.org/10.1101/2021.11.22.469488).\nThe paper introduces a generalized version of the empirical Bayes batch correction method introduced in [1].\nWe use the two-design-matrix approach of Wachinger et al. [2]\n\n\n## Installation\n\nreComBat is a PyPI package which can be installed via `pip`:\n\n```\npip install reComBat\n```\n\nYou can also clone the repository and install it locally via [Poetry](https://python-poetry.org/) by executing\n```bash\npoetry install\n```\nin the repository directory.\n\n## Usage\n\nThe `reComBat` package is inspired by the code of [3] and also uses a scikit-learn like\nAPI.\n\nIn a Python script, you can import it via\n```python\nfrom reComBat import reComBat\n\ncombat = reComBat()\ncombat.fit(data,batches)\ncombat.transform(data,batches)\n```\nor\n\n```python\ncombat.fit_transform(data,batches)\n```\n\nAll data input (data, batches, design matrices) are input as pandas dataframes.\nThe format is (rows x columns) = (samples x features), and the index is an arbitrary sample index.\nThe batches should be given as a pandas series. Note that there are two types of columns for design matrices,\nnumerical columns and categorical columns. All columns in X and C are by default assumed categorical. If a column contains numerical\ncovariates, these columns should have the suffix "_numerical" in the column name.\n\nThere is also a command-line interface which can be called from a bash shell.\n```bash\nreComBat data_file.csv batch_file.csv --<optional args>\n```\n\n## Arguments\n\nThe `reComBat` class has many optional arguments (see below).\nThe `fit`, `transform` and `fit_transform` functions all take pandas dataframes as arguments,\n`data` and `batches`. Both dataframes should be in the form above.\n\n## Optional arguments\n\nThe `reComBat` class has the following optional arguments:\n\n  - `parametric` : `True` or `False`. Choose between the parametric or non-parametric version of the empirical Bayes method.\n  By default, this is `True`, i.e. the parametric method is performed. Note that the non-parametric method has a longer run time than the parametric one.\n  - `model` : Choose which regression model should be used to standardise the data. You can choose between `linear`, `ride`, `lasso` and `elastic_net` regression.\n  By default the `linear` model is used.\n  - `config` : A Python dictionary specifying the keyword arguments for the relevant `scikit-learn` regression functions. for further details refer to [sklearn.linear_model](https://scikit-learn.org/stable/modules/classes.html#module-sklearn.linear_model). The default is `None`.\n  - `conv_criterion` : The convergence criterion for the parametric empirical Bayes optimization. Relative, rather than absolute convergence criteria are used.\n  The default is 1e-4.\n  - `max_iter` : The maximum number of iterations for the parametric empirical Bayes optimization. The default is 1000.\n  - `n_jobs` : The number of parallel thread used in the non-parametric empirical Bayes optimization. A larger number of threads considerably speeds up the computation, but also has higher memory requirements. The default is the number of CPUs of the machine.\n  - `mean_only` : `True` or `False`.  Chooses whether the only the means are adjusted (no scaling is performed), or the full algorithm should be run. The default is `False`.\n  - `optimize_params` : `True` or `False`. Chooses whether the Bayesian parameters should be optimised, or if the starting values should be used. The default is `True`.\n  - `reference_batch` : If the data contains a reference batch, then this can be specified here. The reference batch will not be adjusted. The default is `None`.\n  - `verbose` : `True` or `False`. Toggles verbose output. The default is `True`.\n\nThe command line interface can take any of these arguments (except for `config`) via `--<argument>=ARG`. Any `scikit-learn` keyword arguments should be given explicitly, e.g. `--alpha=1e-10`. The command line interface has the additional following optional arguments:\n  - `X_file` : The csv file containing the design matrix of desired variation. The default is `None`.\n  - `C_file` : The csv file containing the design matrix of undesired variation. The default is `None`.\n  - `data_path` : The path to the data/design matrices. The default is the current directory.\n  - `out_path` : The path where the output file should be stored. The default is the current directory.\n  - `out_file` : The name out the output file (with extension).\n\n## Output\n\nThe `transform` method and the command line interface output a dataframe, respectively a csv file, of the form (samples x features) with the adjusted data.\n\n## Contact\n\nThis code is developed and maintained by members of the [Machine Learning and\nComputational Biology Lab](https://www.bsse.ethz.ch/mlcb) of [Prof. Dr.\nKarsten Borgwardt](https://www.bsse.ethz.ch/mlcb/karsten.html):\n\n- [Michael Adamer](https://mikeadamer.github.io/) ([GitHub](https://github.com/MikeAdamer))\n- Sarah Brüningk ([GitHub](https://github.com/sbrueningk))\n\n*References*:\n\n[1] W. Evan Johnson, Cheng Li, Ariel Rabinovic, Adjusting batch effects in microarray expression data using empirical Bayes methods, Biostatistics, Volume 8, Issue 1, January 2007, Pages 118–127, https://doi.org/10.1093/biostatistics/kxj037\n\n\n[2] Christian Wachinger, Anna Rieckmann, Sebastian Pölsterl. Detect and Correct Bias in Multi-Site Neuroimaging Datasets. arXiv:2002.05049\n\n[3] pycombat, CoAxLab, https://github.com/CoAxLab/pycombat\n',
    'author': 'Michael F. Adamer',
    'author_email': 'mikeadamer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BorgwardtLab/reComBat',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
