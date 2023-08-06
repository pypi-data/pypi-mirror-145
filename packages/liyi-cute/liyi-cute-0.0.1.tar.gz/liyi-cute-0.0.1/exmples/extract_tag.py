#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/27 18:25
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : extract_tag.py

from spacy.gold import biluo_tags_from_offsets
import spacy
nlp = spacy.load("en_core_web_lg")
import json
from spacy import tokenizer
data_path = "../../datasets/output/test.json"
data = json.loads(open(data_path, "r", encoding='utf-8').read())

for content in data:
    for k in content:
        text = content["text"]
        entities = content["entities"]
        entities = [(en["start"],en["end"],en["type"]) for en in entities]
        doc = nlp(text)
        tags = biluo_tags_from_offsets(doc, entities)
        tokens = [token.text for token in doc]

        assert len(tags) == len(tokens), "not equel"