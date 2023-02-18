<h1 align="center">  
  E1ectricBot  
  <br>  
</h1>

<h4 align="center">Music, Qurey, AutoLog and Management.</h4>

<p align="center">  
  <a href="https://www.python.org/downloads/">  
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/discord.py">  
  </a>  
  <a href="https://github.com/Rapptz/discord.py/">  
     <img src="https://img.shields.io/badge/discord-py-blue.svg" alt="discord.py">  
  </a>  
</p>

<p align="center">  
  <a href="#概况">Overview</a>  
  •  
  <a href="#安装">Installation</a>  
  •  
  <a href="#加入我的社区">Community</a>  
  •  
  <a href="#许可证">License</a>  
</p>

<div>  
<p align="center">  
  <a href="https://github.com/HYBBWuXiDiXi/E1ectricBot/blob/master/README.md">English</a>  
  •  
  <a href="https://github.com/HYBBWuXiDiXi/E1ectricBot/blob/master/README-ZH.md">中文</a>  
</p>  
</div>

# 概况

E1ectric是一个简易的Discord机器人，可以执行许多查询功能，例如游戏状态搜索，天气搜索，图片搜索，翻译等。机器人的主要功能基于app_commands，这意味着您可以在没有任何指南的情况下轻松使用命令。您可以将E1ectric变成频道管理机器人，音乐机器人，查询机器人等 !  !

[安装](#安装) 十分简单, 并且不需要您拥有任何编程能力 !  !

**机器人包括以下功能:**

- 频道管理功能 (踢出 / 封禁 / 解封 / 静音 / 禁言 / 清理消息)
- 音乐功能 (基于Spotify，支持歌单，使用时包括播放队列)
- 查询功能 (游戏状态查询，天气查询，以图搜图等)
- 自动记录日志 (当社区中触发了事件，包括但不限于删除信息时，自动在特定Discord频道和本地同时记录日志)

# 安装

**支持以下平台：**

- [Windows](#Windows)
- [Linux](#Linux)

**你需要创建的账户：**

- Discord bot on [Discord Developer Portal](https://discord.com/developers)

**可选项：**

如果不创建这些帐户并获得api调取密钥，机器人将无法运行相应的功能，并且可能会抛出异常，在不创建这两个账户的前提下，您只需删除cmds目录下的music文件夹以及OtherApicmds目录下的translate.py即可解决抛出异常的问题

- Spotify for developers on [Spotify Dashboard](https://developer.spotify.com/dashboard/)

- Genius on [Genius Developers](https://genius.com/developers)

- Openai on [OpenAI](https://platform.openai.com/signup)

- Alibabacloud on [Aliyun Machine Translate](https://www.alibabacloud.com/product/machine-translation)

**在安装项目之前，您需要提前安装：**

- Python 3.10 or above
- python-pip
- Git

## Windows

### step 1:

```
git clone https://github.com/HYBBWuXiDiXi/E1ectricBot.git  
```

**安装依赖：**

```
pip install -r requirements.txt  
```

**额外操作 - For Translator:**

如果要使用翻译功能，请执行以下操作，否则，只需删除cmdsOtherApicmds中的translate.py 如不删除，机器人可能会抛出异常 ！！

```
cd ./cmds/OtherApicmds  
```

```
md res  
```

```
cd res  
```

```
git clone https://github.com/aliyun/aliyun-openapi-python-sdk.git  
```

```
cd aliyun-openapi-python-sdk/aliyun-python-sdk-core  
```

```
python setup.py install  
```

```
cd ../aliyun-python-sdk-alimt  
```

```
python setup.py install  
```

### Step 2:

**设置配置文件:**

主配置文件:

将根目录下的  `config.example` 文件重命名为 `config.json`, 以文本方式打开并修改内容。

其余配置文件:

将config目录下的所有 `.example` 文件后缀改为 `. json`, 以文本方式打开并修改内容。

**对config文件内容的解释:**

点它 -> [here](https://github.com/HYBBWuXiDiXi/E1ectricBot/blob/master/readme/configs.md)

### Step 3:

**接下来只需要运行机器人**

```
python3 Basic_main.py  
```

##      

## Linux

**如果您已经安装了python3.10或更高版本，pip和git，则接下来的步骤与 [windows](#windows) 相同**

如果在阅读指南后您仍然遇到问题，请随时加入 [My Server](https://discord.gg/vWbkrGPyWY) 并在 **#About Bot** 频道中寻求帮助。

# 加入我的社区

**E1ectric**正在不断的进行开发，而且还没有完全完成，我欢迎任何想让机器人良性发展的人。即使您对编程一无所知也欢迎在社区中提供建议，如果您能提供代码支持将会对机器人的发展有很大的帮助。

加入我的服务器 [My Server](https://discord.gg/vWbkrGPyWY)!

# 许可证

基于 [MIT](https://mit-license.org/) 许可证.
