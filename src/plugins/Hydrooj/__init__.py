import pymongo
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Bot, Event

myclient = pymongo.MongoClient("", 27017, username="hydro", password="",authSource='hydro')
mydb = myclient["hydro"]

def RecordQuery(uid:int):
    mycol = mydb["record"]
    usrcol = mydb["user"]
    CountNum={}
    for i in range(9):
        CountNum[i] = 0;
    for x in mycol.find({"uid":uid}):
        status =  int(x['status'])
        if CountNum.get(status) == None:
            CountNum[status] = 1
        else:
            CountNum[status] = CountNum.get(status) + 1
    name = str(usrcol.find_one({"_id":uid})['uname'])
    ans = {"AC":CountNum[1],"WA":CountNum[2],"TLE":CountNum[3],"MLE":CountNum[4],"RE":CountNum[6],"CE":CountNum[7],"SE":CountNum[8],"name":name}
    return ans

UserRecord = on_command("战绩查询", rule=to_me(), aliases={"战绩", "查战绩"}, priority=10, block=True)

@UserRecord.handle()
async def handle_function(args: Message = CommandArg()):
    uid = -1
    if args.extract_plain_text():
        uid = int(args.extract_plain_text())
    if uid != -1:
        ans = RecordQuery(uid)
        rs = str(ans["name"])+"\n战绩如下：\n"+"AC:\t" + str(ans["AC"])+"\nWA:\t"+str(ans["WA"])+"\nTLE:\t"+str(ans["TLE"])+"\nMLE:\t"+\
             str(ans["MLE"])+"\nRE:\t"+str(ans["RE"])+"\nCE:\t"+str(ans["CE"])+"\nSE:\t"+str(ans["SE"])
        await UserRecord.finish(str(rs))
    else:
        await UserRecord.send("请输入UiD")