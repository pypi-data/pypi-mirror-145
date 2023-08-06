# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['noaa_ftp', 'noaa_ftp.noaa']

package_data = \
{'': ['*']}

install_requires = \
['progressbar2>=4.0.0,<5.0.0']

setup_kwargs = {
    'name': 'noaa-ftp',
    'version': '0.1.11',
    'description': 'A python package to work with NOAA FTP',
    'long_description': '# NOAA-FTP\n\n> I needed to work with data from NOAA, so I write a code in jupyter notebook and solved my problem for viewing and downloading data.\n> Then I decided to convert that code to a python package.\n\nMy Personal Website: [Water Directory](https://waterdirectory.ir/).\n\n\nTo import, use command below:\n\n```bash\nfrom noaa_ftp import NOAA\n```\n\nAvailable functions:\n- dir()\n- download()\n\n## Get list of files and folders\n\n```bash\nnoaa_dir = NOAA("ftp.ncdc.noaa.gov", \'pub/data/ghcn/daily\').dir()\nnoaa_dir\n```\n\n## Download custom file from the directory\n\n```bash\nnoaa = NOAA("ftp.ncdc.noaa.gov", \'pub/data/ghcn/daily\').download(\'ghcnd-stations.txt\')\n```',
    'author': 'javad-rzvn',
    'author_email': 'javad.rezvanpour@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/javad-rzvn/noaa_ftp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
