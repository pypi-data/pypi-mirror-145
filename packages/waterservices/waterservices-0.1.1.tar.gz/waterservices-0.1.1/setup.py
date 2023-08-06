# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['waterservices', 'waterservices.nwis']

package_data = \
{'': ['*']}

install_requires = \
['dask>=2022.2.0,<2023.0.0',
 'pandas>=1.3.5,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'tqdm>=4.64.0,<5.0.0']

setup_kwargs = {
    'name': 'waterservices',
    'version': '0.1.1',
    'description': 'A pyhton package to work with WaterServices USGS',
    'long_description': "# WATERSERVICES\n\nA pyhton package to work with WaterServices USGS\n\nMy Personal Website: [Water Directory](https://waterdirectory.ir/).\n\n\nTo import, use command below:\n\n```bash\nfrom waterservices import NWIS\n```\n\nAvailable functions:\n- siteInfo()\n\n\n## Get a csv file for site info of any type\n\n```bash\ncolumns = ['site_no', 'station_nm', 'dec_lat_va', 'dec_long_va', 'huc_cd', 'data_type_cd',\n        'parm_cd', 'stat_cd', 'begin_date', 'end_date']\nfilters = {\n    'seriesCatalogOutput': 'true',\n    'outputDataTypeCd': 'dv,pk,gw',\n    'siteStatus': 'all',\n    'hasDataTypeCd': 'dv,gw'\n}\nnwis = NWIS('GW', ['01'], filters, columns, 'wells').siteInfo()\n```\n\nYou can customize columns, filters, stationType, and HUC code.",
    'author': 'javad-rzvn',
    'author_email': 'javad.rezvanpour@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/javad-rzvn/waterservices',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
