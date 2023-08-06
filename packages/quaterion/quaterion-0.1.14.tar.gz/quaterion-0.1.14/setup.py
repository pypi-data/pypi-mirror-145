# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quaterion',
 'quaterion.dataset',
 'quaterion.distances',
 'quaterion.eval',
 'quaterion.eval.group',
 'quaterion.eval.pair',
 'quaterion.loss',
 'quaterion.loss.extras',
 'quaterion.train',
 'quaterion.train.cache',
 'quaterion.utils']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.3,<0.6.0',
 'mmh3>=3.0.0,<4.0.0',
 'pytorch-lightning>=1.5.8,<2.0.0',
 'quaterion-models>=0.1.5',
 'torch>=1.8.2']

extras_require = \
{'pytorch-metric-learning': ['pytorch-metric-learning>=1.2.1,<2.0.0']}

setup_kwargs = {
    'name': 'quaterion',
    'version': '0.1.14',
    'description': 'Metric Learning fine-tuning framework',
    'long_description': "# Quaterion\n\n>  A dwarf on a giant's shoulders sees farther of the two \n\nA tool collection and framework for fine-tuning metric learning model. \n",
    'author': 'generall',
    'author_email': 'andrey@vasnetsov.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/qdrant/quaterion',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
