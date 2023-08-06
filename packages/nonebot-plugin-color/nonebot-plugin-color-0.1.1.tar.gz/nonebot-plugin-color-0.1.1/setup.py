# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_color']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.2.0', 'nonebot-adapter-onebot>=2.0.0b1', 'nonebot2>=2.0.0a14']

setup_kwargs = {
    'name': 'nonebot-plugin-color',
    'version': '0.1.1',
    'description': 'A specified color image generator for Nonebot2',
    'long_description': '<h1 align="center">Nonebot Plugin Color</h1></br>\n\n\n<p align="center">🤖 用于生成指定色彩图片的 Nonebot2 插件</p></br>\n\n\n<p align="center">\n  <a href="https://github.com/monsterxcn/nonebot-plugin-color/actions">\n    <img src="https://img.shields.io/github/workflow/status/monsterxcn/nonebot-plugin-color/Build%20distributions?style=flat-square" alt="actions">\n  </a>\n  <a href="https://raw.githubusercontent.com/monsterxcn/nonebot-plugin-color/master/LICENSE">\n    <img src="https://img.shields.io/github/license/monsterxcn/nonebot-plugin-color?style=flat-square" alt="license">\n  </a>\n  <a href="https://pypi.python.org/pypi/nonebot-plugin-color">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-color?style=flat-square" alt="pypi">\n  </a>\n  <img src="https://img.shields.io/badge/python-3.7.3+-blue?style=flat-square" alt="python"><br />\n</p></br>\n\n\n**安装方法**\n\n\n```bash\n# 从 PyPI 安装\npython3 -m pip install nonebot-plugin-color\n```\n\n\n<details><summary><i>从 Git 安装</i></summary></br>\n\n\n```bash\n# 从 Git 安装\ngit clone https://github.com/monsterxcn/nonebot-plugin-color.git\ncd nonebot_plugin_color\ncp -r nonebot_plugin_color /path/to/nonebot/plugins/\n```\n\n\n</details>\n\n\n重启 Bot 即可体验此插件。\n\n\n**使用方法**\n\n\n插件支持类似以下格式的命令，基于正则匹配：\n\n\n - `#ABCD88`\n - `123 234 33`\n - `色图 #123456`\n - `color#123456`\n\n\n<details><summary><i>哎哟这个色啊！好色！</i></summary></br>\n\n\n![色图来咯](screenshot.png)\n\n\n</details>\n\n\n**特别鸣谢**\n\n\n[@nonebot/nonebot2](https://github.com/nonebot/nonebot2/) | [@Mrs4s/go-cqhttp](https://github.com/Mrs4s/go-cqhttp)\n',
    'author': 'monsterxcn',
    'author_email': 'monsterxcn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/monsterxcn/nonebot-plugin-color',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0',
}


setup(**setup_kwargs)
