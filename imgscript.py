from PIL import Image

names=["up","upLeft","left","downLeft","down","downRight","right","upRight"]
for i in range(8):
    img = Image.open(""+names[i]+".png")
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save("t_"+names[i]+".png", "PNG")
