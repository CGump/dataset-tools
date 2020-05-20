import os  
import random  

root = 'VOCdevkit/VOC2007/'
train = 0.9  
val = 0.1 
xmlfilepath = root + 'Annotations'  
txtsavepath = root + 'ImageSets/Main'  
total_xml = os.listdir(xmlfilepath)  
 
num = len(total_xml)  
list = range(num)  
tv = int(num * train)  
train_num = random.sample(list, tv)  
 
ftrainval = open(txtsavepath+'/trainval.txt', 'w')  
ftrain = open(txtsavepath+'/train.txt', 'w')  
fval = open(txtsavepath+'/val.txt', 'w')  

for i  in list:  
    name=total_xml[i][:-4]+'\n'  
    ftrainval.write(name)
    if i in train_num:  
        ftrain.write(name)  
    else:  
        fval.write(name)  
 
ftrainval.close()  
ftrain.close()  
fval.close()  
