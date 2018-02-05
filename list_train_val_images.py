import glob
import random

data_path = '../../datasets/EmotionDataset/img/'
folders = ['amusement','anger','awe','contentment','disgust','excitement','fear','sadness']
out = '../../datasets/EmotionDataset/splits/'
train_gt = open(out + 'train_all.txt', 'w')
val_gt = open(out + 'val_all.txt', 'w')

# If creating nto fitlered avoid using fitlered GT images to train
fitlered_gt_path = '../../datasets/EmotionDataset/gt_filtered/test.txt'
fitlered_gt_path_val = '../../datasets/EmotionDataset/gt_filtered/val.txt'
filtered_gt = open(fitlered_gt_path, 'r')
filtered_gt_val = open(fitlered_gt_path_val, 'r')
filtered_test_data =[]
filtered_val_data =[]


for f in filtered_gt:
    filtered_test_data.append(f.split(',')[0].split('/')[1])
for f in filtered_gt_val:
    filtered_val_data.append(f.split(',')[0].split('/')[1])

data = []
data_val = []
for i,f in enumerate(folders):
    for file_name in glob.glob(data_path + f + "/*.jpg"):
        file_name = file_name.split('/')[-2:]
        if file_name[1] in filtered_val_data:
            data_val.append([file_name[0] + '/' + file_name[1], i])
        elif file_name[1] not in filtered_gt:
            data.append([file_name[0] + '/' + file_name[1], i])

print("Train")
random.shuffle(data)
total = len(data)
for i, d in enumerate(data):
    train_gt.write(d[0][:-4] + '\n')

print("Val")
random.shuffle(data_val)
total = len(data_val)
for i, d in enumerate(data_val):
    val_gt.write(d[0][:-4]  + '\n')
