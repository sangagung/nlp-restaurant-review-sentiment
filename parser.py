import xml.etree.ElementTree as ET
import csv
from review_struct import Review
import review_struct
import nltk
# import pandas as pd
# import os

review_map = {} 
review_conflict = {}
food_asp = []
price_asp = []
service_asp = []
ambience_asp = []

test_map = {} 

def parseDoc(path, trainer):
    tree = ET.parse(path)
    corpus = tree.getroot()

    for review in corpus:
        review_asp = {}
        for aspects in review.iter('aspects'):
            for aspect in aspects.iter('aspect'):
                review_asp[aspect.attrib['category']] = aspect.attrib['polarity']
        rev = Review(review.attrib['rid'], review.find('text').text, review_asp, trainer)

        review_map[review.attrib['rid']] = rev
        
        words_filtered = [e.lower() for e in review.find('text').text.split() if len(e) >= 3]

        if review_asp.get('FOOD', False):
            food_asp.append((words_filtered, review_asp.get('FOOD', False)))
        
        if review_asp.get('PRICE', False):
            price_asp.append((words_filtered, review_asp.get('PRICE', False)))
        
        if review_asp.get('SERVICE', False):
            service_asp.append((words_filtered, review_asp.get('SERVICE', False)))
        
        if review_asp.get('AMBIENCE', False):
            ambience_asp.append((words_filtered, review_asp.get('AMBIENCE', False)))

def parseTest(path, trainer):
    tree = ET.parse(path)
    corpus = tree.getroot()

    for review in corpus:
        review_asp = {}
        for aspects in review.iter('aspects'):
            for aspect in aspects.iter('aspect'):
                review_asp[aspect.attrib['category']] = aspect.attrib['polarity']
        rev = Review(review.attrib['rid'], review.find('text').text, review_asp, trainer)
        test_map[review.attrib['rid']] = rev

def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
        all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

dataset1 = 'dataset-xml/dataset_part_31_correction.xml'
dataset3 = 'dataset-xml/dataset_part_33_correction.xml'
datasettest = 'dataset_test.xml'
print(len(review_map))
parseDoc(dataset1, 'agung')
print(len(review_map), '1')
parseDoc(dataset3, 'fatah')
print(len(review_map), '3')
parseTest(datasettest,'machine')

for rid, review in review_map.items():
    print(review_struct.printcsv(review))

for service in service_asp:
    print(service)


##food
word_features = get_word_features(get_words_in_tweets(food_asp))
training_set = nltk.classify.apply_features(extract_features, food_asp)
classifier = nltk.NaiveBayesClassifier.train(training_set)

print(classifier.show_most_informative_features(32))

food_label = []
for rid, review in test_map.items():
    classification = classifier.classify(extract_features(review_struct.gettext(review).split()))
    food_label.append((review_struct.gettext(review), classification))
    review.add_aspect('FOOD', classification)

##price
word_features = get_word_features(get_words_in_tweets(price_asp))
training_set = nltk.classify.apply_features(extract_features, price_asp)
classifier = nltk.NaiveBayesClassifier.train(training_set)

print(classifier.show_most_informative_features(32))

price_label = []
for rid, review in test_map.items():
    classification = classifier.classify(extract_features(review_struct.gettext(review).split()))
    price_label.append((review_struct.gettext(review), classification))
    review.add_aspect('PRICE', classification)

##service
word_features = get_word_features(get_words_in_tweets(service_asp))
training_set = nltk.classify.apply_features(extract_features, service_asp)
classifier = nltk.NaiveBayesClassifier.train(training_set)

print(classifier.show_most_informative_features(32))

service_label = []
for rid, review in test_map.items():
    classification = classifier.classify(extract_features(review_struct.gettext(review).split()))
    service_label.append((review_struct.gettext(review), classification))
    review.add_aspect('SERVICE', classification)

##ambience
word_features = get_word_features(get_words_in_tweets(ambience_asp))
training_set = nltk.classify.apply_features(extract_features, ambience_asp)
classifier = nltk.NaiveBayesClassifier.train(training_set)

print(classifier.show_most_informative_features(32))

ambience_label = []
for rid, review in test_map.items():
    classification = classifier.classify(extract_features(review_struct.gettext(review).split()))
    ambience_label.append((review_struct.gettext(review), classification))
    review.add_aspect('AMBIENCE', classification)



with open('dataset-csv/test_3.csv', 'w', encoding='utf-8') as csvfile:
    fieldnames = ['rid', 'text', 'food', 'price', 'service', 'ambience', 'trainer']
    writer = csv.writer(csvfile)
    writer.writerow(fieldnames)
    for rid, review in test_map.items():
        r = review_struct.printcsv(review)
        print(r)
        writer.writerow(r)
            

# with open('dataset-conflict.csv', 'w', encoding='utf-8') as csvfile:
#     fieldnames = ['rid', 'text', 'food', 'price', 'service', 'ambience', 'trainer']
#     writer = csv.writer(csvfile)
#     writer.writerow(fieldnames)
# # for rid, review in review_map:
# #     print(review_struct.printcsv(review))
#     for rid, review in review_conflict.items():
#         writer.writerow(review_struct.printcsv(review))