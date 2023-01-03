from PIL import Image
import PIL.ExifTags as ExifTags
from pathlib import Path
import datetime
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
       datadir = os.path.dirname(sys.argv[0])
   return os.path.join(datadir, filename)

#get exif from image
def get_exif_of_image(file):
    im = Image.open(file)
    try:
        exif_dict = {
            ExifTags.TAGS[k]: v
            for k, v in im._getexif().items()
            if k in ExifTags.TAGS
        }
        return exif_dict
    except AttributeError:
        return {}

#output_dir = "24h_images"
output_dir = find_data_file("all_photos")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for filename in Path(find_data_file("for_sorting")).glob("*.[Jj][Pp][Gg]"):
    exif_dict = get_exif_of_image(filename)

    if "DateTimeOriginal" in exif_dict:
        #create a new file name based on the time of day the image was taken
        file_dateTime = datetime.datetime.strptime(exif_dict["DateTimeOriginal"], "%Y:%m:%d %H:%M:%S")
    else:
        #use the last modified time if no exif is available
        #change the code depending on OS
        #mac
        bt = os.stat(filename).st_birthtime
        #windows
        #bt = os.path.getctime(filename)
        file_dateTime = datetime.datetime.fromtimestamp(bt)

    file_dateTime = file_dateTime.strftime("%H%M%S_%Y%m%d.jpg")
    new_name = output_dir + '/' + file_dateTime
    filename.rename(new_name)
