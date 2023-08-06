# -*- coding:UTF-8 -*-

# author:user
# contact: test@test.com
# datetime:2022/4/1 17:03
# software: PyCharm

"""
文件说明：
    
"""
from __future__ import annotations

from typing import Tuple, List, Dict, Text
import logging

from tqdm import tqdm

from liyi_cute.shared.imports.schemas.schema import Example, Entity, TraningNerExample, TraningExample

logger = logging.getLogger(__file__)

def cut_sentences_v1(sent_tupe:Tuple,  punctuation_special_char={".", ";"})->List[Tuple]:
    """
    [(0, "1111"), (65, "222")], tupe第一位是原文的开始位置，第二位是原文截断后的位置
    """
    init_start = sent_tupe[0]
    sent = sent_tupe[1]
    sents = []
    string = ""
    start = 0
    for index, char in enumerate(sent):
        if char==" " and index-1>0 and (sent[index-1] in punctuation_special_char):
            string +=sent[index]
            sents.append((init_start+start, string))
            string = ""
            start = index+1
        else:
            string += sent[index]
    if string:
        sents.append((init_start+start, string))
    return sents

def cut_sentences_v2(sent_tupes:List[Tuple], entities:Entity)->List[Tuple]:
    new_sent_tupes = []
    for sent_tupe in sent_tupes:
        init_start = sent_tupe[0]
        c_text = sent_tupe[1]
        mid = len(c_text)//2
        entities = sorted(entities, key=lambda x: x.start)
        while True:
            flag = False
            for ent in entities:
                if ent.start<=mid <ent.end:
                    flag = True

            if not flag or mid>=len(c_text):
                break
            mid +=1
        new_sent_tupes+=[(init_start, c_text[:mid]),(init_start+mid, c_text[mid:])]
    return new_sent_tupes

def correct_tag_position(all_cut_sents:List[Tuple], annotaion:List[Entity])->List[Dict]:
    """
    [Entity(start=0, end=4, mention="KRAS", type="GENE", id="T1"),...]
    return [{'id': 0, 'text': 'KRAS G12V mutation', 'entities': [[0, 4, 'KRAS', 'GENE'], [5, 9, 'G12V', 'DESEASE']]}]
    """
    all_data = []
    sent_ids = 0
    for c_s in all_cut_sents:
        cut_text = c_s[1]
        cut_start = c_s[0]
        cut_end = cut_start + len(cut_text)
        entities = []
        for an in annotaion:
            e_start = an.start
            e_end = an.end
            if cut_start <=e_start< cut_end and cut_start <=e_end< cut_end:
                entities.append([e_start-cut_start, e_end-cut_start, an.mention, an.type])
        all_data.append({"id":sent_ids, "text":cut_text, "entities":entities})
        sent_ids += 1
    return all_data

def cut_sent(examples:List[Example], max_length:int=512)->List[TraningExample]:
    # 将句子分句，细粒度分句后再重新合并
    """

    :param examples:
    :param max_length:
    :return: [{"text":"", "entities":[(0,4,"KRAS", "GENE"), (5,9,"G12V", "DESEASE")], "cut_text":[{'id': 0, 'text': 'KRAS G12V mutation', 'entities': [[0, 4, 'KRAS', 'GENE'], [5, 9, 'G12V', 'DESEASE']]}]}]
    """
    sentences = []

    ## 以句号为分割符号
    tq_bar = tqdm(examples, desc="cut example sentence")
    train_samples = []
    for index, example in enumerate(tq_bar):
        tq_bar.set_description("example number: %s" %index)
        if example.task_name=="ner":
            text = example.text
            entities = example.entities # [Entity()]
            cut_sents_list = [(0, text)]
            ## 一阶截断
            if is_ge_max_len(cut_sents_list, max_length):
                cut_sents_list = cut_sentences_v1((0, example.text), punctuation_special_char={"."}) #[(0, "1111"), (65, "222")]
            ## 二阶截断
            if is_ge_max_len(cut_sents_list, max_length):
                two_cut_sents_list = cut_sents_list
                cut_sents_list = []
                for cut_sent in two_cut_sents_list:
                    if len(cut_sent[1])>max_length:
                        cut_sents_list+=cut_sentences_v2([cut_sent], entities)
                    else:
                        cut_sents_list+=[cut_sent]

            ## 截断后纠正标签的起始和结束的位置
            correct_cut_sents_list = correct_tag_position(cut_sents_list, entities) # [{'id': 0, 'text': 'KRAS G12V mutation', 'entities': [[0, 4, 'KRAS', 'GENE'], [5, 9, 'G12V', 'DESEASE']]}]

            ## 校验标签是否对齐
            check_ner_postion(correct_cut_sents_list)
            for idx, ccsl in enumerate(correct_cut_sents_list):
                train_samples.append(TraningNerExample(id=example.id,
                                                       task_name=example.task_name,
                                                       text=text,
                                                       entities= example.entities,
                                                       sub_id=idx,
                                                       cut_text=ccsl['text'],
                                                       cut_entities=[Entity(id=str(index), start=cu_ent[0],
                                                                            end=cu_ent[1], mention=cu_ent[2],
                                                                            type=cu_ent[3])
                                                                     for index, cu_ent in enumerate(ccsl['entities'])],
                                                       cut_number=len(correct_cut_sents_list),
                                                       cut_len=len(ccsl['text']))
                                     )
        else:
            raise NotImplementedError

    return train_samples

def is_ge_max_len(sents_list:List[Tuple], max_len:int)->bool:
    for cut_sent in sents_list:
        if len(cut_sent[1])>max_len:
            return True
    return False


def check_ner_postion(correct_cut_sent_list:List[Dict])->None:
    """
    [{'id': 0, 'text': 'KRAS G12V mutation', 'entities': [[0, 4, 'KRAS', 'GENE'], [5, 9, 'G12V', 'DESEASE']]}]
    :param correct_cut_sent_list:
    :return:
    """
    for one_cut_sent in correct_cut_sent_list:
        cut_text = one_cut_sent["text"]
        for ent in one_cut_sent['entities']:
            mention = ent[2]
            cut_start = ent[0]
            cut_end =  ent[1]
            if cut_text[cut_start:cut_end]!=mention:
                logger.warning("entity is not aligned")
                logger.warning("cut_text:%s" % cut_text)
                logger.warning("cut_start:%s" %cut_start)
                logger.warning("cut_end:%s" % cut_end)
                logger.warning("mention:%s" % mention)
                logger.warning("cut tag:%s" % cut_text[cut_start:cut_end])
                raise ValueError

