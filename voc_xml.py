import os
import xml.etree.ElementTree as ET
from os import getcwd

ROOT = 'VOCdevkit/VOC2007/'

def get_name(txt_path):
    with open(txt_path) as f:
        pic_names = f.readlines()
    pic_names = [c.strip() for c in pic_names]
    return pic_names



if __name__ == "__main__":
    image_name = get_name(ROOT+'ImageSets/Main/train.txt')
    print(image_name)

    for n in image_name:
        xml_path = os.path.join(ROOT, 'Annotations', '{}.xml'.format(n))
        print(xml_path)
        doc = ET.parse(xml_path)
        root = doc.getroot()
        mything = root.find('name')
        print(mything)
        break