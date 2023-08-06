# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['aws_profile = src.aws_profile:main',
                     'aws_profiles = src.aws_profile:main']}

setup_kwargs = {
    'name': 'aws-profiles',
    'version': '1.0.0',
    'description': 'Simple Script to list all named profiles in ~/.aws/config',
    'long_description': None,
    'author': 'Brian Peterson',
    'author_email': 'brian.peterson@cloudshift.cc',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cloudshiftstrategies/aws-profiles',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
