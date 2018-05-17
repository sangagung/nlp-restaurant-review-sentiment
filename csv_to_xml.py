import pandas as pd
import os
import xml.etree.ElementTree as ET

PATH = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(PATH, "dataset-csv", "test_3.csv")
df = pd.read_csv(DATASET_PATH)

xml_str = '<corpus>\n'

aspects =  ['food','price','service','ambience']
for i in range(len(df.values)):
    xml_str += '<review rid="'+ str(df['rid'].values[i]) +'">\n'
    teks = str(df['text'].values[i])
    teks = teks.replace('<text>','')
    teks = teks.replace('</text>','')
    teks = teks.replace('&','&amp;')
    teks = teks.replace('<','&lt;')
    teks = teks.replace('>','&gt;')

    xml_str += "<text>"+  teks + "</text>\n"

    if(any(v != 0 for v in df[aspects].values[i])):
        xml_str +='<aspects>\n'
        for aspect in aspects:
            polarity = df[aspect].values[i]
            
            xml_str+= '<aspect category="'+aspect.upper()+'" polarity="'+polarity+'"/>\n'

        xml_str +='</aspects>\n'
    xml_str += '</review>\n'


xml_str += '</corpus>'

#tree = ET.ElementTree(ET.fromstring(xml_str))
#mydata = ET.tostring(tree)  
submission = open('submission_3.xml','w')
submission.write(xml_str)
submission.close
