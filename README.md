# MianBot
一个支持Hydrooj的QQ机器人助手（平时上班比较忙，抽空更新）

## 前言
欢迎大家在ISSUES中提出自己想要的功能（尽我所能去实现）

## 预计实现功能

- [x] 用户的战绩查询（AC、WA、TLE、MLE、RE、CE、SE的次数）
- [x] 平台最近x小时提交数量（个人+全部）
- [ ] 每日一题
- [ ] 每日固定时间报备平台活跃量
- [ ] 用户发布讨论贴时在群中同步发出
- [ ] 作业推送(创建时推送到群里)
- [ ] 提供Rank的Top10排名
- [ ] 题目查询是否有题解
- [ ] 用户封禁、讨论反清
- [ ] 权限分配


## 使用说明
暂无，等多实现几个功能后再说，配置文件是 `MianConfig.json`，需要自己创建一个，并放在根目录（`bot.py`同目录），格式如下，目前正在思考
```json
{
    "Hydro": {
      "Host": "42.193.50.191",
      "Port": 27017,
      "username": "hydro",
      "password": "ufaRqx7vkR2KgjUDkHeOuihX7NZVwR9z",
      "authSource": "hydro",
      "timeOff": 8
    }
}
```
其中可能需要解释的是`timeOff`，这个是数据库偏移正常时间的量，可以百度一下，一般是8h，如果不偏移就设置为0即可

命令：

- `commit uid hour` 表示的是查询UID最近hour小时的提交数量，eg：`commit 3 24` 表示的就是查询uid为3的用户最近24h的提交数量
- `user uid` 表示的是查询UID的提交战绩（AC、WA、TLE、MLE、RE、CE、SE的次数）


## 更新日志

- 2023.8.24 实现xx最近xx小时的提交查询
- 2023.8.23 实现用户的战绩查询，提出某些预计实现功能