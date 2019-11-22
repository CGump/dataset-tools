import glob
import os, shutil

import numpy as np
import xml.etree.ElementTree as ET
from skimage import io, transform
from PIL import Image

import cv2


class BatchPcik():
    '''
    批量判断图片维度，并挑出不符合的文件至error文件夹
    ！！！error文件夹如果没有可以新建功能！！！
    '''
    def __init__(self):
        self.imgdir_path = "F:/Fruit_dataset/fresh_fish/"
        self.xml_path = "test/"
        self.error_path = "test/error/"
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

    def find_wrong_pic(self, save_change="c"):
        '''
        处理非3通道、非RGB图片
        save_change: 为`"c"`时change模式，将非3通道、非RGB图片转换为3通道RGB图片
                     为`"r"`时remove模式，删除不符合的图片
                     为`"m"`时move模式，移动图片至指定文件夹
        '''
        filelist = os.listdir(self.imgdir_path)
        if save_change == "c":
            for filename in filelist: 
                image_file = Image.open(self.imgdir_path + filename)
                image_file.convert('RGB').save(self.imgdir_path + filename)
        elif save_change == "r":
            for filename in filelist:
                os.remove(self.imgdir_path + filename)
        elif save_change == "m":
            is_exists = os.path.exists(self.error_path)
            os.makedirs(self.error_path) if not is_exists else print("目录已存在")
            for filename in filelist:
                shutil.move(self.imgdir_path + filename, self.error_path)
        else:
            print("the config \"save_change\" must choose in 'c' or 'r' or 'm'")
        
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

    def rename_batch (self, batch, suffix='.jpg', i_num=1):
        '''
        数据集名称中标签项修改，例如：   
        apple_01_0001.jpg -> apple_04_0001.jpg   
        apple_01_0001.xml -> apple_04_0001.xml   
        batch: 修改后的批次名称   
        suffix: 文件的后缀名   
        i_num: 文件的序号   
        '''
        filelist = os.listdir(self.imgdir_path)  # 获取文件路径 
        for filename in filelist:
            pic_1, _, pic_3 = filename.split('_')  # 获取文件名，序号+后缀
            if (pic_1 in self.classes) and filename.endswith(suffix): 
                src = os.path.join(os.path.abspath(self.imgdir_path), filename) 
                dst = os.path.join(os.path.abspath(self.imgdir_path), pic_1 + '_' + batch + '_' + pic_3)
                try: 
                    os.rename(src, dst) 
                    print ('converting %s to %s ...' % (src, dst)) 
                    i_num = i_num + 1
                except: 
                    continue
        print ('total %d to rename & converted %d jpgs' % (len(filelist), i_num-1))

    def rename_dataset(self, batch, suffix='.jpg', xml_suffix='.xml'):
        '''
        修改数据集批次信息，包括图片名和xml标注文件名，以及标注文件内的图片名和图片路径
        apple_01_0001.jpg -> apple_04_0001.jpg   
        apple_01_0001.xml -> apple_04_0001.xml   
        batch：`str`，修改后的批次号
        suffix：图像的后缀名，默认为`.jpg`
        xml_suffix：标注文件后缀名，默认为`.xml`
        '''
        filelist = os.listdir(self.imgdir_path)  # 获取文件路径 
        for filename in filelist:
            # filename已知 filename="apple_01_0001.jpg" 修改前
            pic_1, _, pic_3 = filename.split('_') # apple  01  0001.jpg
            seach_name = filename.split('.')[0] # 用来索引xml文件的apple_01_0001
            new_pic_name = pic_1 + '_' + batch + '_' + pic_3  # 新名字apple_04_0001.jpg
            xml_name = seach_name + xml_suffix  # xml_name 此时为修改前 apple_01_0001.xml
            xml_1, _, xml_3 = xml_name.split('_') # 提取出来后：apple  01  0001.xml
            new_xml_name = xml_1 + '_' + batch + '_' + xml_3  # 重新组合批次信息，apple_04

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
                print("---filename:%s has been modified---"%(filename))
            except:
                continue

    def change_xml_all(self, suffix='.jpg'):
        '''
        修改xml文件中的filename和path   
        xml文件的文件名与其内部filename和path不对应   
        通过xml文件名提取信息，拼装`.jpg`后缀即可
        suffix：默认后缀为`.jpg`
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

    def get_train_name(self, write_path, suffix='.jpg'):
        '''
        读取数据集中所有图像的名称，并写入文本文件
        write_path：文本文件的存放路径
        '''
        filelist = os.listdir(self.imgdir_path)
        filelist.sort()  # 原地修改
        f = open(write_path, 'w')
        for filename in filelist:
            if filename.endswith(suffix):
                write_name = filename.split('.')[0] + '\n'
                f.write(write_name)
        f.close()

if __name__ == "__main__":
    demo = BatchPcik()
    #demo.error_path = "F:/Fruit_dataset/pick_img/error_img/"
    key = 2
    if key == 1 :
        # 测试修改批次号方法
        demo.imgdir_path = "E:/fruit_server/VOCdevkit/VOC2007/Annotations/"
        demo.classes = ["apple"]
        batch = "04"
        demo.rename_batch(batch, suffix='.xml') 
    elif key == 2:
        demo.classes = ["apple", "avocado", "broccoli", "carrot", "chinese-cabbage", "coconut",
                        "coconut", "corn", "hami-melon", "lemon", "mix" ,"onion", "orange",
                        "pear", "pomegranate", "pomelo", "sweet-potato"]
        for class_name in demo.classes:
            demo.imgdir_path = 'E:/fruit_server/15class_05/15/%s'%(class_name) 
            demo.rename(class_name, batch='05', i_num=1)
    elif key == 3:
        demo.xml_path = "E:/fruit_server/VOCdevkit/VOC2007/Annotations/"
        demo.change_xml_all()
    elif key == 4:
        # 同时修改图片名，标注名和标注信息内的图片名、图片地址
        demo.imgdir_path = "E:/fruit_server/VOCdevkit/VOC2007/JPEGImages/"
        demo.xml_path = "E:/fruit_server/VOCdevkit/VOC2007/Annotations/"
        demo.classes = ["apple","kiwi","mango","mangosteen","mix","orange","pear","peach","pomegranate"]
        demo.rename_dataset("04")
    elif key == 5:
        demo.imgdir_path = "VOC2007/JPEGImages/"
        write_path = "VOC2007/ImageSets/Main/train.txt"
        demo.get_train_name(write_path)
        
    elif key == 6:
        demo.imgdir_path = "test/error_img/"
        demo.find_wrong_pic(save_change='m')

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