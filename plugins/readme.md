**无特殊说明的说明无需配置，如有需求请改源码**

<!--ts-->
* [joinGroupAudit(进群验证码)](#joingroupaudit进群验证码)
* [autoRepeat(自动消息加一)](#autorepeat自动消息加一)
* [stopRevoke(群防撤回)](#stoprevoke群防撤回)
* [whatis(查询缩写意思)](#whatis查询缩写意思)
* [ApologizeToGirlfriend(给女朋友道歉信)](#apologizetogirlfriend给女朋友道歉信)
* [cleanGroupZombie(清理僵尸)](#cleangroupzombie清理僵尸)
* [5000choyen(5000 兆元字体风格图片)](#5000choyen5000-兆元字体风格图片)
* [niubi(吹牛皮)](#niubi吹牛皮)
* [what do you want to eat(吃啥?)](#what-do-you-want-to-eat吃啥)
* [sysinfo(服务器状态信息)](#sysinfo服务器状态信息)
* [phlogo(PornHub 风格的 logo)](#phlogopornhub-风格的-logo)
* [autoRevoke(自动撤回)](#autorevoke自动撤回)
* [toPinYin(汉字转拼音)](#topinyin汉字转拼音)
* [generate Qrcode(生成二维码)](#generate-qrcode生成二维码)
* [amusing language(生成和解码瞎叫字符)](#amusing-language生成和解码瞎叫字符)
* [bili subscriber(订阅 B 站 UP 主视频投稿 或 订阅番剧)](#bili-subscriber订阅-b-站-up-主视频投稿-或-订阅番剧)
* [weirdfonts(花体字符)](#weirdfonts花体字符)
* [jikipedia(小鸡词典查梗)](#jikipedia小鸡词典查梗)
* [versailles(凡尔赛语录)](#versailles凡尔赛语录)
* [weather(天气)](#weather天气)
* [bot_dl_douyin(抖音音视频下载)](#bot_dl_douyin抖音音视频下载)
* [baidu_ocr(百度 OCR)](#baidu_ocr百度-ocr)
* [meiriyiwen(每日一文)](#meiriyiwen每日一文)
* [replay(复读机 Plus)](#replay复读机-plus)
* [corona_virus(疫情订阅)](#corona_virus疫情订阅)
* [moechat(二次元词库聊天)](#moechat二次元词库聊天)
* [steam(steam 促销)](#steamsteam-促销)
* [rua(做一个摸头像的 gif)](#rua做一个摸头像的-gif)
* [custom image(自定义图片.jpg)](#custom-image自定义图片jpg)
* [russian_turntable(俄罗斯轮盘启蒙版)](#russian_turntable俄罗斯轮盘启蒙版)
* [TaoShow(买家秀)](#taoshow买家秀)

<!-- Added by: wongxy, at: Thu Jul 29 12:01:35 CST 2021 -->

<!--te-->

# joinGroupAudit(进群验证码)

进群验证码

# autoRepeat(自动消息加一)

自动消息加一功能，支持文字消息和图片消息

# stopRevoke(群防撤回)

群防撤回，无额外依赖

# whatis(查询缩写意思)

查询缩写意思

格式: 查询+{缩写} 或 查询

# ApologizeToGirlfriend(给女朋友道歉信)

生成给女朋友道歉信.

格式：给女朋友道歉{名}|{事情} 或 直接发送 给女朋友道歉 (接受私聊)

# cleanGroupZombie(清理僵尸)

清理长时间不发言的僵尸

管理员发送 清理僵尸 或 清理僵尸+{人数} 清理操作需要机器人是管理员

# 5000choyen(5000 兆元字体风格图片)

5000 兆元字体风格图片生成

格式：5000 {上部文字} {下部文字} {下部文字向右的额外偏移量(可选)}

`botoy.json`配置及默认值:

- `5000choyen_api`: [图片生成服务端](https://github.com/fz6m/5000choyen-server)接口地址

```json
{
  "5000choyen_api": "http://127.0.0.1:4000/api/v1/gen"
}
```

# niubi(吹牛皮)

吹某个人的牛皮

使用: 艾特一个人并发送文字 nb

# what do you want to eat(吃啥?)

吃啥？我帮你选!

格式：今天吃啥？早上吃啥？晚餐吃什么?...

使用前需先运行插件文件下载菜品数据，需要安装库`pip install aiofiles`,
如果是中途报错退出的，建议多运行几次，下载足够的菜品

# sysinfo(服务器状态信息)

查看服务器当前运行信息

命令：sysinfo

# phlogo(PornHub 风格的 logo)

快速生成 PornHub 风格的 logo

格式:

横向：ph Hello world
竖直：ph Hello world 1

# autoRevoke(自动撤回)

自动撤回插件

`botoy.json`配置项：

```json
{
  "autorevoke_keyword": "revoke"
}
```

该插件没有命令，只要机器人发送的消息中包含关键字 KEYWORD(`autorevoke_keyword`)，则撤回，
可以指定发出去多久后撤回: KEYWORD[多少秒], 如 KEYWORD[20]
表示该条消息 20s 后自动撤回

# toPinYin(汉字转拼音)

汉字转拼音

格式： 拼音{汉字}

# generate Qrcode(生成二维码)

生成二维码

格式：生成二维码{内容}

# amusing language(生成和解码瞎叫字符)

生成和解码瞎叫语言

生成: 瞎叫+{文字内容}

解码: 瞎叫啥+{瞎叫字符串}

`botoy.json`配置及默认值:

瞎叫词库

```json
{
  "amusing_language_matrices": ["唱", "跳", "rap", "篮球", "鸡你太美"]
}
```

# bili subscriber(订阅 B 站 UP 主视频投稿 或 订阅番剧)

B 站视频或番剧订阅

订阅 UP 主：哔哩视频订阅+{UID:123} 或 哔哩视频订阅+{UP 名字}
退订 UP 主：哔哩视频退订+{UID}
查看已订阅 UP 主：哔哩视频列表

订阅番剧：哔哩番剧订阅+{番剧名}
退订番剧：哔哩番剧退订+{番剧 id}
查看已订阅番剧: 哔哩番剧列表

# weirdfonts(花体字符)

生成花体字符

格式：花体+{可选字符串(字母或数字)}

里面使用了自动撤回，需要配合 autoRevoke 插件使用，不过没有也无妨

# jikipedia(小鸡词典查梗)

比如查 cpdd：

发送 cpdd 是啥梗、cpdd 是什么梗、查 cpdd 啥梗、cpdd 啥梗

# versailles(凡尔赛语录)

发送凡尔赛

# weather(天气)

天气+地名

# bot_dl_douyin(抖音音视频下载)

发送包含抖音视频链接的内容即可

# baidu_ocr(百度 OCR)

图片提取文字 格式：ocr 加图片

botoy.json

```json
{
  "baidu_ocr_app_id": "",
  "baidu_ocr_api_key": "",
  "baidu_ocr_secret_key": ""
}
```

配置项意思如键名

# meiriyiwen(每日一文)

每日一文：发送 好文 来读一篇好文章吧

# replay(复读机 Plus)

发送 复读机+内容(可文字，可图片)

# corona_virus(疫情订阅)

订阅疫情最新资讯，不是数值数据。。。。。。

群内发送: 疫情订阅、疫情退订

# moechat(二次元词库聊天)

词库类型及来源：[Kyomotoi/AnimeThesaurus](https://github.com/Kyomotoi/AnimeThesaurus)

1. 指定概率随机回复
2. 发送 moechat 开始连续对话, 即概率为 100%

以上概率是指对消息的检测，具体是否回复还要看词库是否包含该词条

botoy.json

```jsonc
{
  "moechat_chance": 0.2, // 概率
  "moechat_groups": [] // 开启的群组
}
```

# steam(steam 促销)

发送 steam

# rua(做一个摸头像的 gif)

作图功能插件的脑洞就没失望过，感谢大佬的创意[rua](https://github.com/pcrbot/plugins-for-Hoshino/tree/master/shebot/rua)

使用：

艾特一个人并发送 rua

# custom image(自定义图片.jpg)

[制图.jpg/.png](https://github.com/opq-osc/opqqq-plugin#%E8%87%AA%E5%AE%9A%E4%B9%89%E8%A1%A8%E6%83%85%E5%8C%85)

1. img list => 获取图片模板列表
2. img {name} => 设置自己要用的模板
3. 发送 {任意文字}.jpg 或.png 即可

botoy.json

```jsonc
{
  "custom_image_block_group": [] // 屏蔽群列表
  "custom_image_enable_emoji": true // 是否开启支持emoji
}
```

# russian_turntable(俄罗斯轮盘启蒙版)

发送：开始轮盘

# TaoShow(买家秀)

买家秀：发送 来点买家秀或买家秀即可
