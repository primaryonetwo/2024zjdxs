from PIL import image as Image
import pyzbar.pyzbar as pyzbar
import os

path = "./final_out"

orders = []
names = []

for root, dirs, files in os.walk(path):
    for file in files:
        img = Image.open(os.path.join(root, file))
        img = img.convert('RGB')
        width,height=img.size
        result = ""
        for i in range(0,height):
            for j in range(0,width):
                tmp = img.getpixel((j,i))
                result += bin(tmp[0])[-1]
        a = 0
        pic = Image.new("RGB",(50,50))
        for y in range(0,50):
            for x in range(0,50):
                if result[a] == '0':
                    pic.putpixel([x,y],(0,0,0))
                else:
                    pic.putpixel([x,y],(255,255,255))
                a += 1
        pic = pic.resize((500,500))
        barcodes = pyzbar.decode(pic)
        for barcode in barcodes:
            barcodeDATA = barcode.data.decode("utf-8")
            orders.append(barcodeDATA)
            names.append(os.path.join(root, file))

#图片大小
width_i = 50
height_i = 50
#每行每列显示图片数量
line_max = 10
row_max = 10
#参数初始化
all_path = []
num = 0
pic_max=line_max*row_max
toImage = Image.new('RGB',(width_i*line_max,height_i*row_max))

pos = 1
for j in range(0,row_max): 
    for i in range(0,line_max):
        pic_path = names[orders.index(str(pos))]
        pic_fole_head =  Image.open(pic_path)
        width,height =  pic_fole_head.size
        tmppic = pic_fole_head.resize((width_i,height_i))
        loc = (int(i%line_max*width_i),int(j%line_max*height_i))
        toImage.paste(tmppic,loc)
        pos += 1
toImage.save('merged.png')