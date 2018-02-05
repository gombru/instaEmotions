import numpy as np

model = 'classification_resize/EmotionsDataset_all_iter_7000'
data = np.loadtxt('../../datasets/EmotionDataset/results/'+model+'/test.txt', dtype=str)
test = np.loadtxt('../../datasets/EmotionDataset/gt_filtered/test.txt', dtype=str)

correct_class = np.zeros([8,1])
wrong_class = np.zeros([8,1])

acc = 0

for i,r in enumerate(data):
    print r
    gt_label = test[i].split(',')[1]

    if gt_label == r[1]:
        acc += 1
        correct_class[int(gt_label)] += 1
    else:
        wrong_class[int(gt_label)] += 1

total_acc = float(acc) / len(data)

print "ACC: " + str(total_acc)

print "% Correct per class:"
for i,v in enumerate(correct_class):
    if wrong_class[i] == 0:
        print "All Correct in class " + str(i)
    else:
        out = float(v) / (v + wrong_class[i])
        print "Class " + str(i) + ': ' + str(out)


