# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['afluent']

package_data = \
{'': ['*']}

install_requires = \
['console>=0.9907,<0.9908',
 'coverage>=6.3,<7.0',
 'libcst>=0.4.1,<0.5.0',
 'pytest>=6.2.5,<7.0.0',
 'radon>=5.1.0,<6.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'types-tabulate>=0.8.5,<0.9.0']

entry_points = \
{'pytest11': ['afluent = afluent.main']}

setup_kwargs = {
    'name': 'afluent',
    'version': '0.2.0',
    'description': 'Automated Fault Localization Plugin for Pytest',
    'long_description': '# AFLuent\n\nSpectrum Based Fault Localization Plugin for PyTest\n\n## UNDER CONSTRUCTION\n\nThis project is a work in progress, documentation will be published soon\n',
    'author': 'Noor Buchi',
    'author_email': 'buchin@allegheny.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/noorbuchi/AFLuent',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
