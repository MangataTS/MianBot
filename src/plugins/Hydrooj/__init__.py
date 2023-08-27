import json
import random
import pymongo
from bson import ObjectId
from nonebot import on_command
from nonebot.internal.params import ArgPlainText
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.params import CommandArg
from datetime import datetime, timedelta
import requests

with open('MianConfig.json') as file:
    data = json.load(file)
print(data)
MianConfig = data

myclient = pymongo.MongoClient(MianConfig['Hydro']['Host'], MianConfig['Hydro']['Port'],
                               username=MianConfig['Hydro']['username'],
                               password=MianConfig['Hydro']['password'],
                               authSource=MianConfig['Hydro']['authSource'])
mydb = myclient["hydro"]


def record_query(uid: int):
    mycol = mydb["record"]
    usrcol = mydb["user"]
    CountNum = {}
    for i in range(9):
        CountNum[i] = 0;
    for x in mycol.find({"uid": uid}):
        status = int(x['status'])
        if CountNum.get(status) == None:
            CountNum[status] = 1
        else:
            CountNum[status] = CountNum.get(status) + 1
    name = str(usrcol.find_one({"_id": uid})['uname'])
    ans = {"AC": CountNum[1], "WA": CountNum[2], "TLE": CountNum[3], "MLE": CountNum[4], "RE": CountNum[6],
           "CE": CountNum[7], "SE": CountNum[8], "name": name}
    return ans


# TODO 战绩查询还需要参考之前的设计
UserRecord = on_command("user", rule=to_me(), aliases={"战绩", "查战绩", "战绩查询"}, priority=10, block=True)
@UserRecord.handle()
async def handle_record_query(args: Message = CommandArg()):
    if uid := args.extract_plain_text():
        ans = record_query(int(uid))
        rs = str(ans["name"]) + "\n战绩如下：\n" + "AC:\t" + str(ans["AC"]) + "\nWA:\t" + str(ans["WA"]) + "\nTLE:\t" + str(
            ans["TLE"]) + "\nMLE:\t" + \
             str(ans["MLE"]) + "\nRE:\t" + str(ans["RE"]) + "\nCE:\t" + str(ans["CE"]) + "\nSE:\t" + str(ans["SE"])
        await UserRecord.finish(str(rs))


@UserRecord.got("uid", prompt="请输入查询用户的UID")
async def got_record_query(uid: str = ArgPlainText()):
    ans = record_query(int(uid))
    rs = str(ans["name"]) + "\n战绩如下：\n" + "AC:\t" + str(ans["AC"]) + "\nWA:\t" + str(ans["WA"]) + "\nTLE:\t" + str(
        ans["TLE"]) + "\nMLE:\t" + \
         str(ans["MLE"]) + "\nRE:\t" + str(ans["RE"]) + "\nCE:\t" + str(ans["CE"]) + "\nSE:\t" + str(ans["SE"])
    await UserRecord.finish(str(rs))


# 服务器时区偏差需要 ＋ 8hour，
# TODO 添加定时任务，每天凌晨发布最近24h、7days、1month、total的提交数量
# TODO 用户A平台最近X小时的提交数量，当A为0时表示所有提交数量
def record_commit_count(uid, findhour: int):
    collection = mydb['record']
    now = datetime.now()
    past_24_hours = now - timedelta(hours=findhour + int(MianConfig['Hydro']['timeOff']))
    query = {
        'judgeAt': {
            '$gte': past_24_hours,
            '$lt': now
        }
    }
    if uid != 0:
        query['uid'] = uid
    count = collection.count_documents(query)
    print('过去', findhour, '小时新增的数据量：', count)
    return count


# commit uid hour eg: commit 2 24
RecordCommit = on_command("commit", rule=to_me(), aliases={"评测记录"}, priority=10, block=True)


