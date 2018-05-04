import xml.etree.ElementTree as ET
import csv
from review_struct import Review
import review_struct


review_set = set([]) 

def parseDoc(path):
    tree = ET.parse('dataset-xml/dataset_part_31.xml')
    corpus = tree.getroot()

    for review in corpus:
        review_asp = {}
        for aspects in review.iter('aspects'):
            for aspect in aspects.iter('aspect'):
                review_asp[aspect.attrib['category']] = aspect.attrib['polarity']
        
        review_set.add(Review(review.attrib['rid'], review.find('text').text, review_asp))

dataset1 = 'dataset-xml/dataset_part_31.xml'
dataset2 = 'dataset-xml/dataset_part_32.xml'
dataset3 = 'dataset-xml/dataset_part_33.xml'
parseDoc(dataset1)
parseDoc(dataset2)
parseDoc(dataset3)

with open('dataset.csv', 'w', encoding='utf-8') as csvfile:
    fieldnames = ['rid', 'text', 'food', 'price', 'service', 'ambience']
    writer = csv.writer(csvfile)
    writer.writerow(fieldnames)
    
    for review in review_set:
        writer.writerow(review_struct.printcsv(review))