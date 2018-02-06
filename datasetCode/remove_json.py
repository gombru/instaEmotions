import glob
from joblib import Parallel, delayed
import os


images_path = "../../../hd/datasets/instaEmotions/json/"


def remove(file):
    if not os.path.isfile(file.replace("img_resized", "json").replace("jpg", "json")):
        try:
            print "Removed"
            os.remove(file)
        except:
            print "Cannot remove"
            return
        print "Removed"
        return


dirs = [dI for dI in os.listdir(images_path) if os.path.isdir(os.path.join(images_path, dI))]
c = 0
for dir in dirs:
    print dir
    Parallel(n_jobs=12)(delayed(remove)(file) for file in glob.glob(images_path + dir + "/*.json"))