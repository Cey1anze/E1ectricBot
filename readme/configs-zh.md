<h1 align="center">
  About Configs
  <br>
</h1>

<div>
<p align="center">
  <a href="https://github.com/HYBBWuXiDiXi/E1ectricBot/blob/master/readme/configs.md">English</a>
  •
  <a href="https://github.com/HYBBWuXiDiXi/E1ectricBot/blob/master/readme/configs-zh.md">中文</a>
</p>
</div>

**在完成 [Installation](https://github.com/HYBBWuXiDiXi/E1ectricBot/blob/master/README.md) 后,你需要配置configs来让机器人正常运行**

**配置文件包括:**

- [configs.json](#configs.json)

- [channel.json](#channel.json)

- [chatGPTconfig.json](#chatGPTconfig.json)

- [logger.json](#logger.json)

- [music.json](#music.json)

- [translate.json](#translate.json)

### configs.json

| Field name | Type   | Descripiton       |
|:----------:|:------:|:-----------------:|
| token      | string | Discord bot token |

```
{
  "Token": "Your discord bot token here"    
}
```

**如何获得Discord Token:**

[Discord Developer Portal](https://discord.com/developers)

![discord](https://github.com/HYBBWuXiDiXi/E1ectricBot/blob/master/images/discord.png)

### channel.json

请设置一个欢迎频道，以便在新成员加入服务器时向频道中发送欢迎消息。

| Field name    | Type         | Descripiton |
|:-------------:|:------------:|:-----------:|
| welchannel-id | int / string | 频道ID        |

```
{
  "welchannel-id": "channel id"
}
```

**如何获得频道ID:**

![channel](https://github.com/HYBBWuXiDiXi/E1ectricBot/blob/master/images/channel.png)

### chatGPTconfig.json

请设定一个频道，让机器人在此频道回复您的消息，并同时提供OpenAI密钥以授予机器人API访问权限。

| Field name         | Type         | Descripiton |
|:------------------:|:------------:|:-----------:|
| discord_channel_id | int / string | 频道ID        |
| openAI_key         | string       | openai key  |

```
{
  "discord_channel_id": "channel id",
  "openAI_key": "openai key"
}
```

**如何获取OpenAI Key:**

![openai](https://github.com/HYBBWuXiDiXi/E1ectricBot/blob/master/images/openai.png "openai")

### logger.json

请设置一个频道，用于让机器人发送服务器日志。

| Field name     | Type | Descripiton |
|:--------------:|:----:|:-----------:|
| logger_channel | int  | 频道ID        |

```
{
  "logger_channel": your channel id
}
```

### music.json

为了使用音乐功能，您需要同时设置Spotify开发人员账户和Genius开发人员账户。

| Field name      | Type   | Descripiton    |
|:---------------:|:------:|:--------------:|
| client_id       | string | Spotify ID     |
| client_secret   | string | Spotify Secret |
| lrc_key         | string | Genius Key     |
| logging_channel | int    | 频道ID           |

```
{
  "client_id": "spotify client id",
  "client_secret": "spotify client secret",
  "lrc_key": "genius api token",
  "logging_channelid": channel id
}
```

**如何获得这些Key:**

- **Spotify**

  ![spotify](https://github.com/HYBBWuXiDiXi/E1ectricBot/blob/master/images/spotify.png)

  ![spotify_client](https://github.com/HYBBWuXiDiXi/E1ectricBot/blob/master/images/spotify_client.png)

- **Genius**

  ![genius](https://github.com/HYBBWuXiDiXi/E1ectricBot/blob/master/images/genius.png)

  ![genius-1](https://github.com/HYBBWuXiDiXi/E1ectricBot/blob/master/images/genius-1.png)

  ![genius_client](https://github.com/HYBBWuXiDiXi/E1ectricBot/blob/master/images/genius_client.png)

### translate.json

如需使用翻译功能，请设置阿里云账户。

| Field name | Type   | Descripiton         |
|:----------:|:------:|:-------------------:|
| id         | string | 阿里云AccessKey ID     |
| secret     | string | 阿里云AccessKey Secret |
| area       | string | 地区                  |

```
{
    "id": "AccessKey id",
    "secret": "AccessKey secret",
    "area": "area"
}
```

**如何获得阿里云AccessKey:**

请看 [阿里云官方文档](https://help.aliyun.com/document_detail/116401.htm?spm=a2c4g.11186623.0.0.b22b36692HkJOq#task-2245479)

### member.json

这里包含了所有关于成员管理的配置。（目前只作为reaction-role的配置）

| Field name | Type   | Descripiton                      |
|:----------:|:------:|:-------------------------------: |
| Message_id | int    | 用户需要添加反应贴纸的消息ID          |
| emoji      | list   | 表情（直接将表情追加复制到这个列表中）  |
| role_name  | list   | 身份组名字（确保顺序和表情是一一对应的） |

```
{
    "Message_id":1076464925465133147,
    "emoji": ["\uD83D\uDD35","\uD83D\uDFE3","\uD83D\uDFE2","\uD83D\uDFE1"],
    "role_name": ["卧槽~~原?","有为青年!!!","Norch","萨尼铁塔~~"]
}
```