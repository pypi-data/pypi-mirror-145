# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_arcaeabot',
 'nonebot_plugin_arcaeabot.adapters',
 'nonebot_plugin_arcaeabot.adapters.aua',
 'nonebot_plugin_arcaeabot.adapters.estertion',
 'nonebot_plugin_arcaeabot.handlers']

package_data = \
{'': ['*'],
 'nonebot_plugin_arcaeabot': ['assets/*',
                              'assets/char/*',
                              'assets/diff/*',
                              'assets/font/*',
                              'assets/grade/*',
                              'assets/output/*',
                              'assets/ptt/*',
                              'assets/recent/*',
                              'assets/song/*']}

install_requires = \
['Brotli>=1.0.9,<2.0.0',
 'Pillow>=8.3.1',
 'aiohttp>=3.7.4,<4.0.0',
 'httpx>=0.20.0,<1.0.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<=2.0.0-beta.2',
 'nonebot2>=2.0.0-beta.1,<=2.0.0-beta.2',
 'peewee>=3.14.4',
 'websockets>=10.0,<11.0']

setup_kwargs = {
    'name': 'nonebot-plugin-arcaeabot',
    'version': '1.0.7',
    'description': 'An arcaea plugin for nonebot2. ( A cross platform Python async bot framework. )',
    'long_description': None,
    'author': 'SEAFHMC',
    'author_email': 'd1366160279@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
