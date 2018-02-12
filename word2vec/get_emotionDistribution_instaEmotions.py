from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
import os
import string
from joblib import Parallel, delayed
import numpy as np
import gensim
from random import randint
import multiprocessing

# Load data and model
base_path = '../../../hd/datasets/instaEmotions/'
text_data_path = base_path + 'txt/'
model_path = base_path + 'models/word2vec/word2vec_model_instaEmotions.model'

# Create output files
dir = "emotionDistribution_l2norm_gt"
train_out_path = base_path + dir + '/train_instaEmotions_l2norm.txt'
val_out_path = base_path + dir + '/val_instaEmotions_l2norm.txt'

train_file = open(train_out_path, "w")
val_file = open(val_out_path, "w")

words2filter = ['rt','http','t','gt','co','s','https','http','tweet','markars_','photo','pictur','picture','say','photo','much','tweet','now','blog']
model = gensim.models.Word2Vec.load(model_path)

emotions = ['amusement','anger','awe','contentment','disgust','excitement','fear','sadness']

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

        # Create splits random
        split = randint(0,19)
        if split < 19: train_file.write(out)
        else: val_file.write(out)

    except:
        print "Error writing to file: "
        print r[0].rstrip()
        continue

train_file.close()
val_file.close()

print "Done"
