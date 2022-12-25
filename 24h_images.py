import os
import glob
import sys
from PIL import Image

#exe
def find_data_file(filename):
   if getattr(sys, "frozen", False):
       # The application is frozen
       datadir = os.path.dirname(sys.executable)
   else:
       # The application is not frozen
       # Change this bit to match where you store your data files:
       datadir = os.path.dirname(sys.argv[0])
   return os.path.join(datadir, filename)

#resize by height
def scale_to_height(img, height):
    width = round(img.width * height / img.height)
    return img.resize((width, height))

def get_concat_h_multi_resize(im_list, resample=Image.BICUBIC):
    min_height = min(im.height for im in im_list)
    im_list_resize = [im.resize((int(im.width * min_height / im.height), min_height), resample=resample)
                      for im in im_list]
    total_width = sum(im.width for im in im_list_resize)
    dst = Image.new('RGB', (total_width, min_height))
    pos_x = 0
    for im in im_list_resize:
        dst.paste(im, (pos_x, 0))
        pos_x += im.width
    return dst

output_dir = find_data_file("24h_images_output")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for i in range(0, 24):
    tgt_h = str(i).zfill(2)
    files = glob.glob(find_data_file("all_photos") + '/' + tgt_h + "*")
    print(tgt_h + "時...")

    images = []
    for file in sorted(files):
        img = Image.open(file)
        if img is not None:
            scale_to_height(img, 1440)
            images.append(img)

    if not images:
        #make a white image
        white_img = Image.new("L", (1920, 1440), 255)
        white_img.save(output_dir + '/' + tgt_h + '.jpg')
    else:
        # Arrange the photos in order horizontally
        img_all = get_concat_h_multi_resize(images)
        img_all = img_all.resize((1920, 1440), Image.LANCZOS)
        img_all.save(output_dir + '/' + tgt_h + '.jpg')
