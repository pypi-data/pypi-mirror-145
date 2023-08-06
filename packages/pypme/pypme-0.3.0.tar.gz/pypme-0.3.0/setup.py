# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypme']

package_data = \
{'': ['*']}

install_requires = \
['investpy>=1.0.8,<2.0.0',
 'numpy-financial>=1.0.0,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'xirr>=0.1.8,<0.2.0']

setup_kwargs = {
    'name': 'pypme',
    'version': '0.3.0',
    'description': 'Python package for PME (Public Market Equivalent) calculation',
    'long_description': '# pypme – Python package for PME (Public Market Equivalent) calculation\n\nBased on the [Modified PME\nmethod](https://en.wikipedia.org/wiki/Public_Market_Equivalent#Modified_PME).\n\n## Example\n\n```python\nfrom pypme import verbose_xpme\nfrom datetime import date\n\npmeirr, assetirr, df = verbose_xpme(\n    dates=[date(2015, 1, 1), date(2015, 6, 12), date(2016, 2, 15)],\n    cashflows=[-10000, 7500],\n    prices=[100, 120, 100],\n    pme_prices=[100, 150, 100],\n)\n```\n\nWill return `0.5525698793027238` and  `0.19495150355969598` for the IRRs and produce this\ndataframe:\n\n![Example dataframe](https://raw.githubusercontent.com/ymyke/pypme/main/images/example_df.png)\n\nNotes:\n- The `cashflows` are interpreted from a transaction account that is used to buy from an\n  asset at price `prices`.\n- The corresponding prices for the PME are `pme_prices`.\n- The `cashflows` is extended with one element representing the remaining value, that\'s\n  why all the other lists (`dates`, `prices`, `pme_prices`) need to be exactly 1 element\n  longer than `cashflows`.\n\n## Variants\n\n- `xpme`: Calculate PME for unevenly spaced / scheduled cashflows and return the PME IRR\n  only. In this case, the IRR is always annual.\n- `verbose_xpme`: Calculate PME for unevenly spaced / scheduled cashflows and return\n  vebose information.\n- `pme`: Calculate PME for evenly spaced cashflows and return the PME IRR only. In this\n  case, the IRR is for the underlying period.\n- `verbose_pme`: Calculate PME for evenly spaced cashflows and return vebose\n  information.\n- `investpy_xpme` and `investpy_verbose_xpme`: Use price information from Investing.com.\n  See below.\n\n## Investpy examples -- using investpy to retrieve PME prices online\n\nUse `investpy_xpme` and `investpy_verbose_xpme` to use a ticker from Investing.com and\ncompare with those prices. Like so:\n\n```python\nfrom datetime import date\nfrom pypme import investpy_xpme\n\ncommon_args = {\n    "dates": [date(2012, 1, 1), date(2013, 1, 1)],\n    "cashflows": [-100],\n    "prices": [1, 1],\n}\nprint(investpy_xpme(pme_ticker="Global X Lithium", pme_type="etf", **common_args))\nprint(investpy_xpme(pme_ticker="bitcoin", pme_type="crypto", **common_args))\nprint(investpy_xpme(pme_ticker="SRENH", pme_type="stock", pme_country="switzerland", **common_args))\n```\n\nProduces:\n\n```\n-0.02834024870462727\n1.5031336254547634\n0.3402634808264912\n```\n\nThe investpy functions take the following parameters:\n- `pme_type`: One of `stock`, `etf`, `fund`, `crypto`, `bond`, `index`, `certificate`.\n  Defaults to `stock`.\n- `pme_ticker`: The ticker symbol/name.\n- `pme_country`: The ticker\'s country of residence. Defaults to `united states`.\n\nCheck out [the Investpy project](https://github.com/alvarobartt/investpy) for more\ndetails.\n\n\n## Garbage in, garbage out\n\nNote that the package will only perform essential sanity checks and otherwise just works\nwith what it gets, also with nonsensical data. E.g.:\n\n```python\nfrom pypme import verbose_pme\n\npmeirr, assetirr, df = verbose_pme(\n    cashflows=[-10, 500], prices=[1, 1, 1], pme_prices=[1, 1, 1]\n)\n```\n\nResults in this df and IRRs of 0:\n\n![Garbage example df](https://raw.githubusercontent.com/ymyke/pypme/main/images/garbage_example_df.png)\n\n## References\n\n- [Google Sheet w/ reference calculation](https://docs.google.com/spreadsheets/d/1LMSBU19oWx8jw1nGoChfimY5asUA4q6Vzh7jRZ_7_HE/edit#gid=0)\n- [Modified PME on Wikipedia](https://en.wikipedia.org/wiki/Public_Market_Equivalent#Modified_PME)\n',
    'author': 'ymyke',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ymyke/pypme',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
