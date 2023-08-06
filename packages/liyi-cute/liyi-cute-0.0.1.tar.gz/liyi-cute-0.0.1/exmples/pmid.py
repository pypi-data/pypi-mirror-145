#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/26 23:25
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : pmid.py
"""
解析pmid json文件内容
{"key":""
"text":"",
"annotations":[{},{}]
}
"""
from typing import List, Dict
from glob import iglob
import json
import os
import logging
from collections import OrderedDict

from tqdm import tqdm

logger = logging.getLogger(__file__)

def parse_pmid_json(path:str)->List:
    """
    :param path:
    :return:
    """
    pmid_files = iglob("{0}/*.json".format(path))
    informations = list()
    for index, file in tqdm(enumerate(pmid_files)):
        text, annotations = load_json(file)
        ## 核对标签文本是否对齐
        if not check_annotations(text, annotations):
            raise ValueError("label misaligned with text position, file path is{}".format(file))
        informations.append({"key":index, "path":file, "text":text, "annotations":annotations})

    return informations



def load_json(input_path):
    """
    :param input_path:
    :return:
    """
    data = json.load(open(input_path, 'r', encoding="utf-8"))
    text = ""
    annotations = []
    for item in data["passages"]:
        if item["text"]:
            text = text + item["text"] + " "
            for anns in item["annotations"]:
                if anns["text"].strip() != "":
                    annotations.append([anns["locations"][0]["offset"],
                                         anns["locations"][0]["offset"]+anns["locations"][0]["length"],
                                         anns["text"],
                                         anns["infons"]["type"]])
    text = text.rstrip()
    return text, annotations

def check_annotations(text:str, annotations:List) -> bool:
    """
    :param text:
    :param annotations:
    :return:
    """
    for an in annotations:
        start_id = an[0]
        end_ids = an[1]
        if text[start_id:end_ids] != an[2]:
            logger.warning("start_ids: " + str(start_id))
            logger.warning("end_ids: " + str(end_ids))
            logger.warning("text content: " + text[start_id:end_ids])
            logger.warning("annotations content: " + an[2])
            return False
    return True

def covert_json_to_ann(informations:Dict)->None:
    """
    :param informations: {"key":index,"text":text, "annotations":annotations}
    :return:None
    """
    if isinstance(informations, dict):
        raise ValueError("the type of annotations is not dict")
    if len(informations) and "key" not in informations[0].keys():
        raise ValueError("'key' not in dict")
    informations = sorted(informations, key=lambda x:x["key"])
    entity_index = 1
    for index, content in tqdm(enumerate(informations)):
        key = content['key']
        text = content['text']
        path = content['path']
        annotations = content['annotations']
        txt_file_w = open(os.path.splitext(path)[0]+".txt", "w", encoding="utf-8")
        ann_file_w = open(os.path.splitext(path)[0]+".ann", "w", encoding="utf-8")
        for ann in annotations:
            e_inx = "T"+str(entity_index)
            e_type = ann[3]
            strat_postion = ann[0]
            end_postion = ann[1]
            word = ann[2]
            ann_file_w.write(e_inx+"\t"+e_type+" "+str(strat_postion)+" "+str(end_postion)+"\t"+word)
            ann_file_w.write("\n")
            entity_index+=1
        txt_file_w.write(text)
        txt_file_w.close()
        ann_file_w.close()
    logger.info("files covert ann format fninsh")

def covert_ann_to_json():
    pass



if __name__ == '__main__':
    info = parse_pmid_json("../../datasets/pmid")
    covert_json_to_ann(info)
    print(1)