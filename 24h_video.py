import cv2
import glob
import datetime
import random
import os
import sys

#exe
def find_data_file(filename):
   if getattr(sys, "frozen", False):
       # The application is frozen
       datadir = os.path.dirname(sys.executable)
   else:
       # The application is not frozen
       # Change this bit to match where you store your data files:
       datadir = os.path.dirname(__file__)
   return os.path.join(datadir, filename)

def get_h_m_s(td):
    m, s = divmod(td.seconds, 60)
    h, m = divmod(m, 60)
    return h, m, s

def scale_to_width(img, width):
    """
    Resize the image to the specified width with a fixed aspect ratio
    幅が指定した値になるように、アスペクト比を固定して、リサイズする
    """
    h, w = img.shape[:2]
    height = round(h * (width / w))
    dst = cv2.resize(img, dsize=(width, height))

    return dst

def scale_to_height(img, height):
    """
    Resize the image to the specified height with a fixed aspect ratio
    高さが指定した値になるように、アスペクト比を固定して、リサイズする
    """
    h, w = img.shape[:2]
    width = round(w * (height / h))
    dst = cv2.resize(img, dsize=(width, height))

    return dst

def add(img1, img2, top, left): #put img2 on img1 / img2の上にimg1を載せる
    height, width = img1.shape[:2]
    img2[top:height + top, left:width + left] = img1

output_dir = find_data_file("24h_video_output")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# encoder(for mp4)
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
# output file name, encoder, fps, size(fit to image size)
#video = cv2.VideoWriter('takingphotos_24h.mp4', fourcc, 1, (1920, 1080))
video = cv2.VideoWriter(output_dir + '/takingphotos_24h.mp4', fourcc, 1, (1080, 1920))


for i in range(86400):
    dt_sec = datetime.timedelta(seconds=i)
    h, m, s = get_h_m_s(dt_sec)

    hh = (str(h)).zfill(2)
    mm = (str(m)).zfill(2)
    ss = (str(s)).zfill(2)

    time_now = hh + mm + ss + "_" #for file search / ファイル検索のため

    files = glob.glob(find_data_file("all_photos") + "/" + time_now + "*")
    print(files)

    black_back = cv2.imread(find_data_file("black_back.jpg"))

    if len(files) == 0:
        frame = cv2.imread(find_data_file("white_back.jpg")) #blank
        frame = cv2.putText(frame, hh + ":" + mm + ":" + ss, (700, 960), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 5, cv2.LINE_AA)
        #frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    else:
        file = random.choice(files) #Select one image at random if multiple images are available / 2枚以上あるときランダムに取り出す
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

    video.write(frame)

video.release()