@RecordCommit.handle()
async def handle_record_commit_count(args: Message = CommandArg()):
    if AllRecord := args.extract_plain_text():
        split_string = AllRecord.split(" ")  # 使用空格分割字符串
        int_list = []
        for x in split_string:
            try:
                int_value = int(x)
                int_list.append(int_value)
            except ValueError:
                await RecordCommit.finish(f"这也不是数字啊，你是不是9年义务教育都没上完？")
        if len(int_list) == 0:
            await RecordCommit.finish(f"怎么发了个空")
        uid = int_list[0]
        findhour = int_list[0]
        # 如果只发了一个数字那么默认查询所有
        if len(int_list) == 1:
            uid = 0
        if findhour < 0:
            await RecordCommit.finish(f"好家伙，你家时间有负数吗？")
        if findhour > 9000:
            await RecordCommit.finish(f"时间太久远了，臣妾不想查了=_=")
        ans = record_commit_count(uid, findhour)
        if uid != 0:
            Rstr = f"最近{findhour}小时，uid为{uid}的提交数量为：{ans}次~"
        else:
            Rstr = f"最近{findhour}小时，Onlinejudge的提交数量为：{ans}次~"
        await RecordCommit.finish(Rstr)


@RecordCommit.got("AllRecord", prompt="请问你想查询谁最近几小时的提交数量呢？\neg: 3 24 \n表示查询uid为3，最近24h的提交数量")
async def got_record_commit_count(AllRecord: str = ArgPlainText()):
    split_string = AllRecord.split(" ")  # 使用空格分割字符串
    int_list = [int(x) for x in split_string]
    uid = int_list[0]
    findhour = int_list[1]
    if findhour < 0:
        await RecordCommit.finish(f"好家伙，你家时间有负数吗？")
    if findhour > 9000:
        await RecordCommit.finish(f"时间太久远了，臣妾不想查了=_=")
    ans = record_commit_count(uid, findhour)
    if uid != 0:
        Rstr = f"最近{findhour}小时，uid为{uid}的提交数量为：{ans}次~"
    else:
        Rstr = f"最近{findhour}小时，Onlinejudge的提交数量为：{ans}次~"
    await RecordCommit.finish(Rstr)


# 默认获取所有训练中的题目PID，并返回去重后的PID数组，
# 如果传入参数为True，则使用MianConfig.json中的训练
def query_traing_problem(Useconfig=False):
    collection = mydb['document']
    query_default = {
        'docType': 40
    }
    if Useconfig and len(MianConfig['TrainProblem']) != 0:
        ids_to_query = MianConfig['TrainProblem']
        object_ids = [ObjectId(id) for id in ids_to_query]
        query_default['_id'] = {"$in": object_ids}
    result = collection.find(query_default)
    Allpids = []
    cnt = 0
    for it in result:
        cnt = cnt + 1
        for node in it['dag']:
            for ppid in node['pids']:
                Allpids.append(ppid)
    unique_list = list(set(Allpids))
    return unique_list


# 获取题目信息 TODO 后面添加题解、讨论数量指标
def get_problem_info(id: str):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
    }
    url = MianConfig['Hydro']['Url'] + '/api/?'
    query = "query{problem(id:" + id + "){pid,title,nSubmit,nAccept,difficulty,tag}}"
    url = url + query
    val = requests.get(url, headers=headers)
    res = json.loads(val.content)
    it = res["data"]["problem"]
    if it is None:
        return str("题目已被隐藏请再次输入！")
    else:
        link = MianConfig['Hydro']['Url'] + "/p/" + it['pid']
        tag = ""
        l = len(it['tag'])
        j = 1
        for i in it['tag']:
            if j < l:
                tag = tag + i + "、"
            else:
                tag = tag + i
            j = j + 1
        ans = "[题目名称]： " + it['title']
        ans = ans + "\n[题目连接]： " + link
        ans = ans + "\n[算法标签]： " + tag
        ans = ans + "\n[总提交数]： " + str(it['nSubmit'])
        ans = ans + "\n[总通过数]： " + str(it['nAccept'])
        ans = ans + "\n[预估难度]： " + str(it['difficulty'])
        ans = ans + "\n骚年快来挑战吧！别忘了写题解噢！"
        return ans


RandProblem = on_command("coding", rule=to_me(), aliases={"tw"}, priority=10, block=True)

@RandProblem.handle()
async def handle_rand_problem(args: Message = CommandArg()):
    pids = query_traing_problem()
    randp = random.randint(0, len(pids) - 1)
    await RandProblem.finish(get_problem_info(str(randp)))