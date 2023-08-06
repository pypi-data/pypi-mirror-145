#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/1 23:32
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : example_cut_sent.py
from liyi_cute.processor.preprocess import cut_sent
from liyi_cute.shared.imports.pmid_parser import PmidParser
from liyi_cute.shared.imports.schemas.schemaItem import TraningNerExampleSchema

obj = PmidParser(task_name="ner", error="ignore")
examples = obj.parse(r"../data/pmid")
#[{

# }]
t = TraningNerExampleSchema(many=True)
a = cut_sent(examples, max_length=256)
s = t.dump(a)
ex = t.load(s)
print(ex)