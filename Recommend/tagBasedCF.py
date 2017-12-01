#-*-coding:utf-8-*-
import pdb

user_tags = dict()
user_items = dict()
tag_items = dict()
item_tags = dict()

def addValueToMat(mat, key, value):
    if key not in mat:
        mat[key] = dict()
        mat[key][value] = 1
    else:
        if value not in mat[key]:
            mat[key][value] = 1
        else:
            mat[key][value] += 1

def InitStat():
    data_file = open('tagdata.txt')
    line = data_file.readline()
    while line:
        terms = line.split("\t")
        user = terms[0]
        item = terms[1]
        tag = terms[2]
        
        addValueToMat(user_tags, user, tag)
        addValueToMat(user_items, user, item)
        addValueToMat(tag_items, tag, item)
        addValueToMat(item_tags, item, tag)
        
        line = data_file.readline()
    pdb.set_trace()
    data_file.close()

InitStat()
