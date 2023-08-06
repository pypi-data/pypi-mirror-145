# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['cron_task']
setup_kwargs = {
    'name': 'cron-task',
    'version': '0.1.0',
    'description': 'Script runner based on interval',
    'long_description': None,
    'author': 'Ngalim Siregar',
    'author_email': 'ngalim.siregar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
