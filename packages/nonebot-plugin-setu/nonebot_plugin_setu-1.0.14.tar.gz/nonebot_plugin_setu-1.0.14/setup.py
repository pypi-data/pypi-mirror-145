# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_setu', 'nonebot_plugin_setu.dao']

package_data = \
{'': ['*']}

install_requires = \
['httpx-socks>=0.7.3,<0.8.0',
 'httpx>=0.21.3,<0.22.0',
 'nonebot-adapter-onebot>=2.0.0b1,<3.0.0',
 'nonebot2>=2.0.0b2,<3.0.0',
 'tqdm>=4.61.0,<5.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-setu',
    'version': '1.0.14',
    'description': '基于lolicon api的涩图插件',
    'long_description': None,
    'author': 'ayanamiblhx',
    'author_email': '1196818079@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ayanamiblhx/nonebot_plugin_setu',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
