# -*- coding: utf-8 -*-
import codecs
import numpy as np
import pandas as pd
import jieba
import jieba.posseg as pseg

def read_split_write(file_path,target_file_path):
    #1.read data
    file_object=codecs.open(file_path,mode='r',encoding='utf-8')
    target_object=codecs.open(target_file_path,mode='a',encoding='utf-8')
    lines=file_object.readlines()
    print("length of lines:",len(lines))
    for i,line in enumerate(lines):
        #2.split data.
        input_string,labels=line.strip().split("__label__")
        label_list=labels.split(" ")
        #3.write data
        target_object.write(input_string.strip()+" ")
        for label in label_list:
            target_object.write("__label__"+str(label)+" ")
        target_object.write("\n")
    target_object.close()
    file_object.close()


def loadDataSet2List(fileName):
    count = 0
    document = []
    biaoti = []
    file = open(fileName, encoding='utf-8')
    for line in file:
        # if count>10:break
        count += 1
        # (1)分隔
        my_array = line.split("@@@")
        title = my_array[0]
        content = my_array[1]
        if len(title) == 0 or len(content) == 0:
            continue
        # (2)分词
        temp_set = []
        tp_t_set = []
        segs = pseg.cut(title + content)
        seg_title = pseg.cut(title)
        for seg in segs:
            if seg.word != '\n':
                temp_set.append(seg.word)
        for st in seg_title:
            if st.word != '\n':
                tp_t_set.append(st.word)
        document.append(list(temp_set))
        biaoti.append(list(tp_t_set))
    return document, biaoti


def transfrom_set(file_paths, taget_path):
    pos_path, neg_path, mid_path = file_paths
    pos_doc, _ = loadDataSet2List(pos_path)
    neg_doc, _ = loadDataSet2List(neg_path)
    mid_doc, _ = loadDataSet2List(mid_path)
    print(len(pos_doc))
    print(len(neg_doc))
    print(len(mid_doc))
    all_doc = pos_doc + neg_doc + mid_doc
    target_object = codecs.open(taget_path, mode='a', encoding='utf-8')
    for pos in pos_doc:
        target_object.write(' '.join(pos)+' ')
        target_object.write("__label__" + str(1) + " ")
        target_object.write('\n')
    for neg in neg_doc:
        target_object.write(' '.join(neg)+' ')
        target_object.write("__label__" + str(0) + " ")
        target_object.write('\n')
    for mid in mid_doc:
        target_object.write(' '.join(mid) + ' ')
        target_object.write("__label__" + str(2) + " ")
        target_object.write('\n')
    target_object.close()


file_paths = ['positive.txt','negative.txt','midum.txt']
target_path = 'data1.txt'
transfrom_set(file_paths, target_path)
# file_path='sample_multiple_label.txt'
# target_file_path='sample_multiple_label3.txt'
# read_split_write(file_path,target_file_path)
