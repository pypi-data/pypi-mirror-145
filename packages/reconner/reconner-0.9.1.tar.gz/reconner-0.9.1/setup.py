# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['recon', 'recon.cli', 'recon.operations', 'recon.prodigy']

package_data = \
{'': ['*'], 'recon.prodigy': ['templates/*']}

install_requires = \
['numpy>=1.22.0,<1.23.0',
 'scipy>=1.8.0,<1.9',
 'spacy>=3.2.0,<3.4.0',
 'xxhash>=3.0.0,<3.1.0']

entry_points = \
{'console_scripts': ['recon = recon.cli:app'],
 'prodigy_recipes': ['recon.ner_correct = recon:prodigy_recipes.ner_correct',
                     'recon.ner_merge = recon:prodigy_recipes.ner_merge']}

setup_kwargs = {
    'name': 'reconner',
    'version': '0.9.1',
    'description': 'Recon NER, Debug and correct annotated Named Entity Recognition (NER) data for inconsitencies and get insights on improving the quality of your data.',
    'long_description': None,
    'author': 'Kabir Khan',
    'author_email': 'kabirkhan1137@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://kabirkhan.github.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
