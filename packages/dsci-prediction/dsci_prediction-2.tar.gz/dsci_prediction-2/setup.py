# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dsci_prediction']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dsci-prediction',
    'version': '2',
    'description': 'a package for predicting if cancer is treatable or not',
    'long_description': '# prediction\n\na package for predicting if cancer is treatable or not\n\n## Installation\n\n```bash\n$ pip install dsci-prediction\n```\n\n## Usage\n\n`prediction` can be used to load, clean, build a test model and plot results\nas follows:\n\n\n\n```python\nfrom dsci_prediction.dsci_prediction import *\n\nfile_path = "data.txt"  # path to your file\nload = load_data(input_path, output_path)\nclean = clean_data(input_path, output_path_train, output_path_test)\nmodel = build_test_model(train_df, test_df, cross_val_output, tuned_para_output, classification_output, confusion_matrix_output)\nplt.show()\n```\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. \nPlease note that this project is released with a Code of Conduct. \nBy contributing to this project, you agree to abide by its terms.\n\n## License\n\n`prediction` was created by Clichy Bazenga. It is licensed under the terms\nof the MIT license.\n\n## Credits\n\n`prediction` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n\n\n\n\n\n\n',
    'author': 'Clichy Bazenga',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9.5,<4.0.0',
}


setup(**setup_kwargs)
