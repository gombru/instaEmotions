# Resizes the images in a folder and creates a resized datasetcd in another
# It also filters  corrupted images

import glob
from PIL import Image
from joblib import Parallel, delayed
import os
from shutil import copyfile
import time

images_path = "../../../hd/datasets/instaEmotions/img/"
im_dest_path = "../../../hd/datasets/instaEmotions/img_resized/"

minSize = 256


def resize(file):
    try:

        im = Image.open(file)

        w = im.size[0]
        h = im.size[1]

        # print "Original w " + str(w)
        # print "Original h " + str(h)

        if w < h:
            new_width = minSize
            new_height = int(minSize * (float(h) / w))

        if h <= w:
            new_height = minSize
            new_width = int(minSize * (float(w) / h))

        # print "New width "+str(new_width)
        # print "New height "+str(new_height)
        im = im.resize((new_width, new_height), Image.ANTIALIAS)
        if not os.path.exists(im_dest_path + file.split('/')[-2]):
            os.makedirs(im_dest_path + file.split('/')[-2])
        im.save(im_dest_path + file.split('/')[-2] + '/' +  file.split('/')[-1])

    except:
        print "Failed copying image. Removing image and caption " + str(file)
        try:
            # os.remove(file.replace("img", "json").replace("jpg", "json"))
            # os.remove(file)
            # os.remove(file.replace("img", "json_filtered").replace("jpg", "json"))
            print "Removed"
        except:
            print "Cannot remove " + str(file)
            return
        print "Removed"
        return


if not os.path.exists(im_dest_path):
    os.makedirs(im_dest_path)
dirs = [dI for dI in os.listdir(images_path) if os.path.isdir(os.path.join(images_path, dI))]
c = 0
for dir in dirs:
    print dir
    Parallel(n_jobs=1)(delayed(resize)(file) for file in glob.glob(images_path + dir + "/*.jpg"))