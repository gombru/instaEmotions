emotions = ['amusement','contentment','excitement','sadness','fear','disgust','anger','awe']


from gensim import models

model_name = 'word2vec_model_EmotionsDataset.model'
model_path = '../../../datasets/EmotionDataset/models/word2vec/' + model_name
model_path = '../../../datasets/word2vec_pretrained/GoogleNews-vectors-negative300.bin'

print("Loading model ... ")
model = models.Word2Vec.load_word2vec_format(model_path, binary=True)

for e in emotions:
    print("EMOTION: " + e)
    print(model.wv.most_similar(positive=[e]))

#
# for m in emotions:
#     print m
#     print model.wv.similarity(m, 'baby')
#     print model.wv.similarity(m, 'beach')
#     print model.wv.similarity(m, 'winter')
#     print model.wv.similarity(m, 'night')
#     print model.wv.similarity(m, 'terrorism')
#     print model.wv.similarity(m, 'icecream')
#     print model.wv.similarity(m, 'sun')
#     print model.wv.similarity(m, 'laugh')
#     print model.wv.similarity(m, 'dead')
#     print model.wv.similarity(m, 'tears')
#     print model.wv.similarity(m, 'dark')