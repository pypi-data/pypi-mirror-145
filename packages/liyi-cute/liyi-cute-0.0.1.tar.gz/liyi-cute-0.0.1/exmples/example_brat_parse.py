#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/29 18:40
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : example_brat_parse.py.py
from liyi_cute.shared.exceptions import NotImplementedException
from liyi_cute.shared.imports.bart_parser import BratParser
from liyi_cute.shared.convert import convert_example_data
# Initialize a parser.
brat = BratParser(task_name="rel", error="ignore")
examples = brat.parse("../data/bio/")
convert_example_data(examples, output_format="json", out_file=r"../data/output/test.json")