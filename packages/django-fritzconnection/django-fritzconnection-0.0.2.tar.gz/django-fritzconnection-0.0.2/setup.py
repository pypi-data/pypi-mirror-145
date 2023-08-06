# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djfritz',
 'djfritz.admin',
 'djfritz.management',
 'djfritz.management.commands',
 'djfritz.migrations',
 'djfritz.models',
 'djfritz.services',
 'djfritz.templatetags',
 'djfritz.tests',
 'djfritz.tests.fixtures',
 'djfritz.views',
 'djfritz_project',
 'djfritz_project.settings',
 'djfritz_project.tests']

package_data = \
{'': ['*'],
 'djfritz': ['locale/de/LC_MESSAGES/*',
             'locale/en/LC_MESSAGES/*',
             'templates/admin/djfritz/hostmodel/*',
             'templates/djfritz/*',
             'templates/djfritz/includes/*'],
 'djfritz_project': ['templates/admin/*']}

install_requires = \
['bx_django_utils',
 'bx_py_utils',
 'colorlog',
 'django',
 'django-admin-sortable2',
 'django-debug-toolbar',
 'django-reversion-compare',
 'django-tagulous',
 'django-tools',
 'fritzconnection']

entry_points = \
{'console_scripts': ['devshell = djfritz_project.dev_shell:devshell_cmdloop',
                     'run_testserver = '
                     'djfritz_project.manage:start_test_server']}

setup_kwargs = {
    'name': 'django-fritzconnection',
    'version': '0.0.2',
    'description': 'Web based FritzBox management using Python/Django.',
    'long_description': '# django-fritzconnection\n\n![django-fritzconnection @ PyPi](https://img.shields.io/pypi/v/django-fritzconnection?label=django-fritzconnection%20%40%20PyPi)\n![Python Versions](https://img.shields.io/pypi/pyversions/django-fritzconnection)\n![License GPL V3+](https://img.shields.io/pypi/l/django-fritzconnection)\n\nWeb based FritzBox management using Python/Django and the great [fritzconnection](https://github.com/kbr/fritzconnection) library.\n\nThe destination is Web based management of "WAN access" for hosts groups.\nThe idea is to collect hosts, group them and be able to quick change WAN access for all hosts of a group...\n\nCurrent state: **early development stage**\n\nExisting features:\n\n* actions:\n  * Change WAN access of a host\n* models:\n  * HostModel\n    * "Static" storage for all `FritzHosts().get_hosts_info()` information\n    * Update in Admin via change list tools link and manage command\n* a few "test" views:\n  * Host information\n    * Get information about registered hosts\n    * Get raw mesh topology\n  * Diagnose\n    * Test FritzBox connection\n    * List all FritzBox services\n\n\n[![Install django-fritzconnection with YunoHost](https://install-app.yunohost.org/install-with-yunohost.svg)](https://install-app.yunohost.org/?app=django-fritzconnection)\n\n> *This package allows you to install django-fritzconnection quickly and simply on a YunoHost server.\nIf you don\'t have YunoHost, please consult [the guide](https://yunohost.org/#/install) to learn how to install it.*\n\nPull requests welcome ;)\n\n\n## Quick start for developers\n\n```\n~$ git clone https://github.com/jedie/django-fritzconnection.git\n~$ cd django-fritzconnection\n~/django-fritzconnection$ ./devshell.py\n...\nDeveloper shell - djfritz - v0.0.2\n...\n\n(djfritz) run_testserver\n```\n\n## versions\n\n* [*dev*](https://github.com/jedie/django-fritzconnection/compare/v0.0.2.rc1...main)\n  * TBC\n* [v0.0.2 - 04.04.2022](https://github.com/jedie/django-fritzconnection/compare/v0.0.1-alpha...v0.0.2)\n  * Store Host information\n  * Possible to set WAN access for one host\n* v0.0.1-alpha - 24.03.2022\n  * init the project\n',
    'author': 'JensDiemer',
    'author_email': 'git@jensdiemer.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jedie/django-fritzconnection',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0.0',
}


setup(**setup_kwargs)
