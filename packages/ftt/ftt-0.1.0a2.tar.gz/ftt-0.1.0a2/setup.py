# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ftt',
 'ftt.brokers',
 'ftt.brokers.handlers',
 'ftt.brokers.handlers.steps',
 'ftt.brokers.ib',
 'ftt.cli',
 'ftt.cli.commands',
 'ftt.cli.handlers',
 'ftt.cli.handlers.steps',
 'ftt.cli.renderers',
 'ftt.cli.renderers.portfolio_versions',
 'ftt.cli.renderers.portfolios',
 'ftt.cli.renderers.securities',
 'ftt.cli.renderers.weights',
 'ftt.handlers',
 'ftt.handlers.handler',
 'ftt.handlers.order_steps',
 'ftt.handlers.portfolio_steps',
 'ftt.handlers.portfolio_version_steps',
 'ftt.handlers.position_steps',
 'ftt.handlers.securities_steps',
 'ftt.handlers.security_prices_steps',
 'ftt.handlers.weights_steps',
 'ftt.portfolio_management',
 'ftt.storage',
 'ftt.storage.data_objects',
 'ftt.storage.mappers',
 'ftt.storage.models',
 'ftt.storage.repositories']

package_data = \
{'': ['*'], 'ftt': ['config/*']}

install_requires = \
['Riskfolio-Lib>=2.0.0,<3.0.0',
 'SQLAlchemy>=1.4.31,<2.0.0',
 'Yahoo-ticker-downloader>=3.0.1,<4.0.0',
 'cvxopt==1.2.7',
 'ibapi>=9.81.1,<10.0.0',
 'pandas>=1.4.0,<2.0.0',
 'pandas_datareader>=0.9,<0.10',
 'peewee>=3.14.0,<4.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'pyinstrument>=4.1.1,<5.0.0',
 'pyportfolioopt>=1.2.7,<2.0.0',
 'python-nubia>=0.2b5,<0.3',
 'pyyaml>=6.0,<7.0',
 'result>=0.7.0,<0.8.0',
 'rich>=11.1,<12.0',
 'yfinance>=0.1.54,<0.2.0']

entry_points = \
{'console_scripts': ['ftt = ftt:__main__']}

setup_kwargs = {
    'name': 'ftt',
    'version': '0.1.0a2',
    'description': 'Financial Trading Tool (FTT) – is an asset management application that helps to make the right decision on time.',
    'long_description': '# Financial Trading Tools (FTT)\n\n> Finance is hard. Programming is hard.\n\n![PyPI](https://img.shields.io/pypi/v/ftt)\n[![Testing](https://github.com/ftt-project/ftt/actions/workflows/testing.yml/badge.svg)](https://github.com/ftt-project/ftt/actions/workflows/testing.yml)\n[![Linting](https://github.com/ftt-project/ftt/actions/workflows/linting.yml/badge.svg)](https://github.com/ftt-project/ftt/actions/workflows/linting.yml)\n![GitHub](https://img.shields.io/github/license/ftt-project/ftt)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ftt)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/ftt-project/ftt.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/ftt-project/ftt/context:python)\n\nFTT is a financial asset management application that helps to make right decision on time.\n\n## Mission\n\nTo enable every private investor to make a rational algorithmic decision.\n\n## Vision\n\nTo create a compelling service that provides private investors opportunities to cast their investing believes through prism of statistic and analysis.\n\n## Problem statement\n\nFTT solves a concrete problem by assembling multiple features in one place. Refer to [PROBLEM_STATEMENT](PROBLEM_STATEMENT.md) document for details.\n\n## Main features\n\n### Done\n\n* Foundation for organized data storing and viewing.\n* Calculation of weights in portfolio using multiple algorithms.\n* CLI Interface\n\n### Not done\n\n* Backtest portfolios to choose one.\n* Complement portfolio with additional securities for better balancing.\n* Initiate and control financial operations in the brokerage system.\n* Monitor portfolio performance and automatically rebalance it.\n* Take automated decisions on buy and sell operations to prevent losses.\n* Web interface\n\n\n## Collaborators\n- [Artem M](https://github.com/ignar)\n- [Ihor M](https://github.com/IhorMok)\n\n\n## Quickstart\n\n```\n$> pip install ftt\n$> ftt\nftt> example\n```\n',
    'author': 'Artem Melnykov',
    'author_email': 'melnykov.artem.v@gmail.com',
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
