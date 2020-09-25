import math
import json
import pickle
import random
from gensim import models
from gensim import matutils
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from time import time
from nltk.tokenize import sent_tokenize
import glob
import shutil








files="yelp_dataset_challenge_academic_dataset/"
buisness=files+"yelp_academic_dataset_business.json"
reviewsPath=files+"yelp_academic_dataset_review.json"

def main(save_sample,save_categories):
    search_category = 'Restaurants' 
    busID = []
    co = 0
    with open(buisness,'r') as f:
        for line in f.readlines():
            bus_json = json.loads(line)
            categories = bus_json['categories']
            #print(bus_json['business_id'])
            #print(categories)
            if search_category in categories and bus_json['review_count']>=120:
                co += 1
                print(co)
                busID.append(bus_json['business_id'])       
    positive_reviews = ""
    negative_reviews = ""
    pr = 0
    nr = 0
    with open(reviewsPath,'r') as f:
        for line in f.readlines():
            rev_json = json.loads(line)
            resID = rev_json['business_id']
            if resID in busID and rev_json['stars']>=4:
                positive_reviews += rev_json['text']
                pr += 1
            elif resID in busID and rev_json['stars']<=2:
                negative_reviews += rev_json['text']
                nr +=1 
                if(nr == 100):
                    break
            else:
                continue
            print(pr,nr)
    print(positive_reviews)
    print(negative_reviews)
    with open("neg_rev.txt",'w') as f:
        f.write(negative_reviews)

    vectorizer = TfidfVectorizer(max_df=0.5, max_features=1000,
                                     min_df=2, stop_words='english',
                                     ngram_range=(1, 2),
                                     use_idf=True)
    text = []
    with open ("neg_rev.txt", 'r') as f:
        text = f.readlines()
    X = vectorizer.fit_transform(text)
    id2words ={}
    for i,word in enumerate(vectorizer.get_feature_names()):
        id2words[i] = word
    corpus = matutils.Sparse2Corpus(X,  documents_columns=False)
    lda = models.ldamodel.LdaModel(corpus, num_topics=5, id2word=id2words)
    output_text = []
    for i, item in enumerate(lda.show_topics(num_topics=5, num_words=30, formatted=False)):
        output_text.append("Topic: " + str(i))
        re,terms = item
        for (wording,wei) in terms:
            output_text.append( wording + " : " + str(wei) )
    outputfile = "out.txt"
    print("writing topics to file:", outputfile)
    with open ( outputfile , 'w' ) as f:
        f.write('\n'.join(output_text))


    output_json = []
    for i, item in enumerate(lda.show_topics(num_topics=5, num_words=30, formatted=False)):
        print(item)
        temp1,itex = item
        topic_terms = {term: str(weight) for term,weight in itex}
        output_json.append(topic_terms)

    with open(outputfile + '.json', 'w') as f:
        json.dump(output_json, f)





            













if __name__ == "__main__":
    main(True,True)