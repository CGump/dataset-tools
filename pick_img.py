import glob
import os
import shutil

import numpy as np
import xml.etree.ElementTree as ET
from skimage import io, transform

import cv2


class BatchPcik():
    '''
    批量判断图片维度，并挑出不符合的文件至error文件夹
    ！！！error文件夹如果没有可以新建功能！！！
    '''
    def __init__(self):
        self.imgdir_path = "F:/Fruit_dataset/fresh_fish/"
        self.xml_path = "test/"
        self.error_path = "F:/Fruit_dataset/error_img/"
        self.classes = ["apple","avocado","banana","beefsteak","blueberry","carambola","cherries","chicken","coconut","durian",
                        "fig","fish","grape","hamimelon","hawthorn","kiwano","kiwi","lemon","litchi","longan","loquat","mango",
                        "mangosteen","mulberry","muskmelon","orange","pawpaw","peach","pear","pemelo","pepinomelon","persimmon",
                        "pineapple","pitaya","pomegranate","rambutan","strawberry","watermelon","waxberry","mix"]

    def read_image(self):

        w = 100
        h = 100
        c = 3
        path = self.imgdir_path
        cate = [path + x for x in os.listdir(path) if os.path.isdir(path+x)]
        images = []
        labels = []
        for index, folder in enumerate(cate):
            for im in glob.glob(folder + '/*.jpg'):
                img = io.imread(im)
                try:
                    if img.shape[2] == c:
                        img = transform.resize(img, (w, h))
                        images.append(img)
                        labels.append(index)
                        print(im)
                    else:
                        print(im, ' IS WRONG')
                except:
                    continue
            print('label %d is:' % index, folder)
        return np.asarray(images, np.float32), np.asarray(labels, np.int32)

    def find_wrong_pic(self):
        '''
        记录并移动错误图片
        '''
        dir_list = os.listdir(self.imgdir_path)
        for _, name in enumerate(dir_list):  
            img = io.imread(self.imgdir_path + name)
            img_size = img.shape # 图片的尺寸
            img_path = self.imgdir_path + name # 图片的名
            img_len = len(img_size) # 求取图片维度
            if img_len != 3:
                print('尺寸错误的图片是：', name, '具体尺寸为：', img_size, '维度是：', img_len)
                shutil.move(img_path, self.error_path)
            if img_size[2] != 3:
                print('非3通道图片：', name , img_size)
                new_img = cv2.imread(img_path)
                cv2.imwrite(img_path, new_img)# 需要改进'''
        return True

    def rename (self, pic_name, batch, i_num):
        '''
        待修改
        功能：不同文件夹内图像批量重命名，要求文件夹命名格式一致
        或者文件夹内重命名，单独某一类
        以上两者需要可以同时实现，分类选择
        '''
        filelist = os.listdir(self.imgdir_path) #获取文件路径 
        total_num = len(filelist) #获取文件长度（个数） 
        i = i_num #表示文件的命名是从1开始的 
        for item in filelist:
            if item.endswith('.jpg'): #初始的图片的格式为jpg格式的（或者源文件是png格式及其他格式，后面的转换格式就可以调整为自己需要的格式即可）
                src = os.path.join(os.path.abspath(self.imgdir_path), item) 
                #dst = os.path.join(os.path.abspath(self.imgdir_path), ''+ '00' str(i) + pic_name + '.jpg') #处理后的格式也为jpg格式的，当然这里可以改成png格式 
                dst = os.path.join(os.path.abspath(self.imgdir_path), pic_name + '_' + batch + '_' + format(str(i), '0>4s') + '.jpg')    #这种情况下的命名格式为0000000.jpg形式，可以自主定义想要的格式 
                try: 
                    os.rename(src, dst) 
                    print ('converting %s to %s ...' % (src, dst)) 
                    i = i + 1
                except: 
                    continue
        print ('total %d to rename & converted %d jpgs' % (total_num, i))

    def rename_batch (self, pic_list, batch, suffix='.jpg', i_num=1):
        '''
        数据集名称中标签项修改，例如：   
        apple_01_0001.jpg -> apple_04_0001.jpg   
        apple_01_0001.xml -> apple_04_0001.xml   
        pic_list: `list`，需要修改批次号的数据集种类名称列表   
        batch: 修改后的批次名称   
        suffix: 文件的后缀名   
        i_num: 文件的序号   
        '''
        filelist = os.listdir(self.imgdir_path)  # 获取文件路径 
        for item in filelist:
            pic_name, _, pic_num = item.split('_')  # 获取文件名，序号+后缀
            if (pic_name in pic_list) and item.endswith(suffix): 
                src = os.path.join(os.path.abspath(self.imgdir_path), item) 
                dst = os.path.join(os.path.abspath(self.imgdir_path), pic_name + '_' + batch + '_' + pic_num)
                try: 
                    os.rename(src, dst) 
                    print ('converting %s to %s ...' % (src, dst)) 
                    i_num = i_num + 1
                except: 
                    continue
        print ('total %d to rename & converted %d jpgs' % (len(filelist), i_num-1))

    def rename_dataset(self, batch, suffix='.jpg', xml_suf='.xml'):
        filelist = os.listdir(self.imgdir_path)  # 获取文件路径 
        for filename in filelist:
            # filename已知 filename="apple_01_0001.jpg"
            pic_1, _, pic_3 = filename.split('_') # apple  01  0001.jpg
            seach_name = filename.split('.')[0] # 用来索引xml文件的apple_01_0001
            new_pic_name = pic_1 + '_' + batch + '_' + pic_3  # 新名字apple_04_0001.jpg
            xml_name = seach_name + xml_suf  # xml_name = apple_01_0001.xml
            xml_1, _, xml_3 = xml_name.split('_')
            new_xml_name = xml_1 + '_' + batch + '_' + xml_3

            if (pic_1 in self.classes) and filename.endswith(suffix):
                src = os.path.join(os.path.abspath(self.imgdir_path), filename)
                dst = os.path.join(os.path.abspath(self.imgdir_path), new_pic_name)
                src_xml = os.path.join(os.path.abspath(self.xml_path), xml_name)
                dst_xml = os.path.join(os.path.abspath(self.xml_path), new_xml_name)

                doc = ET.parse(self.xml_path + xml_name)
                root = doc.getroot()
                root.find("filename").text = new_pic_name
                root.find("path").text = self.imgdir_path + new_pic_name
                doc.write(self.xml_path + xml_name)

            try:
                os.rename(src, dst)
                os.rename(src_xml, dst_xml)
            except:
                continue

    def change_xml_all(self, suffix='.jpg'):
        '''
        修改xml中的filename中的batch
        升级逻辑思路：图片改->xml改->xml内容改，同步进行
        这样修改前的名字，修改后的名字，修改后图片的地址都可以通过图片索引拿到
        '''
        filelist = os.listdir(self.xml_path)
        for xmlfile in filelist:
            doc = ET.parse(self.xml_path + xmlfile)
            root = doc.getroot()
            alter1 = root.find('filename')
            alter1.text = xmlfile.split('.')[0] + suffix

            alter2 = root.find('path')
            alter2.text = alter2.text.rsplit('\\', 1)[0] + '\\' + xmlfile.split('.')[0] + suffix
            doc.write(self.xml_path + xmlfile)
            print("---done---")


