# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dsci_prediction', 'dsci_prediction..ipynb_checkpoints']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dsci-prediction',
    'version': '1',
    'description': 'a package for predicting if cancer is treatable or not',
    'long_description': '# prediction\n\na package for predicting if cancer is treatable or not\n\n## Installation\n\n```bash\n$ pip install prediction\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`prediction` was created by Clichy Bazenga. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`prediction` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Clichy Bazenga',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '==3.9.5',
}


setup(**setup_kwargs)
