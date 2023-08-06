# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_everyday_en']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.7.0',
 'httpx>=0.19.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1',
 'nonebot2>=2.0.0-beta.1']

setup_kwargs = {
    'name': 'nonebot-plugin-everyday-en',
    'version': '1.1.5',
    'description': '每日一句英文句子。完整帮助文档，可选搭配软依赖nonebot_plugin_apscheduler实现定时发送',
    'long_description': '<p align="center">\n  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>\n</p>\n\n<div align="center">\n  \n# nonebot_plugin_everyday_en\n\n🍥适用于 [Nonebot2](https://github.com/nonebot/nonebot2) 的每日一句插件🍥\n  \n</div>\n\n<p align="center">\n  \n  <a href="https://raw.githubusercontent.com/MelodyYuuka/nonebot_plugin_everyday_en/master/LICENSE">\n    <img src="https://img.shields.io/github/license/MelodyYuuka/nonebot_plugin_everyday_en" alt="license">\n  </a>\n\n  <a href="https://pypi.python.org/pypi/nonebot_plugin_everyday_en">\n    <img src="https://img.shields.io/pypi/v/nonebot_plugin_everyday_en" alt="pypi">\n  </a>\n\n  <a href="https://onebot.dev">\n    <img src="https://img.shields.io/badge/OneBot-11-black" alt="license">\n  </a>\n  \n  <a href="https://github.com/nonebot/nonebot2">\n    <img src="https://img.shields.io/badge/nonebot2-2.0.0beta.1+-green">\n  </a>\n  \n  <a href="">\n    <img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="python">\n  </a>\n  \n</p>\n\n## 安装载入\n\n- 通过 pip 或 nb-cli 安装\n\n```shell\npip install nonebot-plugin-everyday-en\n```\n\n- 并在您的bot.py中载入插件\n\n```python\nnonebot.load_plugin("nonebot_plugin_everyday_en")\n```\n\n- 如需使用定时发送功能，还需安装软依赖 [nonebot-plugin-apscheduler](https://github.com/nonebot/plugin-apscheduler)\n```shell\npip install nonebot-plugin-apscheduler\n```\n\n## 指令\n- `每日一句`: 获取今天的句子\n  - `每日一句[日期]`: 获取指定日期的句子\n    > 日期格式为 YYYY-MM-DD , 例如 2020-01-08\n\n- `开启/关闭定时每日一句`: 开启/关闭本群定时发送 **[SUPERUSER]**\n  - `开启/关闭定时每日一句[群号]`: 开启/关闭指定群定时发送 **[SUPERUSER]**\n\n- `查看定时每日一句列表`: 列出开启定时发送的群聊 **[SUPERUSER]**\n\n## 配置项\n\n配置方式：直接在 NoneBot 全局配置文件中添加以下配置项即可。\n\nNoneBot 配置相关教程详见 [配置 | NoneBot](https://v2.nonebot.dev/docs/tutorial/configuration)\n\n🟢 默认配置为每日 8:00 发送\n### everyday_post_hour\n- 类型: int\n- 默认: 8\n- 说明: 每日定时发送的小时，不需要在数字前加0\n>```python\n>EVERYDAY_POST_HOUR=8\n>```\n\n### everyday_post_minute\n- 类型: int\n- 默认: 0\n- 说明: 每日定时发送的分钟，不需要在数字前加0\n>```python\n>EVERYDAY_POST_MINUTE=0\n>```\n\n### everyday_delay\n- 类型: float\n- 默认: 0.5\n- 说明: 定时发送时各群间发送的延迟秒数，以免腾讯风控导致发送失败\n>```python\n>EVERYDAY_DELAY=0.5\n>```\n\n## 软依赖\n- [`nonebot-plugin-apscheduler`](https://github.com/nonebot/plugin-apscheduler): 使用定时发送功能\n\n- [`nonebot-plugin-help`](https://github.com/XZhouQD/nonebot-plugin-help): 在群内查看帮助文档\n  - 也可自行解析 `__help_plugin_name__` , `__help_version__` , `__usage__`来接入您自己的帮助插件\n\n## 常见问题\n\n### `Q: 为什么没有语音？`\n- A: 如果你使用的是`go-cqhttp`，那么你需要安装`FFmpeg`并重启本插件来使用语音功能，详见[`安装 ffmpeg`](https://docs.go-cqhttp.org/guide/quick_start.html#%E5%AE%89%E8%A3%85-ffmpeg)\n\n### `Q: 为什么定时发送每日一句某些群无法收到？`\n- A: 检查日志，频繁发送消息可能导致腾讯风控，可通过设置[`everyday_delay`](https://github.com/MelodyYuuka/nonebot_plugin_everyday_en#everyday_delay)配置项设置发送延迟来缓解\n\n## 开源许可\n\n- 本插件使用 `MIT` 许可证开源\n',
    'author': 'MelodyYuuka',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MelodyYuuka/nonebot_plugin_everyday_en',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
