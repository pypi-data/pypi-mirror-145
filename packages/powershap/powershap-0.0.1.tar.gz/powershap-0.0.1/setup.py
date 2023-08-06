# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['powershap', 'powershap.shap_wrappers']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.3,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'shap>=0.40.0,<0.41.0',
 'sklearn>=0.0,<0.1']

setup_kwargs = {
    'name': 'powershap',
    'version': '0.0.1',
    'description': 'Feature selection using statistical significance of shap values',
    'long_description': None,
    'author': 'Jarne Verhaeghe, Jeroen Van Der Donckt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
