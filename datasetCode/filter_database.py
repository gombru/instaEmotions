from load_jsons import *
import json
from shutil import copyfile
from langdetect import detect, detect_langs

filtered_jsons_dir = "../../../hd/datasets/instaEmotions/json_filtered/"
output_file_path = "../../../hd/datasets/instaEmotions/captions.json"

word_TH = 3

data = load("../../../hd/datasets/instaEmotions/json/")
print "Number of jsons: " + str(len(data))

# Load users blacklist
users_blacklist = []
users_blacklist_file = open("../../../hd/datasets/instaEmotions/users_blacklist50.txt", "r")
for line in users_blacklist_file:
    users_blacklist.append(line.replace('\n', ''))
users_blacklist_file.close()


discarded_by_user = 0
discarded_by_short_caption = 0
discarded_by_nul_caption = 0

output_data = {}

c = 0

for k, v in data.iteritems():

    c += 1
    if c % 50000 == 0:
        print c

    # Discard by user
    if v['owner']['id'] in users_blacklist:
        discarded_by_user += 1
        if discarded_by_user % 500 == 0:
            print "Num of posts dicarded by user: " + str(discarded_by_user)
        continue

    # Check if post has caption
    if 'caption' not in v:
        discarded_by_nul_caption += 1
        if discarded_by_nul_caption % 500 == 0:
            print "Num of posts dicarded by no caption: " + str(discarded_by_nul_caption)
        continue

    # Preprocess text: Here I only filter to be able to look for cities. The text processing will be done when training text models, because I want to save the captions as they are
    caption = v['caption']
    caption = caption.replace('#', ' ')
    caption = caption.lower()
    words = caption.split()

    # Check num of words. Discard if under the threshold
    if len(words) < word_TH:
        discarded_by_short_caption += 1
        if discarded_by_short_caption % 1000 == 0:
            print "Num of posts dicarded by short caption: " + str(discarded_by_short_caption)
        continue



    # Else save the data in a dir with keys the id and with values the captions (originals)
    output_data[k] = v['caption']

    # And save the original json in a separate folder
    with open(filtered_jsons_dir + k + '.json', 'w') as outfile:
        json.dump(v, outfile)

print "Discards: No captions: " + str(discarded_by_nul_caption) + " Short: " + str(
    discarded_by_short_caption) + " User: " + str(
    discarded_by_user)
print "Number of original vs resulting elements: " + str(len(output_data)) + " vs " + str(len(data))

print "Saving JSON"
with open(output_file_path, 'w') as outfile:
    json.dump(output_data, outfile)

print "Done"
