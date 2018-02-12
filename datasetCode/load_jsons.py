import glob
import json
import os

def load(path):
    data = {}
    print "Loading data"
    dirs = [dI for dI in os.listdir(path) if os.path.isdir(os.path.join(path, dI))]

    c = 0
    for dir in dirs:
        for file in glob.glob(path + dir+ "/*.json"):
            c += 1
            if c % 10000 == 0:
                print c
            with open(file) as data_file:
                try:
                    data[file.split('/')[-2] + '/' + file.split('/')[-1][:-5]] = json.load(data_file)
                except:
                    print "Failed decoding JSON, skipping"
                    continue
    return data

