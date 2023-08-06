# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yapapi',
 'yapapi.contrib',
 'yapapi.contrib.service',
 'yapapi.contrib.strategy',
 'yapapi.executor',
 'yapapi.package',
 'yapapi.payload',
 'yapapi.props',
 'yapapi.rest',
 'yapapi.script',
 'yapapi.services',
 'yapapi.storage',
 'yapapi.strategy']

package_data = \
{'': ['*']}

install_requires = \
['Deprecated>=1.2.12,<2.0.0',
 'aiohttp-sse-client>=0.1.7,<0.2.0',
 'aiohttp>=3.6,<4.0',
 'async_exit_stack>=1.0.1,<2.0.0',
 'attrs>=19.3',
 'colorama>=0.4.4,<0.5.0',
 'jsonrpc-base>=1.0.3,<2.0.0',
 'more-itertools>=8.6.0,<9.0.0',
 'python-statemachine>=0.8.0,<0.9.0',
 'semantic-version>=2.8,<3.0',
 'srvresolver>=0.3.5,<0.4.0',
 'toml>=0.10.1,<0.11.0',
 'typing_extensions>=3.10.0,<4.0.0',
 'urllib3>=1.25.9,<2.0.0',
 'ya-aioclient>=0.6.3,<0.7.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.8,<0.9'],
 'docs': ['sphinx>=4.0.1,<5.0.0',
          'sphinx-autodoc-typehints>=1.12.0,<2.0.0',
          'sphinx-rtd-theme>=1.0.0,<2.0.0'],
 'integration-tests': ['pexpect>=4.8.0,<5.0.0'],
 'integration-tests:python_version >= "3.8.0" and python_version < "4.0.0"': ['goth>=0.10,<0.11']}

