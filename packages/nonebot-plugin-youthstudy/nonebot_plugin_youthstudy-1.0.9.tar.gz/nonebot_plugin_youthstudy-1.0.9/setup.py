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
    'version': '1.0.9',
    'description': '基于nonebot2的青年大学习插件',
    'long_description': '<div align="center">\n    <img src="https://s4.ax1x.com/2022/03/05/bw2k9A.png" alt="bw2k9A.png" border="0"/>\n    <h1>nonebot_plugin_youthstudy</h1>\n    <b>基于nonebot2的青年大学习插件，用于获取最新一期青年大学习答案</b>\n    <br/>\n    <a href="https://github.com/ayanamiblhx/nonebot_plugin_youthstudy/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/ayanamiblhx/nonebot_plugin_youthstudy?style=flat-square"></a>\n    <a href="https://github.com/ayanamiblhx/nonebot_plugin_youthstudy/network"><img alt="GitHub forks" src="https://img.shields.io/github/forks/ayanamiblhx/nonebot_plugin_youthstudy?style=flat-square"></a>\n    <a href="https://github.com/ayanamiblhx/nonebot_plugin_youthstudy/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/ayanamiblhx/nonebot_plugin_youthstudy?style=flat-square"></a>\n    <a href="https://github.com/ayanamiblhx/nonebot_plugin_youthstudy/blob/main/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/ayanamiblhx/nonebot_plugin_youthstudy?style=flat-square"></a>\n</div>\n\n\n\n## 安装及更新\n\n- 使用`nb plugin install nonebot_plugin_youthstudy`或者`pip install nonebot_plugin_youthstudy`来进行安装\n- 使用`nb plugin update nonebot_plugin_youthstudy`或者`pip install nonebot_plugin_youthstudy -U`来进行更新\n\n\n\n### 导入插件(两种方式二选一)\n\n- 在`bot.py`中添加`nonebot.load_plugin("nonebot_plugin_youthstudy")`\n\n- 在`pyproject.toml`里的`[tool.nonebot]`中添加`plugins = ["nonebot_plugin_youthstudy"]`\n\n**注**：如果你使用`nb`安装插件，则不需要设置此项\n\n\n\n### 正式使用\n\n对机器人发送口令：“青年大学习”或者“大学习”即可获取最新一期的青年大学习答案\n\n\n\n### TODO\n\n- [ ] 通过检查更新自动提醒完成青年大学习\n\n\n\n## 更新日志\n\n### 2021/3/5\n\n- 支持nonebot[v2.0.0-beta2]，请更新至最新版nonebot使用\n\n',
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
