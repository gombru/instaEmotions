# Load trained LDA model and inferinstaEmotions_text_data_path = '../../../hd/datasets/instaEmotions/captions.json'
# Make the train/val/test splits for CNN regression training
# It also creates the splits train/val/test randomly

from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import os
from random import randint
import string
from joblib import Parallel, delayed
import numpy as np
import gensim
import multiprocessing
from load_jsons import *

# Load data and model
base_path = '../../../hd/datasets/instaEmotions/'
text_data_path = base_path + 'txt/'
model_path = base_path + 'models/word2vec/word2vec_model_instaEmotions.model'

instaEmotions_text_data_path = base_path + 'json_filtered'

# Create output files
dir = "word2vec_l2norm_gt"
gt_out_path = base_path + dir + '/train_instaEmotions_l2norm.txt'
out_gt = open(gt_out_path, "w")

words2filter = ['rt','http','t','gt','co','s','https','http','tweet','markars_','photo','pictur','picture','say','photo','much','tweet','now','blog']
model = gensim.models.Word2Vec.load(model_path)

size = 300 # vector size
cores = multiprocessing.cpu_count()

def img_exists(path):
    im_path = base_path + "img/" + path + ".jpg"
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
    caption = caption['caption']
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
            embedding += model[tok]
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

print "Loading data"
data = load(instaEmotions_text_data_path)

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
    if not img_exists(str(r[0])):
        print "Img file does not exist"
        continue

    try:
        out = str(r[0])
        for v in r[1]:
            out = out + ',' + str(v)
        out = out + '\n'

        out_gt.write(out)

    except:
        print "Error writing to file: "
        print r[0]
        continue

out_gt.close()

print "Done"
