import json
import re
import csv
import base64
import hashlib

f = open("data.json", "r", encoding="utf-8")
obj = json.loads(f.read())
f.close()

def processBase(name, v):
    if name == "Base64":
        return base64.b64decode(v).decode()
    elif name == "Base32":
        return base64.b32decode(v).decode()
    elif name == "Base85":
        return base64.b85decode(v).decode()

for ob in obj:
    if ob["cryptoType"] != None:
        for k, v in ob.items():
            if k != "cryptoType" and k != "userid":
                ob[k] = processBase(ob["cryptoType"], v)
  
    username = ob["username"]
    username = username[0] + '*' if len(username) == 2 else username[0] + '*' * (len(username) - 2) + username[-1]
    ob["username"] = username

    md = hashlib.md5()
    md.update(ob["password"].encode())
    ob["password"] = md.hexdigest()

    sha1 = hashlib.sha1()
    sha1.update(ob["name"].encode())
    ob["name"] = sha1.hexdigest()

    idcard = ob["idcard"]
    idcard = '*' * 6 +  idcard[6:6+4] + '*' * (len(idcard) - 10)
    ob["idcard"] = idcard

    phone = ob["phone"]
    phone = phone[:3] + "*" * 4 + phone[7:]
    ob["phone"] = phone

    ob.pop("cryptoType")

with open('output.csv', 'w', newline='', encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["userid", "username", "password", "name", "idcard", "phone"])
    writer.writeheader()
    for row in obj:
        writer.writerow(row)

print(obj)


