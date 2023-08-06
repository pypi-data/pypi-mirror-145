# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ogc', 'ogc.commands', 'ogc.tests']

package_data = \
{'': ['*']}

install_requires = \
['Mako>=1.1.6,<2.0.0',
 'PyYAML>=6.0,<7.0',
 'SQLAlchemy>=1.4.32,<2.0.0',
 'alembic>=1.7.7,<2.0.0',
 'apache-libcloud>=3.5.0,<4.0.0',
 'arrow>=1.2.2,<2.0.0',
 'attrs>=21.4.0,<22.0.0',
 'click-didyoumean>=0.3.0,<0.4.0',
 'click>=8.0.4,<9.0.0',
 'colorama>=0.4.4,<0.5.0',
 'dict-deep>=4.1.2,<5.0.0',
 'humanfriendly>=10.0,<11.0',
 'melddict>=1.0.1,<2.0.0',
 'paramiko>=2.9.2,<3.0.0',
 'psycopg2-binary>=2.9.3,<3.0.0',
 'python-dotenv>=0.19.2,<0.20.0',
 'python-slugify>=6.1.1,<7.0.0',
 'retry>=0.9.2,<0.10.0',
 'rich>=12.0.1,<13.0.0',
 'sh>=1.14.2,<2.0.0']

entry_points = \
{'console_scripts': ['ogc = ogc.commands.base:start']}

setup_kwargs = {
    'name': 'ogc',
    'version': '2.1.7',
    'description': 'Provisioner, no more, no less.',
    'long_description': "# OGC\n\nogc - provisioning, that's it.\n\n# Get started\n\n- [Getting Started Guide](https://adam-stokes.github.io/ogc/)\n- User Guide\n  -  [Managing Deployment](https://adam-stokes.github.io/ogc/user-guide/managing-nodes/)\n  -  [Defining Layouts](https://adam-stokes.github.io/ogc/user-guide/defining-layouts/)\n  -  [Scripting](https://adam-stokes.github.io/ogc/user-guide/scripting/)\n# License\n\nMIT.\n\n\n",
    'author': 'Adam Stokes',
    'author_email': '51892+adam-stokes@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/adam-stokes/ogc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
