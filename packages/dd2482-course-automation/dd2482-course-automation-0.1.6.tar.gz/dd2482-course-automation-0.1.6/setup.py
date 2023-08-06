# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dd2482_course_automation']

package_data = \
{'': ['*']}

install_requires = \
['pytz>=2022.1,<2023.0', 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['ddca = dd2482_course_automation:cli']}

setup_kwargs = {
    'name': 'dd2482-course-automation',
    'version': '0.1.6',
    'description': '',
    'long_description': None,
    'author': 'landeholt',
    'author_email': 'johnlan@kth.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
