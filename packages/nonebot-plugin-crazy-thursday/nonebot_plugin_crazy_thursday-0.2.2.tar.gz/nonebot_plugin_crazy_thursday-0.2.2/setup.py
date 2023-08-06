# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_crazy_thursday']

package_data = \
{'': ['*'], 'nonebot_plugin_crazy_thursday': ['resource/*']}

install_requires = \
['nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0', 'nonebot2>=2.0.0-beta.2,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-crazy-thursday',
    'version': '0.2.2',
    'description': 'Send crazy thursday articles of KFC randomly!',
    'long_description': '<div align="center">\n\n# Crazy Thursday\n\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable-next-line MD036 -->\n_🍗 天天疯狂 🍗_\n<!-- prettier-ignore-end -->\n\n</div>\n\n<p align="center">\n  \n  <a href="https://github.com/MinatoAquaCrews/nonebot_plugin_crazy_thursday/blob/main/LICENSE">\n    <img src="https://img.shields.io/badge/license-MIT-informational">\n  </a>\n  \n  <a href="https://github.com/nonebot/nonebot2">\n    <img src="https://img.shields.io/badge/nonebot2-2.0.0beta.2-green">\n  </a>\n  \n  <a href="">\n    <img src="https://img.shields.io/badge/release-v0.2.2-orange">\n  </a>\n  \n</p>\n</p>\n\n## 版本\n\nv0.2.2\n\n⚠ 适配nonebot2-2.0.0beta.2；\n\n👉 适配alpha.16版本参见[alpha.16分支](https://github.com/MinatoAquaCrews/nonebot_plugin_crazy_thursday/tree/alpha.16)\n\n[更新日志](https://github.com/MinatoAquaCrews/nonebot_plugin_crazy_thursday/releases/tag/v0.2.2)\n\n## 安装\n\n1. 通过`pip`或`nb`安装；\n\n2. 读取文案的默认路径位于`./resource`下；可在`.env.*`下设置：\n\n```python\nCRAZY_PATH="your-path-to-post.json"\n```\n\n## 功能\n\n天天疯狂！随机输出KFC疯狂星期四文案。\n\n**重磅新增** 三十余条文案！~~更新假面骑士国配文案~~\n\n## 命令\n\n1. 天天疯狂，疯狂星期[一|二|三|四|五|六|日|天]，输入**疯狂星期八**等不合法时间将提示；\n\n2. 支持狂乱[月|火|水|木|金|土|日]曜日日文触发；\n\n## 本插件改自HoshinoBot疯狂星期四插件\n\n[HoshinoBot-fucking_crazy_thursday](https://github.com/Nicr0n/fucking_crazy_thursday)\n',
    'author': 'KafCoppelia',
    'author_email': 'k740677208@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