setup_kwargs = {
    'name': 'yapapi',
    'version': '0.9.0',
    'description': 'High-level Python API for the New Golem',
    'long_description': '# Golem Python API\n\n[![Tests - Status](https://img.shields.io/github/workflow/status/golemfactory/yapapi/Continuous%20integration/master?label=tests)](https://github.com/golemfactory/yapapi/actions?query=workflow%3A%22Continuous+integration%22+branch%3Amaster)\n[![Docs status](https://readthedocs.org/projects/yapapi/badge/?version=latest)](https://yapapi.readthedocs.io/en/latest/)\n![PyPI - Status](https://img.shields.io/pypi/status/yapapi)\n[![PyPI version](https://badge.fury.io/py/yapapi.svg)](https://badge.fury.io/py/yapapi)\n[![GitHub license](https://img.shields.io/github/license/golemfactory/yapapi)](https://github.com/golemfactory/yapapi/blob/master/LICENSE)\n[![GitHub issues](https://img.shields.io/github/issues/golemfactory/yapapi)](https://github.com/golemfactory/yapapi/issues)\n\n## What\'s Golem and yapapi?\n\n**[Golem](https://golem.network)** is a global, open-source, decentralized supercomputer that anyone can access.\nIt connects individual machines to form a vast network which combines their resources and allows requestors to utilize its unique potential - which may be its combined computing power, storage, the geographical distribution or its censorship resistance.\n\n**Yapapi** is the Python high-level API that allows developers to connect to their Golem nodes and manage their distributed, computational loads through Golem Network.\n\n## Golem application development\n\nFor a detailed introduction to using Golem and yapapi to run your tasks on Golem and a guide to Golem Network application development in general, [please consult our handbook](https://handbook.golem.network/requestor-tutorials/flash-tutorial-of-requestor-development).\n\n\n### Installation\n\n`yapapi` is available as a [PyPI package](https://pypi.org/project/yapapi/).\n\nYou can install it through `pip`:\n```\npip install yapapi\n```\n\nOr if your project uses [`poetry`](https://python-poetry.org/) you can add it to your dependencies like this:\n```\npoetry add yapapi\n```\n\n### API Reference\n\nFor a comprehensive API reference, please refer to [our official readthedocs page](https://yapapi.readthedocs.io/).\n\n## Local setup for yapapi developers\n\n### Poetry\n`yapapi` uses [`poetry`](https://python-poetry.org/) to manage its dependencies and provide a runner for common tasks.\n\nIf you don\'t have `poetry` available on your system then follow its [installation instructions](https://python-poetry.org/docs/#installation) before proceeding.\nVerify your installation by running:\n```\npoetry --version\n```\n\n### Project dependencies\nTo install the project\'s dependencies run:\n```\npoetry install\n```\nBy default, `poetry` looks for the required Python version on your `PATH` and creates a virtual environment for the project if there\'s none active (or already configured by Poetry).\n\nAll of the project\'s dependencies will be installed to that virtual environment.\n\n### Running `goth` integration tests\n\n#### Prerequisites\n\nIf you\'d like to run the `yapapi` integration test suite locally then you\'ll need to install an additional set of dependencies separately.\n\nFirst, install [the dependencies required to run goth](https://github.com/golemfactory/goth#requirements).\n\nNext, [configure goth\'s GitHub API token](https://github.com/golemfactory/goth#getting-a-github-api-token).\n\nNow, you can install goth and its additional python requirements:\n\n```\npoetry install -E integration-tests\n```\n\nFinally, generate goth\'s default assets:\n\n```\npoetry run poe goth-assets\n```\n\n#### Running the tests\n\nOnce you have the environment set up, to run all the integration tests, use:\n\n```\npoetry run poe goth-tests\n```\n\n## See also\n\n* [Golem](https://golem.network), a global, open-source, decentralized supercomputer that anyone can access.\n* Learn what you need to know to set-up your Golem requestor node:\n    * [Requestor development: a quick primer](https://handbook.golem.network/requestor-tutorials/flash-tutorial-of-requestor-development)\n    * [Run first task on Golem](https://handbook.golem.network/requestor-tutorials/flash-tutorial-of-requestor-development/run-first-task-on-golem)\n* Have a look at the most important concepts behind any Golem application: [Golem application fundamentals](https://handbook.golem.network/requestor-tutorials/golem-application-fundamentals)\n* Learn about preparing your own Docker-like images for the [VM runtime](https://handbook.golem.network/requestor-tutorials/vm-runtime)\n* Write your own app with yapapi:\n    * [Task Model development](https://handbook.golem.network/requestor-tutorials/task-processing-development)\n    * [Service Model development](https://handbook.golem.network/requestor-tutorials/service-development)\n\n## Environment variables\n\nIt\'s possible to set various elements of `yagna` configuration through environment variables.\n`yapapi` currently supports the following environment variables:\n- `YAGNA_ACTIVITY_URL`, URL to `yagna` activity API, e.g. `http://localhost:7500/activity-api/v1`\n- `YAGNA_API_URL`, base URL to `yagna` REST API, e.g. `http://localhost:7500`\n- `YAGNA_APPKEY`, `yagna` app key to be used, e.g. `a70facb9501d4528a77f25574ab0f12b`\n- `YAGNA_MARKET_URL`, URL to `yagna` market API, e.g. `http://localhost:7500/market-api/v1`\n- `YAGNA_PAYMENT_NETWORK`, Ethereum network name for `yagna` to use, e.g. `rinkeby`\n- `YAGNA_PAYMENT_DRIVER`, payment driver name for `yagna` to use, e.g. `erc20`\n- `YAGNA_PAYMENT_URL`, URL to `yagna` payment API, e.g. `http://localhost:7500/payment-api/v1`\n- `YAGNA_SUBNET`, name of the `yagna` sub network to be used, e.g. `devnet-beta`\n- `YAPAPI_USE_GFTP_CLOSE`, if set to a _truthy_ value (e.g. "1", "Y", "True", "on") then `yapapi`\n  will ask `gftp` to close files when there\'s no need to publish them any longer. This may greatly\n  reduce the number of files kept open while `yapapi` is running but requires `yagna`\n  0.7.3 or newer, with older versions it will cause errors.\n',
    'author': 'Przemysław K. Rekucki',
    'author_email': 'przemyslaw.rekucki@golem.network',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/golemfactory/yapapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
