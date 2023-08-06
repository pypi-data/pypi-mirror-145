# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_gocqhttp',
 'nonebot_plugin_gocqhttp.process',
 'nonebot_plugin_gocqhttp.process.device',
 'nonebot_plugin_gocqhttp.web']

package_data = \
{'': ['*'],
 'nonebot_plugin_gocqhttp.web': ['dist/*',
                                 'dist/css/*',
                                 'dist/fonts/*',
                                 'dist/icons/*',
                                 'dist/js/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'chevron>=0.14.0,<0.15.0',
 'httpx>=0.20.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot2>=2.0.0-beta.1,<3.0.0',
 'psutil>=5.9.0,<6.0.0',
 'py-cpuinfo>=8.0.0,<9.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-gocqhttp',
    'version': '0.5.1',
    'description': 'A plugin to run go-cqhttp directly in NoneBot2, without additional download and installation.',
    'long_description': '<!--cSpell:disable -->\n\n# nonebot-plugin-gocqhttp\n\n_A plugin to run go-cqhttp directly in NoneBot2, without additional download and installation._\n\n**一款在 NoneBot2 中直接运行 go-cqhttp 的插件, 无需额外下载安装.**\n\n![PyPI](https://img.shields.io/pypi/v/nonebot-plugin-gocqhttp?style=for-the-badge)\n\n[![GitHub issues](https://img.shields.io/github/issues/mnixry/nonebot-plugin-gocqhttp)](https://github.com/mnixry/nonebot-plugin-gocqhttp/issues)\n[![GitHub forks](https://img.shields.io/github/forks/mnixry/nonebot-plugin-gocqhttp)](https://github.com/mnixry/nonebot-plugin-gocqhttp/network)\n[![GitHub stars](https://img.shields.io/github/stars/mnixry/nonebot-plugin-gocqhttp)](https://github.com/mnixry/nonebot-plugin-gocqhttp/stargazers)\n[![GitHub license](https://img.shields.io/github/license/mnixry/nonebot-plugin-gocqhttp)](https://github.com/mnixry/nonebot-plugin-gocqhttp/blob/main/LICENSE)\n\n---\n\n## 优势\n\n~~对标[`koishijs/koishi-plugin-gocqhttp`](https://github.com/koishijs/koishi-plugin-gocqhttp/)~~\n\n**便于部署:** 部署时只需启动一个 Bot 进程即可, 无需其他附加工具\n\n**易于使用:** 本插件提供一个简单的 WebUI, 可以直接在图形界面中添加账户:\n\n<!-- markdownlint-disable MD033 -->\n<table>\n  <tr>\n    <td>\n      <img src="https://user-images.githubusercontent.com/97567575/159159758-3f8b9165-ba23-43fd-bfa7-cdc27cd9d6c3.png"/>\n      <b>添加帐号</b>\n    </td>\n    <td>\n      <img src="https://user-images.githubusercontent.com/97567575/159159878-6928cda1-4745-4291-97c8-e24ccca5c6ae.png"/>\n      <b>控制进程</b>\n    </td>\n  </tr>\n  <tr>\n    <td>\n      <img src="https://user-images.githubusercontent.com/32300164/161667766-2ffdc726-d54f-496c-9e15-d2cc8fce38b7.png" />\n      <b>查看状态</b>\n    </td>\n    <td>\n      <b>还有更多...</b><br />\n      <em>如果你觉得这个插件很赞, 欢迎返图!</em>\n    </td>\n  </tr>\n</table>\n<!-- markdownlint-enable MD033 -->\n\n**跨平台支持:** 根据反馈, 本插件已可以在`MacOS`/`Linux`/`Windows`上运行, 且不受[异步子进程调用带来的限制](https://github.com/nonebot/discussions/discussions/13#discussioncomment-1159147)\n\n## 使用\n\n### 安装\n\n推荐[使用`nb-cli`进行安装](https://v2.nonebot.dev/docs/start/install-plugin#%E5%AE%89%E8%A3%85)\n\n要求最低 Python 版本为 `3.8`\n\n### 配置\n\n本项目提供以下**可选**配置项, 请在`.env`中自行进行配置\n\n如果想要获取更多配置文件相关信息, 请[阅读源代码](./nonebot_plugin_gocqhttp/plugin_config.py)\n\n#### 账号配置\n\n`GOCQ_ACCOUNTS`: 要登录的 QQ 账号列表, 为一个 json 数组\n\n- 支持的字段:\n\n  - `uin`: QQ 账号 **(必填)**\n  - `password`: QQ 密码, 不填将使用扫码登录\n  - `protocol`: 数字, 是登录使用的[客户端协议](https://docs.go-cqhttp.org/guide/config.html#%E8%AE%BE%E5%A4%87%E4%BF%A1%E6%81%AF)\n\n- 示例:\n\n  ```json\n  [\n    {\n      "uin": "QQ帐号",\n      "password": "密码"\n    }\n  ]\n  ```\n\n#### 下载地址配置\n\n`GOCQ_URL`: 下载 URL, 默认为空, 设置该项目后以下几个与下载有关的配置项目将失效\n\n`GOCQ_DOWNLOAD_DOMAIN`: 下载域名, 默认为[`download.fastgit.org`](https://download.fastgit.org/)\n\n`GOCQ_REPO`: 要下载的仓库, 默认为[`Mrs4s/gocqhttp`](https://github.com/Mrs4s/go-cqhttp/)\n\n`GOCQ_VERSION`: 要下载的版本, 默认为空, 即下载最新版本\n\n`GOCQ_FORCE_DOWNLOAD`: 强制在启动时下载, 默认为 `false`\n\n#### 其他配置\n\n`GOCQ_PROCESS_KWARGS`: 创建进程时的可选参数, 请[参照代码](./nonebot_plugin_gocqhttp/process/process.py)进行修改\n\n`GOCQ_WEBUI_USERNAME`/`GOCQ_WEBUI_PASSWORD`: WebUI 的登录凭证, 不设置即不进行验证\n\n### 开始使用\n\n配置好了以后启动你的 Bot 即可\n\n- **需要注意以下几点**:\n\n  - 本插件会在 Bot 工作目录下创建`accounts`文件夹用于存储`go-cqhttp`的二进制和账户数据文件, 如果你使用版本管理工具(如`git`), 请自行将该文件夹加入[忽略列表](./.gitignore)\n\n  - 本插件通过子进程调用实现, 如果你在外部通过手段强行终止了 Bot 进程, 请检查开启的子进程是否也同样已终止\n\n  - 如果你的 Bot 监听来自所有主机的连接(比如监听了`0.0.0.0`), 或者它向公网开放, 强烈建议设置 WebUI 登录凭证以防止被未授权访问\n\n- 本插件提供了一个[仅`SUPERUSERS`能使用的命令](./nonebot_plugin_gocqhttp/plugin.py): `gocq`, 可以用来查看当前运行的`go-cqhttp`进程状态\n\n## 鸣谢\n\n- [`koishijs/koishi-plugin-gocqhttp`](https://github.com/koishijs/koishi-plugin-gocqhttp/): 本项目直接参考 ~~(直接开抄)~~\n- [`Mrs4s/gocqhttp`](https://github.com/Mrs4s/go-cqhttp/), [`nonebot/nonebot2`](https://github.com/nonebot/nonebot2): ~~(看看项目名, 什么成分不用多说了吧)~~ 本项目的套壳的核心\n\n## 开源许可证\n\n由于`go-cqhttp`使用了[AGPL-3.0](https://github.com/Mrs4s/go-cqhttp/blob/master/LICENSE)许可证, 本项目也同样使用该许可\n\n**注意! 如果在您的项目中依赖了该插件, 您的项目必须以该许可开源!**\n\n<!-- markdownlint-disable MD046 -->\n\n    A plugin to run go-cqhttp directly in NoneBot2, without additional download and installation.\n    Copyright (C) 2022 Mix\n\n    This program is free software: you can redistribute it and/or modify\n    it under the terms of the GNU Affero General Public License as published\n    by the Free Software Foundation, either version 3 of the License, or\n    (at your option) any later version.\n\n    This program is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n    GNU Affero General Public License for more details.\n\n    You should have received a copy of the GNU Affero General Public License\n    along with this program.  If not, see <https://www.gnu.org/licenses/>.\n',
    'author': 'Mix',
    'author_email': 'mnixry@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mnixry/nonebot-plugin-gocqhttp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
