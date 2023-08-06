#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/2 16:18
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : example_tokenizer.py
from liyi_cute.processor.postprocess import NerPostprocessing
from liyi_cute.processor.preprocess import cut_sent
from liyi_cute.shared.imports.pmid_parser import PmidParser
from liyi_cute.processor.tokenizers.lm_tokenizer import LanguageModelTokenizer
from liyi_cute.shared.imports.schemas.schemaItem import TraningNerExampleSchema

obj = PmidParser(task_name="ner", error="ignore")
examples = obj.parse(r"../data/pmid")
#[{

# }]

cut_examples = cut_sent(examples, max_length=256)
obj = LanguageModelTokenizer.create({
        "pretrained_model_name_or_path": "bert-base-uncased",
        "add_special_tokens": True,
        "max_length": 256,
        "padding":"max_length",
        "return_offsets_mapping":True,
        "task_name":"ner"
    })
t = TraningNerExampleSchema(many=True)
tts = []
pre_tags = []
for c_exp in cut_examples:
    tts.append(obj.tokenize(c_exp))
    pre_tags.append(["O"]*len(c_exp.input_ids))

result = NerPostprocessing(pre_tags, tts)
