import xml.etree.ElementTree as ET
import csv
from review_struct import Review
import review_struct


review_map = {} 

def parseDoc(path, trainer):
    tree = ET.parse('dataset-xml/dataset_part_31.xml')
    corpus = tree.getroot()

    for review in corpus:
        review_asp = {}
        for aspects in review.iter('aspects'):
            for aspect in aspects.iter('aspect'):
                review_asp[aspect.attrib['category']] = aspect.attrib['polarity']
        if review.attrib['rid'] in review_map:
            print(review_map[review.attrib['rid']])
        review_map[review.attrib['rid']] = Review(review.attrib['rid'], review.find('text').text, review_asp)
        # review_set.add(Review(review.attrib['rid'], review.find('text').text, review_asp))

dataset1 = 'dataset-xml/dataset_part_31.xml'
dataset2 = 'dataset-xml/dataset_part_32.xml'
dataset3 = 'dataset-xml/dataset_part_33.xml'
print(len(review_map))
parseDoc(dataset1, 'agung')
print(len(review_map))
parseDoc(dataset2, 'faishal')
print(len(review_map))
parseDoc(dataset3, 'fatah')
print(len(review_map))

# for rid, review in review_map.items():
#     print(review_struct.printcsv(review))


with open('dataset.csv', 'w', encoding='utf-8') as csvfile:
    fieldnames = ['rid', 'text', 'food', 'price', 'service', 'ambience']
    writer = csv.writer(csvfile)
    writer.writerow(fieldnames)
# for rid, review in review_map:
#     print(review_struct.printcsv(review))
    for rid, review in review_map.items():
        writer.writerow(review_struct.printcsv(review))