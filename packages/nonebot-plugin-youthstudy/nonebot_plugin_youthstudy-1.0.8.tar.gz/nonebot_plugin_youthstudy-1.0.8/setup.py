# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_youthstudy']

package_data = \
{'': ['*'], 'nonebot_plugin_youthstudy': ['resource/bac/*', 'resource/font/*']}

install_requires = \
['Pillow>=9.0.1,<9.1.0',
 'beautifulsoup4>=4.10.0,<4.11.0',
 'httpx>=0.21.3,<0.22.0',
 'nonebot-adapter-onebot>=2.0.0b1,<3.0.0',
 'nonebot2>=2.0.0b2']

setup_kwargs = {
    'name': 'nonebot-plugin-youthstudy',
    'version': '1.0.8',
    'description': '基于nonebot2的青年大学习插件',
    'long_description': None,
    'author': 'ayanamiblhx',
    'author_email': '1196818079@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ayanamiblhx/nonebot_plugin_youthstudy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
