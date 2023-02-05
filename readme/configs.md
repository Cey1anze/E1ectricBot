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

**After [Installation](https://github.com/HYBBWuXiDiXi/E1ectricBot/blob/master/README.md),You need to setup these
configs to let bot run properly**

**includes:**

- [configs.json](#configs.json)

- [channel.json](#channel.json)

- [chatGPTconfig.json](#chatGPTconfig.json)

- [logger.json](#logger.json)

- [music.json](#music.json)

- [translate.json](#translate.json)

##### configs.json

| Field name | Type   | Descripiton       |
|:----------:|:------:|:-----------------:|
| token      | string | discord bot token |

```
{
  "Token": "Your discord bot token here"    
}
```

**How to get token:**

[Discord Developer Portal](https://discord.com/developers)

![discord](https://github.com/HYBBWuXiDiXi/E1ectricBot/blob/master/images/discord.png)

##### channel.json

Please set a welcome channel for the bot to send a welcome message to new members upon joining the server.

| Field name    | Type         | Descripiton                     |
|:-------------:|:------------:|:-------------------------------:|
| welchannel-id | int / string | channel id,can be int or string |

```
{
  "welchannel-id": "channel id"
}
```

**How to get channel id:**

![channel](https://github.com/HYBBWuXiDiXi/E1ectricBot/blob/master/images/channel.png)

##### chatGPTconfig.json

Please set a channel for the bot to respond to your messages, and provide an OpenAI key to grant the bot API access.

| Field name         | Type         | Descripiton                     |
|:------------------:|:------------:|:-------------------------------:|
| discord_channel_id | int / string | channel id,can be int or string |
| openAI_key         | string       | openai key                      |

```
{
  "discord_channel_id": "channel id",
  "openAI_key": "openai key"
}
```

**How to get openai key:**

![openai](https://github.com/HYBBWuXiDiXi/E1ectricBot/blob/master/images/openai.png "openai")

##### logger.json

Please set a log channel for the bot to send server logs.

| Field name     | Type | Descripiton |
|:--------------:|:----:|:-----------:|
| logger_channel | int  | channel id  |

```
{
  "logger_channel": your channel id
}
```

##### music.json

To use the music function, you need to set up both a Spotify Developer account and a Genius Developer account.

| Field name      | Type   | Descripiton           |
|:---------------:|:------:|:---------------------:|
| client_id       | string | spotify client_id     |
| client_secret   | string | soptify client_secret |
| lrc_key         | string | genius api token      |
| logging_channel | int    | channel id            |

```
{
  "client_id": "spotify client id",
  "client_secret": "spotify client secret",
  "lrc_key": "genius api token",
  "logging_channelid": channel id
}
```

**How to get Spotify client and genius api key:**

- **Spotify**

  ![spotify](https://github.com/HYBBWuXiDiXi/E1ectricBot/blob/master/images/spotify.png)

  ![spotify_client](https://github.com/HYBBWuXiDiXi/E1ectricBot/blob/master/images/spotify_client.png)

- **Genius**

  ![genius](https://github.com/HYBBWuXiDiXi/E1ectricBot/blob/master/images/genius.png)

  ![genius-1](https://github.com/HYBBWuXiDiXi/E1ectricBot/blob/master/images/genius-1.png)

  ![genius_client](https://github.com/HYBBWuXiDiXi/E1ectricBot/blob/master/images/genius_client.png)

##### translate.json

To use the translate function, you need to obtain an Alibaba Access Key.

| Field name | Type   | Descripiton    |
|:----------:|:------:|:--------------:|
| id         | string | Alibaba id     |
| secret     | string | Alibaba secret |
| area       | string | area           |

```
{
    "id": "AccessKey id",
    "secret": "AccessKey secret",
    "area": "area"
}
```

**How to get Alibaba AccessKey:**

just
check [Offical Documentation](https://www.alibabacloud.com/help/en/basics-for-beginners/latest/obtain-an-accesskey-pair)
