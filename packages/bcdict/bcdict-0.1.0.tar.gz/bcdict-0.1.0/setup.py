# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bcdict']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bcdict',
    'version': '0.1.0',
    'description': 'Python dictionary with broadcast support.',
    'long_description': '[![Tests](https://github.com/mariushelf/bcdict/actions/workflows/tests.yml/badge.svg)](https://github.com/mariushelf/bcdict/actions/workflows/tests.yml)\n[![codecov](https://codecov.io/gh/mariushelf/bcdict/branch/master/graph/badge.svg?token=5E2159JF60)](https://codecov.io/gh/mariushelf/bcdict)\n\n# Broadcast Dictionary\n\n\nPython dictionary with broadcast support.\n\n# Usage\n\n```python\nfrom bcdict import BCDict\n>>> d = BCDict({"a": "hello", "b": "world!"})\n>>> d\n{\'a\': \'hello\', \'b\': \'world!\'}\n```\n\n\nRegular element access:\n```python\n>>> d[\'a\']\n\'hello\'\n```\n\n\nRegular element assignments\n```python\n>>> d[\'a\'] = "Hello"\n>>> d\n{\'a\': \'Hello\', \'b\': \'world!\'}\n```\n\nCalling functions:\n```python\n>>> d.upper()\n{\'a\': \'HELLO\', \'b\': \'WORLD!\'}\n```\n\nSlicing:\n```python\n>>> d[1:3]\n{\'a\': \'el\', \'b\': \'or\'}\n```\n\nApplying functions:\n```python\n>>> d.pipe(len)\n{\'a\': 5, \'b\': 6}\n```\n\nWhen there is a conflict between an attribute in the values and an attribute in\n`BCDict`, use the attribute accessor and item() function explicitly:\n\n```python\n>>> d.a.upper()\n{\'a\': \'HELLO\', \'b\': \'WORLD!\'}\n```\n\nSlicing with conflicting keys:\n```python\n>>> n = BCDict({1:"hello", 2: "world"})\n>>> n[1]\n\'hello\'\n>>> n.item(1)\n{1: \'e\', 2: \'o\'}\n```\n\n# Full example\n\nHere we create a dictionary with 3 datasets and then train, apply and validate\na linear regression on all 3 datasets without a single for loop or dictionary\ncomprehension.\n\n```python\nfrom collections.abc import Collection\nfrom pprint import pprint\nimport numpy as np\nimport pandas as pd\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.metrics import r2_score\n\ndef get_random_data(datasets: Collection) -> dict[str, pd.DataFrame]:\n    """Just create some random data."""\n    columns = list("ABCD") + ["target"]\n    dfs = {}\n    for name in datasets:\n        dfs[name] = pd.DataFrame(\n            np.random.random((10, len(columns))), columns=columns\n        )\n    return dfs\n\ndatasets = ["noord", "brabant", "limburg"]\n\n# make dict with three dataframes, one for each grid:\ntrain_dfs = BCDict(get_random_data(datasets))\ntest_dfs = BCDict(get_random_data(datasets))\n\nfeatures = list("ABCD")\ntarget = "target"\n\n# get X, y *for all 3 grids at once*:\nX_train = train_dfs[features]\ny_train = train_dfs[target]\n\n# get X, y *for all 3 grids at once*:\nX_test = test_dfs[features]\ny_test = test_dfs[target]\n\n# creates models for all 3 grids at once:\n# we call the `train` function on each dataframe in X_train, and pass the\n# corresponding y_train series into the function.\ndef train(X: pd.DataFrame, y: pd.Series) -> LinearRegression:\n    """We use this function to train a model."""\n    model = LinearRegression()\n    model.fit(X, y)\n    return model\n\nmodels = X_train.pipe(train, y_train)\n\n# Apply each model to the correct grid.\n# `models` is a BCDict.\n# When calling the `predict` function, it knows that `test_dfs` is a dict with\n# the same keys as `models`. When calling predict on each model, the corresponding\n# dataframe from `test_dfs` is passed to the function.\npreds = models.predict(X_test)\n\n# now we pipe all predictions and the\nscores = y_test.pipe(r2_score, preds)\npprint(scores)\n# {\'brabant\': -2.2075573154836925,\n#  \'limburg\': -1.3066288799673251,\n#  \'noord\': -0.8467452520467658}\n\nassert list(scores.keys()) == datasets\nassert all((isinstance(v, float) for v in scores.values()))\n\n# Conclusion: no single for loop or dict comprehension used to train 3 models\n# predict and evaluate 3 grids :)\n\n```\n\n\n\nOriginal repository: [https://github.com/mariushelf/bcdict](https://github.com/mariushelf/bcdict)\n\nAuthor: Marius Helf \n  ([helfsmarius@gmail.com](mailto:helfsmarius@gmail.com))\n\n\n# License\n\nMIT -- see [LICENSE](LICENSE)\n\n',
    'author': 'Marius Helf',
    'author_email': 'helfsmarius@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mariushelf/bcdict',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
