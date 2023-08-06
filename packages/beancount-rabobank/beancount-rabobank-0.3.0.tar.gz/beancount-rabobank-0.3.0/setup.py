# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beancount_rabobank']

package_data = \
{'': ['*'], 'beancount_rabobank': ['test_files/*']}

setup_kwargs = {
    'name': 'beancount-rabobank',
    'version': '0.3.0',
    'description': 'Beancount importer for Rabobank CSV exports',
    'long_description': '# Beancount Rabobank CSV Importer\n\n`beancount-rabobank` provides an importer for converting CSV exports of\n[Rabobank] (Netherlands) account summaries to the [Beancount] format.\n\n## Installation\n\n```sh\n$ pip install beancount-rabobank\n```\n\n## Usage\n\nIf you\'re not familiar with how to import external data into Beancount, please\nread [this guide] first.\n\nAdjust your [config file] to include the provided `rabobank.Importer` class.\nA sample configuration might look like the following:\n\n```python\nfrom beancount_rabobank import rabobank\n\nCONFIG = [\n    # ...\n    rabobank.Importer("EUR", "Assets:Liquid:Rabobank:Checkings")\n    # ...\n]\n```\n\nOnce this is in place, you should be able to run `bean-extract` on the command\nline to extract the transactions and pipe all of them into your Beancount file.\nIt should also work in fava using the same configuration.\n\n```sh\n$ bean-extract /path/to/config.py transaction.csv >> you.beancount\n```\n\nThis importer works with [smart-importer] which will auto suggest postings based\non machine learning, which is lovely. In this case a config can look like this:\n\n```python\nfrom smart_importer import apply_hooks, PredictPostings\nfrom beancount_rabobank import rabobank\n\nCONFIG = [\n    # ...\n    apply_hooks(rabobank.Importer(\n        "EUR", "Assets:Liquid:Rabobank:Checkings"), [PredictPostings()])\n    # ...\n]\n```\n\n## Contributing\n\nContributions are most welcome!\n\nPlease make sure you have Python 3.9+ and [Poetry] installed.\n\n1. Clone the repository\n2. If you want to develop using VSCode run the following command: `poetry config virtualenvs.in-project true`\n3. Install the packages required for development: `poetry install`\n4. That\'s basically it. You should now be able to run the test suite: `poetry run py.test`.\n\n[beancount]: http://furius.ca/beancount/\n[config file]: https://beancount.github.io/docs/importing_external_data.html#configuration\n[rabobank]: https://www.rabobank.nl/\n[poetry]: https://python-poetry.org/\n[this guide]: https://beancount.github.io/docs/importing_external_data.html\n[smart-importer]: https://github.com/beancount/smart_importer\n',
    'author': 'Marijn van Aerle',
    'author_email': 'marijn.vanaerle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mvaerle/beancount-rabobank',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
