# prediction

a package for predicting if cancer is treatable or not

## Installation

```bash
$ pip install dsci-prediction
```

## Usage

`prediction` can be used to load, clean, build a test model and plot results
as follows:



```python
from dsci_prediction.dsci_prediction import *

file_path = "data.txt"  # path to your file
load = load_data(input_path, output_path)
clean = clean_data(input_path, output_path_train, output_path_test)
model = build_test_model(train_df, test_df, cross_val_output, tuned_para_output, classification_output, confusion_matrix_output)
plt.show()
```

## Contributing

Interested in contributing? Check out the contributing guidelines. 
Please note that this project is released with a Code of Conduct. 
By contributing to this project, you agree to abide by its terms.

## License

`prediction` was created by Clichy Bazenga. It is licensed under the terms
of the MIT license.

## Credits

`prediction` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).






