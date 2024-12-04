class rc4():
    def toBytes(self,data):
        if type(data)==str:
            return data.encode()
        elif type(data)==bytes:
            return data
        else:
            raise Exception("data Type Error")

    def GetKey(self,data):
        k=[132, 206, 173, 4, 211, 121, 250, 202, 41, 13, 59, 166, 91, 116, 34, 200, 248, 49, 102, 215, 63, 160, 21, 103, 135, 68, 208, 175, 36, 30, 146, 181, 38, 64, 194, 57, 165, 195, 79, 99, 141, 0, 145, 96, 189, 128, 5, 170, 90, 55, 148, 229, 73, 219, 104, 243, 15, 77, 123, 152, 111, 239, 2, 35, 93, 190, 9, 26, 105, 199, 167, 228, 84, 124, 143, 252, 232, 66, 130, 122, 8, 71, 28, 53, 172, 251, 203, 89, 209, 23, 147, 101, 127, 86, 137, 236, 184, 1, 185, 134, 24, 16, 50, 32, 100, 76, 230, 88, 19, 225, 168, 87, 43, 94, 207, 46, 22, 214, 136, 54, 164, 106, 133, 10, 198, 60, 98, 142, 110, 192, 220, 201, 222, 140, 82, 95, 51, 154, 62, 118, 221, 11, 125, 233, 108, 52, 17, 234, 254, 14, 18, 255, 120, 29, 155, 126, 153, 40, 176, 12, 177, 245, 171, 83, 156, 187, 191, 112, 80, 235, 244, 237, 109, 78, 249, 231, 149, 72, 216, 107, 241, 69, 174, 253, 27, 144, 182, 180, 150, 61, 162, 56, 163, 186, 37, 131, 65, 223, 39, 115, 138, 33, 218, 42, 157, 3, 97, 246, 210, 178, 158, 92, 240, 117, 47, 217, 205, 196, 70, 159, 129, 58, 81, 227, 6, 213, 74, 113, 151, 7, 67, 20, 45, 75, 139, 204, 44, 161, 226, 179, 119, 188, 247, 25, 31, 48, 242, 183, 197, 238, 193, 85, 114, 169, 224, 212]
        return k

    def Cipher(self,data):
        data=self.toBytes(data)
        enc=[]
        k=self.Key.copy()
        n=0
        n1=0
        tmp=0
        key=[]
        print(k)
        for _ in range(50):
            n=(n+1)&0xff
            n1=(n1+k[n])&0xff
            tmp=k[n]
            k[n]=k[n1]
            k[n1]=tmp
            key.append(k[(k[n]+k[n1])%256])
        print(key)
        for c,k in zip(data,key):
            enc.append(c^k^51)
        return bytes(enc)


    def __init__(self,key):
        key=self.toBytes(key)
        self.Key=self.GetKey(key)
        self.__Key=key

    def SetKey(self,key):
        key=self.toBytes(key)
        self.Key=self.GetKey(key)
        self.__Key=key

import base64
b=base64.b64decode("w53Cj3HDgzTCsSM5wrg6FMKcw58Qw7RZSFLCljRxwrxbwrVdw4AEwqMjw7/DkMKTw4/Cv8Onw4NGw7jDmSdcwq4GGg==").decode("utf-8")
b_=[]
for i in b:
    b_.append(ord(i))
key=b"7e021a7dd49e4bd0837e22129682551b"
key_=[]
for i in key:
    key_.append(i^102)
r=rc4(bytes(key_))
print(r.Cipher(bytes(b_)))