if __name__ == "__main__":
    demo = BatchPcik()
    demo.error_path = "F:/Fruit_dataset/pick_img/error_img/"
    key = 4
    if key == 1 :
        # 测试修改批次号方法
        demo.imgdir_path = "E:/fruit_server/VOCdevkit/VOC2007/Annotations/"
        classes = ["apple"]
        batch = "04"
        demo.rename_batch(classes, batch, suffix='.xml') 
    elif key == 2:
        classes = ["apple","avocado","banana","beefsteak","blueberry","carambola","cherries","chicken","coconut","durian",
        "fig","fish","grape","hamimelon","hawthorn","kiwano","kiwi","lemon","litchi","longan","loquat","mango",
        "mangosteen","mulberry","muskmelon","orange","pawpaw","peach","pear","pemelo","pepinomelon","persimmon",
        "pineapple","pitaya","pomegranate","rambutan","strawberry","watermelon","waxberry"]
    elif key == 3:
        demo.xml_path = "E:/fruit_server/VOCdevkit/VOC2007/Annotations/"
        demo.change_xml_all()
    elif key == 4:
        # 同时修改图片名，标注名和标注信息内的图片名、图片地址
        demo.imgdir_path = "dataset/JPEGImages/"
        demo.xml_path = "dataset/Annotations/"
        demo.classes = ["apple"]
        demo.rename_dataset("04")


    elif key == 10:
        classes.append('mix')
        for class_name in classes:
            dirpath = "F:/Fruit_dataset/yolo_39class/test_image/%s"%(class_name)
            os.makedirs(dirpath)
            print("New folder has been done!-->" + dirpath)
    else:
        # 测试集制作
        classes.append('mix')
        for class_name in classes:
            batch = 'test'
            i_num = 1
            demo.imgdir_path = "F:/Fruit_dataset/yolo_39class/test_image/%s/"%(class_name)
            demo.find_wrong_pic()
            demo.rename(class_name, batch, i_num) 
   
    '''
    else:
        demo.imgdir_path = "F:/Fruit_dataset/meat_train/test/"
        data, label = demo.read_image()
        print(data.shape) 
    '''