from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
import os
import string
from joblib import Parallel, delayed
import numpy as np
import gensim
import multiprocessing

# Load data and model
base_path = '../../../datasets/EmotionDataset/'
text_data_path = base_path + 'txt/'
idx_data_path = '../../../datasets/EmotionDataset/splits/train_all.txt'
model_path = base_path + 'models/word2vec/word2vec_model_EmotionsDataset.model'

# Create output files
dir = "emotionDistribution_l2norm_gt"
gt_out_path = base_path + dir + '/train_EmotionDataset_l2norm.txt'
out_gt = open(gt_out_path, "w")

words2filter = ['rt','http','t','gt','co','s','https','http','tweet','markars_','photo','pictur','picture','say','photo','much','tweet','now','blog']
model = gensim.models.Word2Vec.load(model_path)

emotions = ['amusement','contentment','excitement','sadness','fear','disgust','anger','awe']

size = 8 # vector size
cores = multiprocessing.cpu_count()

def img_exists(path):
    im_path = base_path + "img/" + path
    return os.path.isfile(im_path)

#Initialize Tokenizer
tokenizer = RegexpTokenizer(r'\w+')
en_stop = get_stop_words('en')

# add own stop words
for w in words2filter:
    en_stop.append(w)

whitelist = string.letters + string.digits + ' '

def infer_word2vec(id, caption):
    filtered_caption = ""
    caption = caption.replace('#', ' ')
    for char in caption:
        if char in whitelist:
            filtered_caption += char
    filtered_caption = filtered_caption.decode('utf-8').lower()
    #Gensim simple_preproces instead tokenizer
    tokens = gensim.utils.simple_preprocess(filtered_caption)
    stopped_tokens = [i for i in tokens if not i in en_stop]
    tokens_filtered = [token for token in stopped_tokens if token in model.wv.vocab]


    embedding = np.zeros(size)
    c = 0
    for tok in tokens_filtered:
        try:
            for i,e in enumerate(emotions):
                embedding[i] += model.wv.similarity(tok, e)
                # print "TOK: " + str(tok) + " EM: " + str(e) + " SIM: " + str(model.wv.similarity(tok, e))
            # print embedding
            c += 1
        except:
            #print "Word not in model: " + tok
            continue
    if c > 0:
        embedding /= c

    if min(embedding) < 0:
        embedding = embedding - min(embedding)

    # L2 normalized
    if sum(embedding) > 0:
        embedding = embedding / np.linalg.norm(embedding)

    return id, embedding
print "Out file is: " + gt_out_path
print "Reading data from: " + idx_data_path
data = {}
filenames = []
file = open(idx_data_path, "r")
for l in file:
    filenames.append(l.rstrip())

for i,file_name in enumerate(filenames):
    if i%1000 == 0:
        print str(i) + " / " + str(len(filenames))
    caption = ""
    filtered_caption = ""
    try:
        file = open(text_data_path + file_name.rstrip() + ".txt", "r")
        # print (text_data_path + file_name.rstrip() + ".txt")
    except:
        # print("txt not found")
        continue
    for line in file:
        caption = caption + line
    # Replace hashtags with spaces
    caption = caption.replace('#', ' ')
    # Keep only letters and numbers
    for char in caption:
        if char in whitelist:
            filtered_caption += char

    data[file_name + ".jpg"] = filtered_caption.decode('utf-8').lower()


parallelizer = Parallel(n_jobs=cores)
tasks_iterator = (delayed(infer_word2vec)(id,caption) for id, caption in data.iteritems())
results = parallelizer(tasks_iterator)
count = 0
for r in results:
    # Create splits random
    if sum(r[1]) == 0:
        print "Continuing, sum = 0"
        continue

    # Check if image file exists
    if not img_exists(str(r[0]).rstrip()):
        print "Img file does not exist: " + str(r[0].rstrip())
        continue
    else:
        print("Writing")

    try:
        out = str(r[0].rstrip())
        for v in r[1]:
            out = out + ',' + str(v)
        out = out + '\n'

        out_gt.write(out)

    except:
        print "Error writing to file: "
        print r[0].rstrip()
        continue

out_gt.close()

print "Done"
