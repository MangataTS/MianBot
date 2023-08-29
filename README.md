# MianBot
一个支持Hydrooj的QQ机器人助手（平时上班比较忙，抽空更新）

## 前言
欢迎大家在ISSUES中提出自己想要的功能（尽我所能去实现）

## 预计实现功能

- 战绩查询
  - [x] 用户提交数据AC、WA、TLE、MLE、RE、CE、SE的次数
  - [x] 用户注册时间、上次登陆时间、用户身份
  - [ ] 用户的称号
  - [ ] 用户排名
  - [x] 用户头像
  - [ ] 用户使用的文件存储空间
- 平台提交数量查询
  - [x] 单个用户x小时提交数量查询
  - [x] 全平台x小时提交数量查询
  - [ ] 每天凌晨报备平台的活跃量
- 随机题目（这个将会在指定的训练中随机抽取，默认从所有训练中抽取）
  - [x] 每天固定时间在服务群聊中发布每日一题
  - [x] 随机一题
- 比赛查询
  - [ ] codeforces
  - [ ] atcoder
  - [ ] nowcoder
  - [ ] 全平台播报
- 题目状态
  - [ ] 隐藏题目
  - [ ] 开放题目
  - [ ] 一键开放所有题目
- [ ] 讨论监控推送（用户发布讨论贴时在服务群中同步发出）
- [ ] 作业监控推送（创建时推送到群里）
- [ ] 比赛监控推送（↑）
- [ ] 提供Rank的Top 10排名
- [ ] 题目查询是否有题解
- [ ] 用户封禁、讨论反清
- [ ] 设置用户称号系统
- [ ] 权限分配
- [ ] 根据用户的登录IP监控比赛，防止多端登录进行作弊



## 使用说明
暂无，等多实现几个功能后再说，配置文件是 `MianConfig.json`，需要自己创建一个，并放在根目录（`bot.py`同目录），格式如下，目前正在思考
```json
{
    "Hydro": {
      "Url": "",
      "Host": "",
      "Port": 27017,
      "username": "hydro",
      "password": "",
      "authSource": "hydro",
      "timeOff": 8
    },
    "TrainProblem": [""],
    "ServiceGroupList": [""]
}
```
其中可能需要解释的是，

- `Url` ：填入主页的完整网址，eg:`http://acm.mangata.ltd/`
- `Host`：填入服务器的IP（如果端口不是80的话需要再加上端口）
- `Port`：填入数据库端口，一般默认27017
- `username`：填入数据库的用户名，一般就是`hydro`不用管
- `password`：填入数据库的密码，这个可以用root权限查看`/root/.hydro/config.json`文件
- `authSource`：不用管
- `timeOff`：这个是数据库偏移正常时间的量，可以百度一下，一般是8h，如果不偏移就设置为0即可
- `TrainProblem`：这个是加入每日一题or随机一题的训练题单的ID列表
- `ServiceGroupList`：这个表示BOT服务的群聊列表，主要是做一些消息推送

<hr>

命令：

- `/commit uid hour` 表示的是查询UID最近hour小时的提交数量，eg：`commit 3 24` 表示的就是查询uid为3的用户最近24h的提交数量
- `/user uid` 表示的是查询UID的提交战绩（AC、WA、TLE、MLE、RE、CE、SE的次数）
- `/coding` 随机给你挑选一题（当然是本OJ的）


## 感谢(参考)

- [nonebot-plugin-cp-broadcast](https://github.com/HuParry/nonebot-plugin-cp-broadcast) 一个 Codeforces、牛客竞赛、AtCoder 平台的编程竞赛查询插件

## 更新日志

- 2023.8.28 新增了关于随机一题的内容，并且修复了之前的一些小bug，更新了REDEME文件
- 2023.8.24 实现xx最近xx小时的提交查询
- 2023.8.23 实现用户的战绩查询，提出某些预计实现功能