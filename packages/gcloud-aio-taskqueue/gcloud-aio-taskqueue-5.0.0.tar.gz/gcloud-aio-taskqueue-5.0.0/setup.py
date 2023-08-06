# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gcloud', 'gcloud.aio', 'gcloud.aio.taskqueue']

package_data = \
{'': ['*']}

install_requires = \
['backoff>=1.0.0,<2.0.0', 'gcloud-aio-auth>=3.1.0,<5.0.0']

setup_kwargs = {
    'name': 'gcloud-aio-taskqueue',
    'version': '5.0.0',
    'description': 'Python Client for Google Cloud Task Queue',
    'long_description': "(Asyncio OR Threadsafe) Python Client for Google Cloud Task Queue\n=================================================================\n\n|pypi| |pythons-aio| |pythons-rest|\n\nInstallation\n------------\n\n.. code-block:: console\n\n    $ pip install --upgrade gcloud-{aio,rest}-taskqueue\n\nUsage\n-----\n\nWe're still working on documentation -- for now, you can use the `smoke tests`_\nas an example.\n\nEmulators\n~~~~~~~~~\n\nFor testing purposes, you may want to use ``gcloud-aio-taskqueue`` along with a\nlocal emulator. Setting the ``$CLOUDTASKS_EMULATOR_HOST`` environment variable\nto the address of your emulator should be enough to do the trick.\n\nContributing\n------------\n\nPlease see our `contributing guide`_.\n\n.. _contributing guide: https://github.com/talkiq/gcloud-aio/blob/master/.github/CONTRIBUTING.rst\n.. _smoke tests: https://github.com/talkiq/gcloud-aio/tree/master/taskqueue/tests/integration\n\n.. |pypi| image:: https://img.shields.io/pypi/v/gcloud-aio-taskqueue.svg?style=flat-square\n    :alt: Latest PyPI Version (gcloud-aio-taskqueue)\n    :target: https://pypi.org/project/gcloud-aio-taskqueue/\n\n.. |pythons-aio| image:: https://img.shields.io/pypi/pyversions/gcloud-aio-taskqueue.svg?style=flat-square&label=python (aio)\n    :alt: Python Version Support (gcloud-aio-taskqueue)\n    :target: https://pypi.org/project/gcloud-aio-taskqueue/\n\n.. |pythons-rest| image:: https://img.shields.io/pypi/pyversions/gcloud-rest-taskqueue.svg?style=flat-square&label=python (rest)\n    :alt: Python Version Support (gcloud-rest-taskqueue)\n    :target: https://pypi.org/project/gcloud-rest-taskqueue/\n",
    'author': 'Vi Engineering',
    'author_email': 'voiceai-eng@dialpad.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/talkiq/gcloud-aio',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
