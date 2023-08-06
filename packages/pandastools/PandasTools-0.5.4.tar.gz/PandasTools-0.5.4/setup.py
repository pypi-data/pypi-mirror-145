# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pandastools', 'pandastools.accessors', 'pandastools.utils']

package_data = \
{'': ['*']}

install_requires = \
['llvmlite>=0.38,<0.39', 'pandas>=1.0.5,<2.0.0']

extras_require = \
{':python_version >= "3.9" and python_version < "3.11"': ['numba>=0.55,<0.56'],
 'addons:python_version >= "3.9" and python_version < "3.11"': ['scipy>=1.7.0,<2.0.0']}

setup_kwargs = {
    'name': 'pandastools',
    'version': '0.5.4',
    'description': 'Helper functions for Pandas DataFrames / Series',
    'long_description': '# pandastools: Helper functions for Pandas DataFrames / Series\n[![PyPI Latest Release](https://img.shields.io/pypi/v/pandastools.svg)](https://pypi.org/project/pandastools/)\n[![Package Status](https://img.shields.io/pypi/status/pandastools.svg)](https://pypi.org/project/pandastools/)\n[![License](https://img.shields.io/pypi/l/pandastools.svg)](https://github.com/pandastools-dev/pandastools/blob/master/LICENSE)\n[![Travis Build Status](https://travis-ci.org/pandastools-dev/pandastools.svg?branch=master)](https://travis-ci.org/pandastools-dev/pandastools)\n[![CodeCov](https://codecov.io/gh/phil65/PandasTools/branch/master/graph/badge.svg)](https://codecov.io/gh/phil65/PandasTools)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![PyUp](https://pyup.io/repos/github/phil65/PandasTools/shield.svg)](https://pyup.io/repos/github/phil65/PandasTools/)\n\n## What is it?\n\n**PandasTools** is a Python package that provides additional functions for Pandas DataFrames, Series and Indexes via accessors\n\n## Main Features\n\n  - TODO\n\n   [dataframe]: https://phil65.github.io/PandasTools/dataframe.html\n\n\n## Where to get it\nThe source code is currently hosted on GitHub at:\nhttps://github.com/phil65/PandasTools\n\nThe latest released version are available at the [Python\npackage index](https://pypi.org/project/pandastools).\n\n```sh\n# or PyPI\npip install pandastools\n```\n\n## Dependencies\n- [pandas](https://pypi.org/project/pandas)\n- [numba](https://pypi.org/project/numba)\n\n\n## Installation from sources\n\nThis project uses poetry for dependency management and packaging. Install this first.\nIn the `pandastools` directory (same one where you found this file after\ncloning the git repo), execute:\n\n```sh\npoetry install\n```\n\n## License\n[MIT](LICENSE)\n\n## Documentation\nThe official documentation is hosted on Github Pages: https://phil65.github.io/PandasTools/\n\n## Contributing to pandas [![Open Source Helpers](https://www.codetriage.com/phil65/pandastools/badges/users.svg)](https://www.codetriage.com/phil65/pandastools)\n\nAll contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.\n\nOr maybe through using PandasTools you have an idea of your own or are looking for something in the documentation and thinking ‘this can be improved’...you can do something about it!\n',
    'author': 'phil65',
    'author_email': 'philipptemminghoff@googlemail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/phil65/pandastools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
