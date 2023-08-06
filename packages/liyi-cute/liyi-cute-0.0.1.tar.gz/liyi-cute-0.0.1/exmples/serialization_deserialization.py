# -*- coding:UTF-8 -*-

# author:user
# contact: test@test.com
# datetime:2022/3/28 13:56
# software: PyCharm

"""
文件说明：
    序列化与反序列化
"""
from liyi_cute.shared.imports.schemas.schemaItem import ExampleSchema

# 对象之间的序列化与反序列话
from liyi_cute.shared.imports.bart_parser import BratParser
brat = BratParser(task_name="rel", error="ignore")
examples = brat.parse("../data/bio/")
example_schema = ExampleSchema() # 也可以加入过滤参数 only=("mention", "start")

## 序列化
exs = example_schema.dump(examples, many=True)

## 反序列化
sez = example_schema.load(exs, many=True)


## 加载json 序列化
import json
js = json.load(open("../data/output/test.json", 'r', encoding="utf-8"))
se1 = example_schema.load(js, many=True)


