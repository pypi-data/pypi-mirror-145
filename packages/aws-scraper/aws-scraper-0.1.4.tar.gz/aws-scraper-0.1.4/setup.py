# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_scraper']

package_data = \
{'': ['*']}

install_requires = \
['aiobotocore>=2.1.0,<3.0.0',
 'boto3<2',
 'loguru>=0.5.3,<0.6.0',
 'pandas>=1.4.1,<2.0.0',
 'python-dotenv>=0.19.2,<0.20.0',
 's3fs>=2022.1.0,<2023.0.0',
 'selenium-stealth>=1.0.6,<2.0.0',
 'selenium>=4.1.3,<5.0.0',
 'simplejson>=3.17.6,<4.0.0',
 'tryagain>=1.0,<2.0',
 'webdriver-manager>=3.5.3,<4.0.0']

entry_points = \
{'console_scripts': ['aws-scraper = aws_scraper.__main__:cli']}

setup_kwargs = {
    'name': 'aws-scraper',
    'version': '0.1.4',
    'description': 'A Python utility for submitting and running scraping jobs in parallel on AWS ECS Fargate.',
    'long_description': None,
    'author': 'Nick Hand',
    'author_email': 'nick.hand@phila.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
