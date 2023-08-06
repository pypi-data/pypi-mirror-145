# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pertpy', 'pertpy.data', 'pertpy.plot', 'pertpy.preprocessing', 'pertpy.tools']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1',
 'click>=7.0.0',
 'ipywidgets>=7.6.5',
 'muon>=0.1.2',
 'pypi-latest>=0.1.1',
 'requests>=2.27.1',
 'rich>=10.11.0',
 'scanpy>=1.8.1',
 'scikit-misc>=0.1.4,<0.2.0',
 'switchlang>=0.1.0,<0.2.0']

entry_points = \
{'console_scripts': ['pertpy = pertpy.__main__:main']}

setup_kwargs = {
    'name': 'pertpy',
    'version': '0.1.0',
    'description': 'Perturbation Analysis in the Scanpy ecosystem.',
    'long_description': '[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Build](https://github.com/theislab/pertpy/workflows/Build%20pertpy%20Package/badge.svg)](https://github.com/theislab/pertpy/actions?workflow=Package)\n[![Codecov](https://codecov.io/gh/theislab/pertpy/branch/master/graph/badge.svg)](https://codecov.io/gh/theislab/pertpy)\n[![License](https://img.shields.io/github/license/theislab/pertpy)](https://opensource.org/licenses/Apache2.0)\n[![PyPI](https://img.shields.io/pypi/v/pertpy.svg)](https://pypi.org/project/pertpy/)\n[![Python Version](https://img.shields.io/pypi/pyversions/pertpy)](https://pypi.org/project/pertpy)\n[![Read the Docs](https://img.shields.io/readthedocs/pertpy/latest.svg?label=Read%20the%20Docs)](https://pertpy.readthedocs.io/)\n[![Test](https://github.com/theislab/pertpy/workflows/Run%20pertpy%20Tests/badge.svg)](https://github.com/theislab/pertpy/actions?workflow=Tests)\n[![PyPI](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n\n# pertpy\n\n## Features\n\n-   Differential cell type perturbation analysis with Augurpy\n\n## Installation\n\nYou can install _pertpy_ via [pip] from [PyPI]:\n\n```console\n$ pip install pertpy\n```\n\n## Usage\n\nPlease see [Usage] for details.\n\n## Credits\n\nThis package was created with [cookietemple] using [Cookiecutter] based on [Hypermodern_Python_Cookiecutter].\n\n[cookiecutter]: https://github.com/audreyr/cookiecutter\n[cookietemple]: https://cookietemple.com\n[hypermodern_python_cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[pip]: https://pip.pypa.io/\n[pypi]: https://pypi.org/\n[usage]: https://pertpy.readthedocs.io/en/latest/usage.html\n',
    'author': 'Lukas Heumos',
    'author_email': 'lukas.heumos@posteo.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/theislab/pertpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<3.10',
}


setup(**setup_kwargs)
