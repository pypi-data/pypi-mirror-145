#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/2 10:06
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : postprocess.py
from __future__ import annotations

from typing import Dict, List, Tuple, Union, Text

from tqdm import tqdm

from liyi_cute.shared.imports.schemas.schema import TraningExample, TraningNerExample

"""
输出内容
pre_ner_tag = []

"""

def NerPostprocessing(pre_neg_tags:List[List],
                      train_samples:List[TraningNerExample])-> Tuple[List, List[List], List[List]]:

    id = ""
    test_texts = []
    text_pre_tags = []
    offset_mappings = []

    offset_mapping = []
    text_string = ""
    pre_tag = []
    for index, example in enumerate(train_samples):
        if index==0:
            text = example.text
            id = example.id
            text_string+=example.cut_text
            pre_tag+= pre_neg_tags[index]
            offset_mapping += example.offset_mapping
        elif id==example.id:
            text = example.text
            id=example.id
            text_string += example.cut_text
            pre_tag += pre_neg_tags[index]
            offset_mapping += example.offset_mapping
        else:
            assert len(text)==len(text_string), "句子长度不相等"
            test_texts.append(text_pre_tags)
            offset_mappings.append(offset_mapping)
            text_pre_tags.append(pre_tag)
            ## 不相等的重新初始化数据
            id = example.id
            text = example.text
            text_string = example.cut_text
            pre_tag = pre_neg_tags[index]
            offset_mapping = example.offset_mapping

    if text_string:
        test_texts.append(text_pre_tags)
        offset_mappings.append(offset_mapping)
        text_pre_tags.append(pre_tag)

    return test_texts, offset_mappings, text_pre_tags

def postion_to_string(pre_tags, entitie, offset_mapping:List[Tuple], text, ids)->Dict:
    tag_type = pre_tags[entitie[0]].split("-")[1]
    start = offset_mapping[entitie[0]][0]
    end = offset_mapping[entitie[-1]][1]
    return {"id": "T"+str(ids), "mention":text[start:end], "start":start, "end":end, "type":tag_type}

def entity_to_json_v1(pre_tags, offset_mapping, text):
    entities = []
    entitie = []
    ids = 1
    for index, tag in enumerate(pre_tags):
        if tag[0]=="B" and len(entitie)==0:
            entitie.append(index)
        elif tag[0]=="B" and len(entitie)!=0:
            entities.append(postion_to_string(pre_tags, entitie, offset_mapping, text, ids))
            ids += 1
            entitie = [index]
        elif tag[0]=="I":
            entitie.append(index)
        else:
            if entitie:
                entities.append(postion_to_string(pre_tags, entitie, offset_mapping, text, ids))
                ids += 1
            entitie = []

    return {"text": text, "entities": entities}

def result_to_json_v2(strings, tags):
    """
    :param strings:
    :param tags:
    :return:
    """
    item = {"string":strings, "entities":[]}

    entity_name = ""
    entity_start = 0
    idx = 0

    for word, tag in zip(strings, tags):
        print(word, tag)
        if tag[0] == "S":
            item['entities'].append({"word":word, "start":idx+1, "type":tag[2:]})
        elif tag[0] == "B":
            entity_name = entity_name + word
            entity_start = idx
        elif tag[0] == "I":
            entity_name = entity_name + word
        elif tag[0] == "E":
            entity_name = entity_name + word
            item['entities'].append({"mention":entity_name, "start":entity_start, "end":idx+1, "type":tag[2:]})
        else:
            entity_name=""
            entity_start = idx
        idx = idx + 1
    return item