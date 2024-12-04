import json
import base64
import hashlib
import csv

# 假设你的JSON文件名为'data.json'
file_name = 'data.json'
def processBase(name, v):
    if name == "Base64":
        return base64.b64decode(v).decode()
    elif name == "Base32":
        return base64.b32decode(v).decode()
    elif name == "Base85":
        return base64.b85decode(v).decode()

    # 打开并读取JSON文件
with open(file_name, 'r', encoding='utf-8') as file:
    # 将文件内容解析为JSON列表
    data_list = json.load(file)
        
for ob in data_list:
    if ob["cryptoType"] != None:
        for k, v in ob.items():
            if k != "cryptoType" and k != "userid":
                ob[k] = processBase(ob["cryptoType"], v)
        username = ob["username"]
    
    ##脱敏处理
    ##若只有两个字符则只对最后一位使用本号代替，否则只保留第一位和最后一位字符， 其余都用*代替
    username = username[0] + '*' if len(username) == 2 else username[0] + '*' * (len(username) - 2) + username[-1]
    ob["username"] = username

    ##对密码进行MD5加密
    md = hashlib.md5()
    md.update(ob["password"].encode())
    ob["password"] = md.hexdigest()

    ##对姓名进行SHA1加密
    sha1 = hashlib.sha1()
    sha1.update(ob["name"].encode())
    ob["name"] = sha1.hexdigest()

    ##对身份证号进行脱敏处理,只保留年份,其余*代替
    idcard = ob["idcard"]
    idcard = '*' * 6 +  idcard[6:6+4] + '*' * (len(idcard) - 10)
    ob["idcard"] = idcard

    ##对手机号进行脱敏处理,只保留前三位和后四位,其余*代替
    phone = ob["phone"]
    phone = phone[:3] + "*" * 4 + phone[7:]
    ob["phone"] = phone

    ##去除cryptoType字段
    ob.pop("cryptoType")

with open('output.csv', 'w', newline='', encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["userid", "username", "password", "name", "idcard", "phone"])
    writer.writeheader()
    for row in data_list:
        writer.writerow(row)        
print(data_list)