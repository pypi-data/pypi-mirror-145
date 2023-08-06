# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gcloud', 'gcloud.rest', 'gcloud.rest.bigquery']

package_data = \
{'': ['*']}

install_requires = \
['gcloud-rest-auth>=3.1.0,<5.0.0']

setup_kwargs = {
    'name': 'gcloud-rest-bigquery',
    'version': '6.0.0',
    'description': 'Python Client for Google Cloud BigQuery',
    'long_description': "(Asyncio OR Threadsafe) Python Client for Google Cloud BigQuery\n===============================================================\n\n    This is a shared codebase for ``gcloud-rest-bigquery`` and\n    ``gcloud-rest-bigquery``\n\n|pypi| |pythons-aio| |pythons-rest|\n\nInstallation\n------------\n\n.. code-block:: console\n\n    $ pip install --upgrade gcloud-{aio,rest}-bigquery\n\nUsage\n-----\n\nWe're still working on documentation -- for now, you can use the `smoke test`_\nas an example.\n\nEmulators\n~~~~~~~~~\n\nFor testing purposes, you may want to use ``gcloud-rest-bigquery`` along with a\nlocal emulator. Setting the ``$BIGQUERY_EMULATOR_HOST`` environment variable\nto the address of your emulator should be enough to do the trick.\n\nContributing\n------------\n\nPlease see our `contributing guide`_.\n\n.. _contributing guide: https://github.com/talkiq/gcloud-rest/blob/master/.github/CONTRIBUTING.rst\n.. _smoke test: https://github.com/talkiq/gcloud-rest/blob/master/bigquery/tests/integration/smoke_test.py\n\n.. |pypi| image:: https://img.shields.io/pypi/v/gcloud-rest-bigquery.svg?style=flat-square\n    :alt: Latest PyPI Version (gcloud-rest-bigquery)\n    :target: https://pypi.org/project/gcloud-rest-bigquery/\n\n.. |pythons-aio| image:: https://img.shields.io/pypi/pyversions/gcloud-rest-bigquery.svg?style=flat-square&label=python (aio)\n    :alt: Python Version Support (gcloud-rest-bigquery)\n    :target: https://pypi.org/project/gcloud-rest-bigquery/\n\n.. |pythons-rest| image:: https://img.shields.io/pypi/pyversions/gcloud-rest-bigquery.svg?style=flat-square&label=python (rest)\n    :alt: Python Version Support (gcloud-rest-bigquery)\n    :target: https://pypi.org/project/gcloud-rest-bigquery/\n",
    'author': 'Vi Engineering',
    'author_email': 'voiceai-eng@dialpad.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/talkiq/gcloud-aio',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
