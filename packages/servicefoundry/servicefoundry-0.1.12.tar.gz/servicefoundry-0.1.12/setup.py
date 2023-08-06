# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['servicefoundry',
 'servicefoundry.build',
 'servicefoundry.build.clients',
 'servicefoundry.build.local_deploy',
 'servicefoundry.build.model',
 'servicefoundry.build.package',
 'servicefoundry.build.package.docker_template',
 'servicefoundry.build.parser',
 'servicefoundry.build.remote_deploy',
 'servicefoundry.cli',
 'servicefoundry.cli.servicedef']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0',
 'PyJWT>=2.3.0,<3.0.0',
 'PyYAML>=6.0,<7.0',
 'click>=8.0.4,<9.0.0',
 'fastapi>=0.75.0,<0.76.0',
 'importlib-metadata>=4.2,<5.0',
 'importlib-resources>=5.2.0,<6.0.0',
 'mistune>=0.8.4,<0.9.0',
 'prometheus_client>=0.13.1,<0.14.0',
 'python-socketio[client]>=5.5.2,<6.0.0',
 'questionary>=1.10.0,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich-click>=1.2.1,<2.0.0',
 'rich>=12.0.0,<13.0.0']

entry_points = \
{'console_scripts': ['servicefoundry = servicefoundry.__main__:main']}

setup_kwargs = {
    'name': 'servicefoundry',
    'version': '0.1.12',
    'description': 'Generate deployed services from code',
    'long_description': '# Install\n\nInstall dependencies:\n\n```python\npoetry install\n```\n\nBuild:\n\n```python\npoetry build\n```\n# Testing\n\n```\npoetry run pytest\n```\n',
    'author': 'Abhishek Choudhary',
    'author_email': 'abhichoudhary06@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/innoavator/servicefoundry',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
