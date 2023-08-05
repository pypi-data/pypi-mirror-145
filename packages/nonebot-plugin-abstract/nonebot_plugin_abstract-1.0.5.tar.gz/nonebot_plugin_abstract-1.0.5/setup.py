# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_abstract']

package_data = \
{'': ['*']}

install_requires = \
['jieba==0.42.1',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot2>=2.0.0-beta.1,<3.0.0',
 'pinyin==0.4.0']

setup_kwargs = {
    'name': 'nonebot-plugin-abstract',
    'version': '1.0.5',
    'description': 'Plugin for nonebot2 that abstracts statements',
    'long_description': '# nonebot-plugin-abstract\n\n适用于 Nonebot2 的语句抽象化插件\n\n### 目前已实现功能\n- [x] 语句抽象话。\n\n### 未来要实现的功能\n- [ ] 分好抽象等级，例如基本抽象和深度抽象。~~怕抽象的语句过于抽象了。~~\n\n\n### 安装\n\n- 使用 nb-cli\n\n```\nnb plugin install nonebot_plugin_abstract\n```\n\n- 使用 pip\n\n```\npip install nonebot_plugin_abstract\n```\n\n\n### 使用\n```\n抽象 [要抽象的语句]\n```\n\n\n### 示例\n\n<div align="left">\n  <img src="https://s2.loli.net/2022/03/25/qdiuRKBILSJ1NxV.jpg" width="400" />\n</div>\n\n\n### 特别感谢\n\n- [THUzhangga/NMSL](https://github.com/THUzhangga/NMSL) Abstraction your words——never mind the scandal and liber\n',
    'author': 'CherryCherries',
    'author_email': 'cherrycherries@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CherryCherries/nonebot-plugin-abstract',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
