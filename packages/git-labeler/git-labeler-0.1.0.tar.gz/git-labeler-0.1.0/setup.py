# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_labeler']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.27,<4.0.0',
 'pyaml>=21.10.1,<22.0.0',
 'pyfiglet>=0.8.post1,<0.9',
 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['git-labeler = git_labeler.script:main']}

setup_kwargs = {
    'name': 'git-labeler',
    'version': '0.1.0',
    'description': 'Apply, change, remove labels on multiple or single repos in one go',
    'long_description': None,
    'author': 'John Stilia',
    'author_email': 'stilia.johny@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
