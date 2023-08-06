# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['getdeck',
 'getdeck.api',
 'getdeck.deckfile',
 'getdeck.provider',
 'getdeck.provider.k3d',
 'getdeck.provider.kubectl',
 'getdeck.sources']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.27,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'docker>=5.0.3,<6.0.0',
 'kubernetes>=23.3.0,<24.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'semantic-version>=2.9.0,<3.0.0']

entry_points = \
{'console_scripts': ['deck = getdeck.__main__:main',
                     'setversion = version:set_version']}

setup_kwargs = {
    'name': 'getdeck',
    'version': '0.3.0',
    'description': 'Deck, a CLI that creates reproducible Kubernetes environments for development and testing',
    'long_description': '# deck\nA CLI that creates reproducible Kubernetes environments for development and testin\n',
    'author': 'Michael Schilonka',
    'author_email': 'michael@unikube.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://getdeck.dev',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
