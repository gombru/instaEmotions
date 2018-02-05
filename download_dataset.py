import glob
import urllib
import os

data_path = "../../datasets/EmotionDataset/agg"
out_path = "../../datasets/EmotionDataset/img_filtered/"

for file_name in glob.glob(data_path + "/*.csv"):
    print file_name
    with open(file_name, 'r') as file:
        for line in file:
            try:
                data = line.split(',')
                if int(data[3]) < 3: continue # That's the paper acceptance threshold
                out_name = data[1].split('/')[-1]

                if not os.path.exists(out_path + data[0]):
                    os.makedirs(out_path + data[0])

                out_name = out_path + data[0] + '/' + out_name
                urllib.urlretrieve(data[1], out_name)
            except:
                print "Error with line: " + str(data)

