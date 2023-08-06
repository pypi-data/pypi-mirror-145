#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/4 22:53
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : test4.py
from liyi_cute.shared.imports.schemas.schema import Entity, Example


def _en_serialization (data, tag, mode):
    text = ""
    entities = []
    tag_len = len(tag)
    index = 0
    ids = 1
    while index < tag_len:
        text += data[index] + " "
        if tag[index][0] == "B":
            type = tag[index].split("-")[1]
            start = len(text) - len(data[index])
            mention = data[index] + " "
            while index + 1 < tag_len and tag[index + 1] == "I":
                index += 1
                text += data[index] + " "
                mention += data[index] + " "
            end = len(text)
            entities.append(Entity(id=f"T{str(ids)}", start=start, end=end, mention=mention.rstrip(), type=type))
            ids += 1
    return Example(id=mode, task_name="ner", text=text, entities=entities)

data = []
tag = []
mode ="train"