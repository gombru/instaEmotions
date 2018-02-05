import glob
import random

data_path = '../../datasets/EmotionDataset/img/'
folders = ['amusement','anger','awe','contentment','disgust','excitement','fear','sadness']
out = '../../datasets/EmotionDataset/gt_all/'
train_gt = open(out + 'train.txt', 'w')
val_gt = open(out + 'val.txt', 'w')
test_gt = open(out + 'test.txt', 'w')

# If creating nto fitlered avoid using fitlered GT images to train
fitlered_gt_path = '../../datasets/EmotionDataset/gt_filtered/test.txt'
fitlered_gt_path_val = '../../datasets/EmotionDataset/gt_filtered/val.txt'
filtered_gt = open(fitlered_gt_path, 'r')
filtered_gt_val = open(fitlered_gt_path_val, 'r')
filtered_gt_data =[]

for f in filtered_gt:
    filtered_gt_data.append(f.split(',')[0].split('/')[1])
for f in filtered_gt_val:
    filtered_gt_data.append(f.split(',')[0].split('/')[1])

data = []
for i,f in enumerate(folders):
    for file_name in glob.glob(data_path + f + "/*.jpg"):
        file_name = file_name.split('/')[-2:]
        if file_name[1] not in filtered_gt_data:
            data.append([file_name[0] + '/' + file_name[1], i])

random.shuffle(data)
total = len(data)
for i, d in enumerate(data):

    # If not filtered, use all to train
    train_gt.write(d[0] + ',' + str(d[1]) + '\n')

    # if i < int(0.8*total):
    #     train_gt.write(d[0] + ',' + str(d[1]) + '\n')
    # elif i < int(0.85 * total):
    #     val_gt.write(d[0] + ',' + str(d[1]) + '\n')
    # else:
    #     test_gt.write(d[0] + ',' + str(d[1]) + '\n')

