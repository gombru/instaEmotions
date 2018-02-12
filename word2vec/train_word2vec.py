from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
import gensim
import string
import glob
import multiprocessing
import json
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import sys
sys.path.insert(0, '../datasetCode/')
from load_jsons import *

cores = multiprocessing.cpu_count()

finetune = True
if finetune:
    print "Loading pretrained model"
    pretrained_model_path = '../../../datasets/word2vec_pretrained/GoogleNews-vectors-negative300.bin'
    model = gensim.models.KeyedVectors.load_word2vec_format(pretrained_model_path, binary=True)


whitelist = string.letters + string.digits + ' '
text_data_path = '../../../hd/datasets/EmotionDataset/txt/'
idx_data_path = '../../../hd/datasets/EmotionDataset/splits/train_all.txt'
model_path = '../../../hd/datasets/EmotionDataset/models/word2vec/word2vec_model_EmotionsDataset.model'
words2filter = ['rt','http','t','gt','co','s','https','http','tweet','markars_','photo','pictur','picture','say','photo','much','tweet','now','blog','wikipedia','google', 'flickr', 'figure', 'photo', 'image', 'homepage', 'url', 'youtube','wikipedia','google', 'flickr', 'figure', 'photo', 'image', 'homepage', 'url', 'youtube', 'images', 'blog', 'pinterest']
instaEmotions_text_data_path = '../../../hd/datasets/instaEmotions/json_filtered/'

size = 300 # vector size
min_count = 5 # minimum word count to 2 in order to give higher frequency words more weighting
iter = 50 # iterating over the training corpus x times
window = 8

#Initialize Tokenizer
tokenizer = RegexpTokenizer(r'\w+')
en_stop = get_stop_words('en')
es_stop = get_stop_words('es')
ca_stop = get_stop_words('ca')
for w in es_stop:
    en_stop.append(w)
for w in ca_stop:
    en_stop.append(w)
# add own stop words
for w in words2filter:
    en_stop.append(w)

posts_text = [] #List of lists of tokens


def get_EmotionsDataset():
    posts_text = []
    filenames = []
    file = open(idx_data_path, "r")
    for l in file:
        filenames.append(l)

    for file_name in filenames:
        caption = ""
        filtered_caption = ""
        print text_data_path + file_name.strip('\n') + ".txt"
        try:
            file = open(text_data_path + file_name.strip('\n') + ".txt", "r")
        except:
            print("txt not found, skipping")
            continue
        for line in file:
            caption = caption + line
        # Replace hashtags with spaces
        caption = caption.replace('#', ' ')
        # Keep only letters and numbers
        for char in caption:
            if char in whitelist:
                filtered_caption += char

        posts_text.append(filtered_caption.decode('utf-8').lower())

    return posts_text

def get_instaEmotions():
    data = load(instaEmotions_text_data_path)
    for k, v in data.iteritems():
        filtered_caption = ""
        caption = v['caption']
        caption = caption.replace('#', ' ')
        for char in caption:
            if char in whitelist:
                filtered_caption += char
        posts_text.append(filtered_caption.decode('utf-8').lower())
    return posts_text

posts_text = get_EmotionsDataset()

print "Number of posts: " + str(len(posts_text))

print "Creating tokens"
c= 0

texts = []
for t in posts_text:

    c += 1
    if c % 10000 == 0:
        print c

    try:
        #Gensim simple_preproces instead tokenizer
        tokens = gensim.utils.simple_preprocess(t)
        # remove stop words from tokens
        stopped_tokens = [i for i in tokens if not i in en_stop]
        texts.append(stopped_tokens)
    except:
        continue

posts_text = []

#Train the model
print "Training ..."
if finetune:
    print model.iter
    model.train(texts, total_examples=model.corpus_count, epochs=25, compute_loss=False)
else:
    model = gensim.models.Word2Vec(texts, size=size, min_count=min_count, workers=cores, iter=iter, window=window)

model.save(model_path)
print "DONE"