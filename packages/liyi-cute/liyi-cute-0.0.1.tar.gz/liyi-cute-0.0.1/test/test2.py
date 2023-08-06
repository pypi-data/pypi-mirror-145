#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/4 16:41
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : test2.py
import os

file_name = "test.txt"
root_path = "../data/conll/"

all_data = []
data = []
all_tag = []
tag = []
with open(os.path.join(root_path, file_name), 'r', encoding="utf-8") as fr:
    lines = fr.readlines()
    for line in lines:
        line = line.strip()
        if line:
            line_list = line.split(" ")
            if len(line_list)==4:
                data.append(line_list[0])
                tag.append(line_list[3])
        else:
            all_data.append(data)
            all_tag.append(tag)
            data = []
            tag = []

with open(os.path.join(root_path, "test.txt"), "w", encoding="utf-8") as fw:
    for d, t in list(zip(all_data, all_tag)):
        for k in list(zip(d, t)):
            fw.write("\t".join(k))
            fw.write("\n")
        fw.write("\n")

