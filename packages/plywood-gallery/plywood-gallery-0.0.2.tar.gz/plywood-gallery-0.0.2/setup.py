# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plywood_gallery']

package_data = \
{'': ['*'],
 'plywood_gallery': ['jinja2_template/*',
                     'quickstart_template/*',
                     'quickstart_template/gallery_assets/*']}

install_requires = \
['Flask>=2.0.2,<3.0.0',
 'Jinja2>=3.1.1,<4.0.0',
 'Pillow>=9.0.0,<10.0.0',
 'PyYAML>=6.0,<7.0',
 'ipykernel>=6.7.0,<7.0.0',
 'ipython>=7.31.0,<8.0.0',
 'watchdog>=2.1.6,<3.0.0']

setup_kwargs = {
    'name': 'plywood-gallery',
    'version': '0.0.2',
    'description': 'Jupyter cell magic that turns images from cell output into a  gallery',
    'long_description': None,
    'author': 'kolibril13',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
