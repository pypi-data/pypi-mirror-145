# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kfp_toolbox']

package_data = \
{'': ['*']}

install_requires = \
['kfp>=1.8,<2.0']

setup_kwargs = {
    'name': 'kfp-toolbox',
    'version': '0.0.0',
    'description': 'The toolbox for kfp (Kubeflow Pipelines)',
    'long_description': '# kfp-toolbox\nThe toolbox for kfp (Kubeflow Pipelines)\n',
    'author': 'Takahiro Yano',
    'author_email': 'speg03@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/speg03/kfp-toolbox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
