# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wccls']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1', 'beautifulsoup4>=4.9.3', 'requests>=2.25.1']

extras_require = \
{':python_version >= "3.10" and python_version < "4"': ['urllib3>=1.26']}

setup_kwargs = {
    'name': 'wccls',
    'version': '3.1.0',
    'description': 'Scraper for the WCCLS account page',
    'long_description': '# Overview\n\nThis is a read-only scraper for the [WCCLS](https://wccls.bibliocommons.com) account page. It also works for the [Multnomah County Bibliocommons site](https://multcolib.bibliocommons.com)\n\n# Usage\n\n![image](https://github.com/rkhwaja/wccls/workflows/ci/badge.svg) [![codecov](https://codecov.io/gh/rkhwaja/wccls/branch/master/graph/badge.svg)](https://codecov.io/gh/rkhwaja/wccls)\n\n``` python\nfrom wccls import Wccls, WcclsAsync\nitems = Wccls(login=card_number_or_username, password=password)\nfor item in items:\n    print(item)\n\nitems = await WcclsAsync(login=card_number_or_username, password=password)\nfor item in items:\n    print(item)\n```\n\n# Running tests\n\n## Run against the live website\n\n- Set the environment variables to show what the expected counts are for the various categories\n\n- Run\n```bash\npytest\n```\n\n## To record new test data\nSet SCRUB_EMAIL, WCCLS_CARD_NUMBER, WCCLS_PASSWORD environment variables\n``` python\npytest --collect=save\n```\n\n## To test existing test data\n``` python\npytest\n```\n',
    'author': 'Rehan Khwaja',
    'author_email': 'rehan@khwaja.name',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rkhwaja/wccls',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
