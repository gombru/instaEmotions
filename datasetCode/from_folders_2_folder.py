import glob
from PIL import Image
from joblib import Parallel, delayed
import os
from shutil import copyfile
import time

im_path = "../../../hd/datasets/instaEmotions/img_resized/"
im_dest_path = "../../../hd/datasets/instaEmotions/img_resized_toguether/"

def copy(file):
    copyfile(file, im_dest_path + file.split('/')[-1])


dirs = [dI for dI in os.listdir(im_path) if os.path.isdir(os.path.join(im_path, dI))]
for dir in dirs:
    print dir
    Parallel(n_jobs=12)(delayed(copy)(file) for file in glob.glob(im_path + dir + "/*.jpg"))