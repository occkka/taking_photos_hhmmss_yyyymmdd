from PIL import Image
import PIL.ExifTags as ExifTags
from pathlib import Path
import datetime
import os

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

for filename in Path("all_photos").glob("*.[Jj][Pp][Gg]"):
    exif_dict = get_exif_of_image(filename)

    if "DateTimeOriginal" in exif_dict:
        #create a new file name based on the time of day the image was taken
        file_dateTime = datetime.datetime.strptime(exif_dict["DateTimeOriginal"], "%Y:%m:%d %H:%M:%S")
    else:
        #use the last modified time if no exif is available
        #change the code if you are using an OS other than mac
        bt = os.stat(filename).st_birthtime
        file_dateTime = datetime.datetime.fromtimestamp(bt)

    file_dateTime = file_dateTime.strftime("%H%M%S_%Y%m%d.jpg")
    new_name = Path(filename).with_name(file_dateTime)
    filename.rename(new_name)




