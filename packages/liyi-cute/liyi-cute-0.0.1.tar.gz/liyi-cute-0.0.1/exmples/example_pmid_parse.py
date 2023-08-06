#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/27 13:57
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : example_pmid_parse.py
import json
from liyi_cute.shared.imports.pmid_parser import PmidParser
from liyi_cute.shared.convert import convert_example_data
from liyi_cute.shared.imports.schemas.schemaItem import ExampleSchema

if __name__ == '__main__':
    obj = PmidParser(task_name="ner", error="ignore")
    examples = obj.parse(r"../data/pmid")
    a = obj.entities()
    mutation = list(a['Mutation'])
    gene = list(a["Gene"])
    chemical = list(a["Chemical"])

    with open("../tests/mutation.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(mutation))

    with open("../tests/gene.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(gene))

    with open("../tests/chemical.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(chemical))


    # convert_example_data(examples, output_format="json", out_file=r"../data/output/pmid.json")

    # js = json.load(open("../data/output/pmid.json", "r", encoding='utf-8'))
    # ex = ExampleSchema()
    # print(ex.load(js, many=True))