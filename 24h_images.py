import cv2
import glob

def hconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    h_min = min(im.shape[0] for im in im_list)
    im_list_resize = [cv2.resize(im, (int(im.shape[1] * h_min / im.shape[0]), h_min), interpolation=interpolation)
                      for im in im_list]
    return cv2.hconcat(im_list_resize)

for i in range(0, 24):
    tgt_h = str(i).zfill(2)
    files = glob.glob("all_photos/" + tgt_h + "*")

    images = []
    for file in sorted(files):
        img = cv2.imread(file)
        if img is not None:
            images.append(img)

    if not images:
        pass
    else:
        #Arrange the photos in order horizontally / 写真を横に並べる
        im_h_resize = hconcat_resize_min(images)
        #
        #Set the size of the output image / 出力画像のサイズを決める
        img_resize = cv2.resize(im_h_resize, dsize=(4618, 3464))
        cv2.imwrite('24h_images/' + tgt_h + '.jpg', img_resize)