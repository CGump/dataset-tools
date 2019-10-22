import glob
import os
import shutil

import numpy as np
from skimage import io, transform

import cv2


class BatchPcik():
    '''
    批量判断图片维度，并挑出不符合的文件至error文件夹
    ！！！error文件夹如果没有可以新建功能！！！
    '''
    def __init__(self):
        self.imgdir_path = "F:/Fruit_dataset/fresh_fish/"
        self.error_path = "F:/Fruit_dataset/error_img/"
    
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
        filelist = os.listdir(self.imgdir_path) #获取文件路径 
        total_num = len(filelist) #获取文件长度（个数） 
        i = i_num #表示文件的命名是从1开始的 
        for item in filelist:
            if (class_name in item) and item.endswith('.jpg'): #初始的图片的格式为jpg格式的（或者源文件是png格式及其他格式，后面的转换格式就可以调整为自己需要的格式即可）
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

if __name__ == "__main__":
    demo = BatchPcik()
    demo.error_path = "F:/Fruit_dataset/pick_img/error_img/"
    '''
    classes = ["apple","avocado","banana","beefsteak","blueberry","carambola","cherries","chicken","coconut","durian",
            "fig","fish","grape","hamimelon","hawthorn","kiwano","kiwi","lemon","litchi","longan","loquat","mango",
            "mangosteen","mulberry","muskmelon","orange","pawpaw","peach","pear","pemelo","pepinomelon","persimmon",
            "pineapple","pitaya","pomegranate","rambutan","strawberry","watermelon","waxberry"]
    '''
    classes = []
    key = 1
    if key == 1 :
        class_name = "mangosteen_" #数据集标签
        batch = "04" #数据集制作批次
        i_num = 1 #表示文件的命名是从1开始的
        demo.imgdir_path = "VOC2007/JPEGImages/"
        #demo.find_wrong_pic()
        demo.rename(class_name, batch, i_num) 
    elif key == 2:
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

    '''
    test
    '''