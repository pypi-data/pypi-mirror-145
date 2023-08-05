# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tehran_stocks',
 'tehran_stocks.config',
 'tehran_stocks.download',
 'tehran_stocks.models']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.28,<2.0.0',
 'aiodns>=3.0.0,<4.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'cchardet>=2.1.7,<3.0.0',
 'jalali-pandas>=0.2.0,<0.3.0',
 'lxml>=4.8.0,<5.0.0',
 'pandas>=1.4.1,<2.0.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'tehran-stocks',
    'version': '1.0.0',
    'description': 'Data Downloader for Tehran stock market',
    'long_description': '# Tehran Stock Market\n\n[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)\n![PyPI - Downloads](https://img.shields.io/pypi/dw/tehran_stocks.svg?color=blue)\n[![PyPI version](https://badge.fury.io/py/tehran-stocks.svg)](https://badge.fury.io/py/tehran-stocks)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)\n\n<!-- ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tehran-stocks.svg) -->\n\nA python package that helps to access TSETMC stock price history, Using OOP Interface\n\n## Features\n\n- Download All stocks prices\n- Download prices from a group (i.e ETFs or cars, etc.)\n- Download Price history of one specific Stock\n- After first setup available offline.\n- CommandLine Interface\n- Export data to csv, excel or Stata(dta)\n- Compatible with `sqlalchemy`\n- Compatible with `PANDAS`\n- Based on light `sqlite`\n\n## 0 - Install\n\n```bash\npip install tehran_stocks\n```\n\n## 1- Initialization\n\nFor first use you need initialize the database\n\n### 1-1 Command line\n\n```bash\nts-get init  # Set up to sqlite database\n```\n\n### 1-2 Python\n\n```python\nimport tehran_stocks\n# On first import package initialize itself\n```\n\nDuring initialization you will prompt for downloading all prices. if you answer yes it will download all prices, otherwise you can download data\n\n## 2- Download and Update prices\n\n### 2-1 Command line\n\n```bash\nts-get update # update  all price , or download all if no price exist\nts-get  group 34 ## 34 is the code for car\'s group.\nts-get get_groups ## get group name and group codes\n```\n\n### 2-2 Python\n\n```python\nfrom tehran_stocks import get_all_price, Stocks, update_group\n\nget_all_price() # download and(or) update all prices\n\nupdate_group(34) #download and(or) update Stocks in groupCode = 34 (Cars)\n\nStocks.get_group() # to see list of group codes\n```\n\n## 3- Access Data\n\nTo access data you can use `Stocks` which is an customized `sqlalchemy` object, which helps you to find prices on an easy way.\n\n### 3-1 Search Stocks\n\n```python\nfrom tehran_stocks import Stocks, db\n\n# You can use query to find stocks\nstock = Stocks.query.filter_by(name=\'كگل\').first() #find by symbol(نماد)\n\nstock = Stocks.query.filter_by(code=\'35700344742885862\').first() # find by code on tsetmc url\n\nstock = Stocks.query.filter(Stocks.title.like(\'%گل گهر%\')).first() # Search by title\n\nstock_list = Stocks.query.filter_by(group_code =34).all() # find all Stocks in Khodro\n\nstock_list = Stocks.query.filter(Stocks.group_code.in_([13,34])).all() # all stocks in khodro and felezat\n\n\n## (Advanced)or run sql query using orm or raw sql\ndb.session.query(Stocks.group_code, Stocks.group_name).group_by(Stocks.group_code).all()\n\ndb.session.execute(\'select group_code , group_name from stocks group by group_name\').fetchall()\n```\n\nNow easily access stock price and do whatever you want with `pandas` dataframes:\n\n```python\n# use data as a pandas dataframe\n>>> stock.df #\n      id               code        ticker  dtyyyymmdd    first     high      low    close        value      vol  openint per     open     last       date\n0  22491  35700344742885862  Gol-E-Gohar.    20040829  12000.0  12021.0  12000.0  12000.0  18841605000  1570000     2708   D  12000.0  12000.0 2004-08-29\n\n>>> stock.summary()\nStart date: 20040829\nEnd date: 20190714\nTotal days: 2987\n\n>>> stock.update()\n# update stock price history\n\n# Export to your preferred format\n>>> stock.df.to_csv(\'price.csv\')\n>>> stock.df.to_excel(\'price.xlsx\')\n>>> stock.df.to_stata(\'price.dta\')\n\n```\n\n## Todo\n\n- [x] Create Database\n- [x] Download Data\n- [x] CommandLine Support\n- [x] Jalali Support\n\n# Donation❤️\n\nIf you like this package you can buy me a cup of coffee ☕️.\n\nYou can pay using آپ Application by scanning following qrcode in the application or entering code `95656781`:\n\n![NeshanPardakht](qrcode.png "95656781")\n\nOr donate using [IDPAY](https://idpay.ir/ghodsizadeh)\n\n',
    'author': 'Mehdi Ghodsizadeh',
    'author_email': 'mehdi.ghodsizadeh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://ghodsizadeh.github.io/tehran-stocks/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
