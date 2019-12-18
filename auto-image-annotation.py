# -*- coding: utf-8 -*-
import os, sys
import glob
from PIL import Image

class Auto_ann():
    def __init__(self):
        self.scr_img_dir = "auto-annotation/img" # 图像存储路径
        self.scr_xml_dir = "auto-annotation/xml" # 标注存储路径
        self.scr_txt_dir = "auto-annotation/txt" # 识别结果路径
        self.img_list = glob.glob(self.scr_img_dir + "/*.jpg") #["1.jpg","2.jpg"...]
        self.folder = self.scr_img_dir.split('/')[-1]
        self.img_basename = [os.path.basename(item) for item in self.img_list]

    def auto_annotation(self):
        for img in self.img_basename:
            width, height = Image.open(self.scr_img_dir + '/' + img).size
            img_name = os.path.splitext(img)[0]
            result_txt = open(self.scr_txt_dir + '/' + img_name + '.txt').read().splitlines()

            # 写入xml文件
            xml_file = open((self.scr_xml_dir + '/' + img_name + '.xml'), 'w')
            xml_file.write('<annotation>\n')
            xml_file.write('    <folder>' + self.folder + '</folder>\n')
            xml_file.write('    <filename>' + img + '</filename>\n')
            xml_file.write('    <source>\n')
            xml_file.write('        <database>Unknown</database>\n')
            xml_file.write('    </source>\n')
            xml_file.write('    <size>\n')
            xml_file.write('        <width>' + str(width) + '</width>\n')
            xml_file.write('        <height>' + str(height) + '</height>\n')
            xml_file.write('        <depth>3</depth>\n')
            xml_file.write('    </size>\n')
            xml_file.write('	<segmented>0</segmented>\n')

            # 写入标注信息
            # 标注信息格式：识别名称 置信度 xmin ymin xmax ymax
            for each_label in result_txt:
                spt = each_label.split(' ')
                xml_file.write('    <object>\n')
                xml_file.write('        <name>' + str(spt[0]) + '</name>\n')
                xml_file.write('        <pose>Unspecified</pose>\n')
                xml_file.write('        <truncated>0</truncated>\n')
                xml_file.write('        <difficult>0</difficult>\n')
                xml_file.write('        <bndbox>\n')
                xml_file.write('            <xmin>' + str(spt[2]) + '</xmin>\n')
                xml_file.write('            <ymin>' + str(spt[3]) + '</ymin>\n')
                xml_file.write('            <xmax>' + str(spt[4]) + '</xmax>\n')
                xml_file.write('            <ymax>' + str(spt[5]) + '</ymax>\n')
                xml_file.write('        </bndbox>\n')
                xml_file.write('    </object>\n')
            
            xml_file.write('</annotation>')
            xml_file.close()

if __name__ == "__main__":
    anno = Auto_ann()
    anno.auto_annotation()