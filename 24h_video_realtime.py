import cv2
import glob
import datetime
import random

def scale_to_width(img, width):
    """幅が指定した値になるように、アスペクト比を固定して、リサイズする。
    """
    h, w = img.shape[:2]
    height = round(h * (width / w))
    dst = cv2.resize(img, dsize=(width, height))

    return dst

def scale_to_height(img, height):
    """高さが指定した値になるように、アスペクト比を固定して、リサイズする。
    """
    h, w = img.shape[:2]
    width = round(w * (height / h))
    dst = cv2.resize(img, dsize=(width, height))

    return dst

def add(img1, img2, top, left): #put img2 on img1 / img2の上にimg1を載せる
    height, width = img1.shape[:2]
    img2[top:height + top, left:width + left] = img1


while True:
    dt_now = datetime.datetime.now()
    hh = (str(dt_now.hour)).zfill(2)
    mm = (str(dt_now.minute)).zfill(2)
    ss = (str(dt_now.second)).zfill(2)

    time_now = hh + mm + ss + "_"

    files = glob.glob("all_photos/*" + time_now + "*")
    print(files)

    black_back = cv2.imread("black_back.jpg")

    if len(files) == 0:
        frame = cv2.imread("white_back.jpg")  #blank
        frame = cv2.putText(frame, hh + ":" + mm + ":" + ss, (700, 960), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 5,
                            cv2.LINE_AA)
    else:
        file = random.choice(files)  # 2枚以上あるときランダムに取り出す
        img = cv2.imread(file)
        img_hight, img_width, img_color = img.shape

        if img_width > img_hight:#landscape orientation/ 横長
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            img_hight, img_width, img_color = img.shape
        else: #portrait orientation/ 縦長
            pass

        if img_width/img_hight < 1080/1920: #Slender than 16:9 → Fit to length / 16:9より細長い→縦幅合わせ
            img = scale_to_height(img, 1920)
            img_hight, img_width, img_color = img.shape
            add(img, black_back, 0, int(1080 / 2 - img_width / 2))
        else: #Squarer than 16:9 → Fit to width / 16:9より寸胴→横幅合わせ
            img = scale_to_width(img, 1080)
            img_hight, img_width, img_color = img.shape
            add(img, black_back, int(1920 / 2 - img_hight / 2), 0)

        frame = black_back

    cv2.imshow('window', frame)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()

