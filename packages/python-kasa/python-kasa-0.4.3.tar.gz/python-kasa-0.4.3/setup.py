# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kasa', 'kasa.tests']

package_data = \
{'': ['*'], 'kasa.tests': ['fixtures/*']}

install_requires = \
['anyio', 'asyncclick>=8', 'importlib-metadata']

extras_require = \
{'docs': ['sphinx>=3,<4',
          'm2r>=0,<1',
          'mistune<2.0.0',
          'sphinx_rtd_theme>=0,<1',
          'sphinxcontrib-programoutput>=0,<1']}

entry_points = \
{'console_scripts': ['kasa = kasa.cli:cli']}

setup_kwargs = {
    'name': 'python-kasa',
    'version': '0.4.3',
    'description': 'Python API for TP-Link Kasa Smarthome devices',
    'long_description': "# python-kasa\n\n[![PyPI version](https://badge.fury.io/py/python-kasa.svg)](https://badge.fury.io/py/python-kasa)\n[![Build Status](https://github.com/python-kasa/python-kasa/actions/workflows/ci.yml/badge.svg)](https://github.com/python-kasa/python-kasa/actions/workflows/ci.yml)\n[![codecov](https://codecov.io/gh/python-kasa/python-kasa/branch/master/graph/badge.svg?token=5K7rtN5OmS)](https://codecov.io/gh/python-kasa/python-kasa)\n[![Documentation Status](https://readthedocs.org/projects/python-kasa/badge/?version=latest)](https://python-kasa.readthedocs.io/en/latest/?badge=latest)\n\npython-kasa is a Python library to control TPLink smart home devices (plugs, wall switches, power strips, and bulbs) using asyncio.\nThis project is a maintainer-made fork of [pyHS100](https://github.com/GadgetReactor/pyHS100) project.\n\n## Getting started\n\nYou can install the most recent release using pip:\n```\npip install python-kasa\n```\n\nAlternatively, you can clone this repository and use poetry to install the development version:\n```\ngit clone https://github.com/python-kasa/python-kasa.git\ncd python-kasa/\npoetry install\n```\n\n## Discovering devices\n\nAfter installation, the devices can be discovered either by using `kasa discover` or by calling `kasa` without any parameters.\n\n```\n$ kasa\nNo --bulb nor --plug given, discovering..\nDiscovering devices for 3 seconds\n== My Smart Plug - HS110(EU) ==\nDevice state: ON\nIP address: 192.168.x.x\nLED state: False\nOn since: 2017-03-26 18:29:17.242219\n== Generic information ==\nTime:         1970-06-22 02:39:41\nHardware:     1.0\nSoftware:     1.0.8 Build 151101 Rel.24452\nMAC (rssi):   50:C7:BF:XX:XX:XX (-77)\nLocation:     {'latitude': XXXX, 'longitude': XXXX}\n== Emeter ==\nCurrent state: {'total': 133.082, 'power': 100.418681, 'current': 0.510967, 'voltage': 225.600477}\n```\n\nUse `kasa --help` to get list of all available commands, or alternatively, [consult the documentation](https://python-kasa.readthedocs.io/en/latest/cli.html).\n\n## Basic controls\n\nAll devices support a variety of common commands, including:\n * `state` which returns state information\n * `on` and `off` for turning the device on or off\n * `emeter` (where applicable) to return energy consumption information\n * `sysinfo` to return raw system information\n\n## Energy meter\n\nPassing no options to `emeter` command will return the current consumption.\nPossible options include `--year` and `--month` for retrieving historical state,\nand reseting the counters is done with `--erase`.\n\n```\n$ kasa emeter\n== Emeter ==\nCurrent state: {'total': 133.105, 'power': 108.223577, 'current': 0.54463, 'voltage': 225.296283}\n```\n\n## Bulb-specific commands\n\nAt the moment setting brightness, color temperature and color (in HSV) are supported depending on the device.\nThe commands are straightforward, so feel free to check `--help` for instructions how to use them.\n\n# Library usage\n\nYou can find several code examples in [the API documentation](https://python-kasa.readthedocs.io).\n\n## Contributing\n\nContributions are very welcome! To simplify the process, we are leveraging automated checks and tests for contributions.\n\n### Setting up development environment\n\nTo get started, simply clone this repository and initialize the development environment.\nWe are using [poetry](https://python-poetry.org) for dependency management, so after cloning the repository simply execute\n`poetry install` which will install all necessary packages and create a virtual environment for you.\n\n### Code-style checks\n\nWe use several tools to automatically check all contributions. The simplest way to verify that everything is formatted properly\nbefore creating a pull request, consider activating the pre-commit hooks by executing `pre-commit install`.\nThis will make sure that the checks are passing when you do a commit.\n\nYou can also execute the checks by running either `tox -e lint` to only do the linting checks, or `tox` to also execute the tests.\n\n### Running tests\n\nYou can run tests on the library by executing `pytest` in the source directory.\nThis will run the tests against contributed example responses, but you can also execute the tests against a real device:\n```\npytest --ip <address>\n```\nNote that this will perform state changes on the device.\n\n### Analyzing network captures\n\nThe simplest way to add support for a new device or to improve existing ones is to capture traffic between the mobile app and the device.\nAfter capturing the traffic, you can either use the [softScheck's  wireshark dissector](https://github.com/softScheck/tplink-smartplug#wireshark-dissector)\nor the `parse_pcap.py` script contained inside the `devtools` directory.\n\n\n## Supported devices\n\n### Plugs\n\n* HS100\n* HS103\n* HS105\n* HS107\n* HS110\n* KP105\n* KP115\n* KP401\n\n### Power Strips\n\n* EP40\n* HS300\n* KP303\n* KP400\n\n### Wall switches\n\n* HS200\n* HS210\n* HS220\n\n### Bulbs\n\n* EP40\n* LB100\n* LB110\n* LB120\n* LB130\n* LB230\n* KL50\n* KL60\n* KL110\n* KL120\n* KL125\n* KL130\n* KL135\n\n### Light strips\n\n* KL400\n* KL430\n\n**Contributions (be it adding missing features, fixing bugs or improving documentation) are more than welcome, feel free to submit pull requests!**\n\n## Resources\n\n### Links\n\n* [softScheck's github contains lot of information and wireshark dissector](https://github.com/softScheck/tplink-smartplug#wireshark-dissector)\n* [TP-Link Smart Home Device Simulator](https://github.com/plasticrake/tplink-smarthome-simulator)\n* [Unofficial API documentation](https://github.com/plasticrake/tplink-smarthome-api/blob/master/API.md)\n* [MQTT access to TP-Link devices, using python-kasa](https://github.com/flavio-fernandes/mqtt2kasa)\n\n### TP-Link Tapo support\n\n* [Tapo P100 (Tapo P105/P100 plugs, Tapo L510E bulbs)](https://github.com/fishbigger/TapoP100)\n  * [Home Assistant integration](https://github.com/fishbigger/HomeAssistant-Tapo-P100-Control)\n",
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/python-kasa/python-kasa',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
