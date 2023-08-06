# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['lemon', 'lemon.utils', 'lemon.utils.datasets', 'lemon.utils.matchers']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1,<2', 'scikit-learn>=1.0,<2.0']

extras_require = \
{'all': ['transformers>=4.10.3,<5.0.0',
         'torch>=1.9.1,<2.0.0',
         'py-entitymatching>=0.4.0,<0.5.0',
         'pyarrow>=5.0.0,<6.0.0'],
 'matchers': ['transformers>=4.10.3,<5.0.0',
              'torch>=1.9.1,<2.0.0',
              'py-entitymatching>=0.4.0,<0.5.0'],
 'storage': ['pyarrow>=5.0.0,<6.0.0']}

setup_kwargs = {
    'name': 'lemon-explain',
    'version': '0.1.1',
    'description': 'LEMON: Explainable Entity Matching',
    'long_description': '# LEMON: Explainable Entity Matching\n\n![Illustration of LEMON](images/LEMON.png)\n\nLEMON is an explainability method that addresses the unique challenges of explaining entity matching models.\n\n\n## Installation\n\n```shell\npip install lemon-explain\n```\nor\n```shell\npip install lemon-explain[storage]  # Save and load explanations\npip install lemon-explain[matchers] # To run matchers in lemon.utils\npip install lemon-explain[all]      # All dependencies\n```\n\n## Usage\n\n```python\nimport lemon\n\n\n# You need a matcher that follows this api:\ndef predict_proba(records_a, records_b, record_id_pairs):\n    ... # predict probabilities / confidence scores\n    return proba\n\nexp = lemon.explain(records_a, records_b, record_id_pairs, predict_proba)\n\n# exp can be visualized in a Jupyter notebook or saved to a json file\nexp.save("explanation.json")\n\n```\n[See the example notebook](https://nbviewer.jupyter.org/github/NilsBarlaug/lemon/blob/main/Example.ipynb)\n\n[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/NilsBarlaug/lemon/blob/main/Example.ipynb)\n\n![Example of explanation from LEMON](images/explanation.png)\n\n## Documentation\n\n### lemon.explain()\n\n```\nlemon.explain(\n    records_a: pd.DataFrame,\n    records_b: pd.DataFrame,\n    record_id_pairs: pd.DataFrame,\n    predict_proba: Callable,\n    *,\n    num_features: int = 5,\n    dual_explanation: bool = True,\n    estimate_potential: bool = True,\n    granularity: str = "counterfactual",\n    num_samples: int = None,\n    token_representation: str = "record-bow",\n    token_patterns: Union[str, List[str], Dict] = "[^ ]+",\n    explain_attrs: bool = False,\n    attribution_method: str = "lime",\n    show_progress: bool = True,\n    random_state: Union[int, np.random.Generator, None] = 0,\n    return_dict: bool = None,\n) -> Union[MatchingAttributionExplanation, Dict[any, MatchingAttributionExplanation]]:\n```\n\n#### Parameters\n- **records_a** : pd.DataFrame\n  - Records from data source a.\n- **records_b** : pd.DataFrame\n    - Records from data source b.\n- **record_id_pairs** : pd.DataFrame\n    - Which record pairs to explain.\n      Must be a pd.DataFrame with columns `"a.rid"` and `"b.rid"` that reference the index of `records_a` and `records_b` respectively.\n- **predict_proba** : Callable\n  - Matcher function that predicts the probability of match.\n    Must accept three arguments: `records_a`, `records_b`, and `record_id_pairs`.\n    Should return array-like (list, np.ndarray, pd.Series, ...) of floats between 0 and 1 - the predicted probability that a record pair is a match - for all record pairs described by `record_id_pairs` in the same order.\n- **num_features** : int, default = 5\n  - The number of features to select for the explanation.\n- **dual_explanation** : bool, default = True\n  - Whether to use dual explanations or not.\n- **estimate_potential** : bool, default = True\n  - Whether to estimate potential or not.\n- **granularity** : {"tokens", "attributes", "counterfactual"}, default = "counterfactual"\n  - The granularity of the explanation.\n    For more info on `"counterfactual"` granularity see our paper.\n- **num_samples** : int, default = None\n  - The number of neighborhood samples to use.\n    If None a heuristic will automatically pick the number of samples.\n- **token_representation** : {"independent", "shared-bow", "record-bow"}, default = "record-bow"\n  - Which token representation to use.\n    - independent: All tokens are unique.\n    - shared-bow: Bag-of-words representation shared across both records\n    - record-bow: Bag-of-words representation per individual record\n- **token_patterns** : str, List[str], or Dict, default = `"[^ ]+"`\n  - Regex patterns for valid tokens in strings.\n    A single string will be interpreted as a regex pattern and all strings will be tokenized into non-overlapping matches of this pattern.\n    You can specify a list of patterns to tokenize into non-overlapping matches of any pattern.\n    For fine-grained control of how different parts of records are tokenized you can provide a dictionary with keys on the format `("a" or "b", attribute_name, "attr" or "val")` and values that are lists of token regex patterns.\n- **explain_attrs** : bool, default = False\n  - Whether to explain attribution names or not.\n    If True, `predict_proba` should accept the keyword argument `attr_strings` - a list that specifies what strings to use as attributes for each prediction.\n    Each list element is on the format {("a" or "b", record_column_name): attr_string}.\n- **attribution_method** : {"lime", "shap"}, default = False\n  - Which underlying method to use contribution estimation.\n    Note that in order to use shap `estimate_potential` must be False and the shap package must be installed.\n- **show_progress** : bool, default = True\n  - Whether to show progress or not. This is passed to `predict_proba` if it accepts this parameter.\n- **return_dict** : bool, default = None\n  - If True a dictionary of explanations will be returned where the keys are labels from the index of `record_id_pairs`.\n    If False a single explanation will be returned (an exception is raised if `len(record_id_pairs) > 1`).\n    If None it will return a single explanation if `len(record_id_pairs)` and a dictionary otherwise.\n\n#### Returns\n`lemon.MatchingAttributionExplanation` isntance or an `Dict[any, lemon.MatchingAttributionExplanation]`,\ndepending on the input to the `return_dict` parameter.\n\n\n### lemon.MatchingAttributionExplanation\n\n#### Attributes\n- **record_pair** : pd.DataFrame\n- **string_representation** : Dict[Tuple, Union[None, str, TokenizedString]],\n- **attributions** : List[Attribution],\n- **prediction_score** : float\n- **dual** : bool\n- **metadata** : Dict[str, any]\n\n#### Methods\n- **save(path: str = None) -> Optional[Dict]**\n  - Save the explanation to a json file.\n    If path is not specified a json-serializable dictionary will be returned.\n    Requires pyarrow to be installed (`pip install lemon-explain[storage]`).\n- **static load(path: Union[str, Dict]) -> MatchingAttributionExplanation**\n  - Load an explanation from a json file.\n    Instead of a path, one can instead provide a json-serializable dictionary.\n    Requires pyarrow to be installed (`pip install lemon-explain[storage]`).\n\n### lemon.Attribution\n\n#### Attributes\n- **weight**: float\n- **potential**: Optional[float]\n- **positions**: List[Union[Tuple[str, str, str, Optional[int]]]]\n- **name**: Optional[str]\n',
    'author': 'Nils Barlaug',
    'author_email': 'nils.barlaug@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NilsBarlaug/lemon',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
