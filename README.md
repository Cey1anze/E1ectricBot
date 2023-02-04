<h1 align="center">
  E1ectricBot
  <br>
</h1>

<h4 align="center">Music, Qurey, AutoLog and Moderation.</h4>

<p align="center">
  <a href="https://www.python.org/downloads/">
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/discord.py">
  </a>
  <a href="https://github.com/Rapptz/discord.py/">
     <img src="https://img.shields.io/badge/discord-py-blue.svg" alt="discord.py">
  </a>
</p>

<p align="center">
  <a href="#overview">Overview</a>
  •
  <a href="#installation">Installation</a>
  •
  <a href="#join-my-community">Community</a>
  •
  <a href="#license">License</a>
</p>

<div>
<p align="center">
  <a href="https://github.com/HYBBWuXiDiXi/E1ectricBot/blob/master/README.md">English</a>
  •
  <a href="https://github.com/HYBBWuXiDiXi/E1ectricBot/blob/master/README-ZH.md">中文</a>
</p>
</div>

# Overview

E1ectric is a simple bot that can do many query functions,such as game status search,weather search,picture
search,translator and more.This mostly based on app_commands,that means you can easliy use commands without any
guide.You can turn E1ectric into an admin bot, music bot, search bot,new best friend or all of these together!

[Installation](#installation) is easy, and you do **NOT** need to know anything about coding!

**E1ectric Bot includes:**

- Moderation features (kick / ban / unban / mute / timeout / chat cleanup)
- Music features (Spotify, playlists, queues)
- Query features(game status search,weather search,picture search)
- AutoLog features(auto log guild events in both discord channels and local log files)

# Installation

**The following platforms are officially supported:**

- [Windows](#Windows)
- [Linux](#Linux)

**Accounts You Need To Create:**

- Discord bot on [Discord Developer Portal](https://discord.com/developers)

**Optional:**

(without these two optional accounts,bot can will not be able to run the corresponding functions and will throw
exceptions)

- Spotify for developers
  on [Spotify Dashboard]([My Dashboard | Spotify for Developers](https://developer.spotify.com/dashboard/))

- Alibabacloud on [Aliyun Machine Translate](https://www.alibabacloud.com/product/machine-translation)

**Before Installation,you need to install:**

- Python 3.10 or above
- python-pip
- Git

## Windows

##### step 1:

```
git clone https://github.com/HYBBWuXiDiXi/E1ectricBot.git
```

**Install Dependences:**

```
pip install -r requirements.txt
```

**Additional - For Translator:**

DO it if you want to use translator function,Otherwise,just delete translate.py in cmds/OtherApicmds(if you keep this
.py flie,bot will throw an exception)

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

##### Step 2:

**Setup configs:**

main config:

Modify  `config.example` files in the root directory to `config.json`, open and modify the contents in text method.

other configs:

Modify all `.example` files in the configs directory to `. json`, open and modify the contents in text method.

**Explanation of config file content:**

check [here]([E1ectricBot/configs.md at master · HYBBWuXiDiXi/E1ectricBot · GitHub](https://github.com/HYBBWuXiDiXi/E1ectricBot/blob/master/readme/configs.md))

##### Step 3:

**Well Done,All you need to do next is run the bot**

```
python3 Basic_main.py
```

## Linux

**If you already installed python3.10 or above,pip and git,the next steps is the same as [windows](#windows)**

If after reading the guide you are still experiencing issues, feel free to join
[My Server](https://discord.gg/vWbkrGPyWY) and ask in the **#About Bot** channel for help.

# Join My community!

**E1ectric** is in continuous development, and it’s not fully complete,I welcome anyone who wants to make robots develop
healthily. Even if you don't know anything about programming, it is welcome to provide advice and code support in the
community.

Join me on [My Server]([e1ectronic的服务器](https://discord.gg/vWbkrGPyWY))!

# License

Released under the [MIT](https://mit-license.org/) license.



