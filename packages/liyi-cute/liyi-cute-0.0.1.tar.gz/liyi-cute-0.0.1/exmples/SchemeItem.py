# -*- coding:UTF-8 -*-

# author:user
# contact: test@test.com
# datetime:2022/3/28 13:56
# software: PyCharm

"""
文件说明：
    序列化与反序列化
"""
from typing import Dict
# from pprint import pprint
# from liyi_cute.shared.imports.schemas.data_schema import Entity, EntitySchema
# en = Entity(mention="ssss", start=1, end=1, id="T1", type="gene")
# schema = EntitySchema()
# result = schema.dump(en)
# ## 序列化
# print(result)
# pprint(type(result))
# pprint(type(schema.dumps(en)))
#
# ## 过滤输出
# summary_schema = EntitySchema(only=("mention", "start"))
# rs = summary_schema.dump(en)
# pprint(rs)
#
# ## 反序列化
# res = schema.load(result)
# print(res)

## 对象之间的序列化与反序列话
# from liyi_cute.shared.imports.bart_parser import BratParser
# from liyi_cute.shared.imports.schemas.data_schema import ExampleSchema
# brat = BratParser(error="ignore")
# examples = brat.parse("../data/bio/")
# example_schema = ExampleSchema()
# exs = []
# # 序列化
# for ex in examples:
#     result = example_schema.dump(ex)
#     exs.append(result)
#
# ## 反序列化
# sez = []
# for ex in exs:
#     res = example_schema.load(ex)
#     sez.append(res)


## 从json文件中加载，然后反序列话
import json

from liyi_cute.shared.exceptions import NotContainException
from liyi_cute.shared.imports.schemas.data_schema import Example, Entity, Relation, Reference, Event

js = json.load(open("../data/output/test.json", 'r', encoding="utf-8"))
# a = JSONSerializer.deserialize(Example, js[0])

all_entity_dict = []
for example in js:
    text = example.get("text", "")
    if not text:
        continue
    entities = example.get("entities", [])
    ## 实体初始化

    entity_dict = {}
    for ent  in entities:
        if not ent.get("id"):
            raise ValueError
        references = ent.pop("references")
        references_list = [Reference(**data) for data in references ]
        entity_obj = Entity(references=references_list, **ent)

        entity_dict[ent.get("id")] = entity_obj
    all_entity_dict.append(entity_dict)

tasks = ["ner", "rel", "eve", "attr"] # 1)entity extraction 2)relation extraction 3)event extraction 4)attribute extraction
task_name = "ner"
if task_name not in tasks:
    raise NotContainException

for index, example in enumerate(js):
    text  = example.get("text", "")
    if not text:
        continue

    entitie_dict = all_entity_dict[index]
    relations = example.get("relations", [])
    events = example.get("events", [])
    id = example.get("id", None)





    # ## 关系初始化
    # relations = example.get("relations", [])
    # relation_list = []
    # for rel in relations:
    #     arg1 = rel.pop("arg1")
    #     arg1_references = arg1.pop("references")
    #     arg1_references_list = [Reference(**data) for data in arg1_references]
    #     arg1_obj = Entity(references = arg1_references_list, **arg1)
    #
    #     arg2 = rel.pop("arg2")
    #     arg2_references_list = arg2.pop("references")
    #     arg2_obj = Entity( references=arg2_references_list, **arg2)
    #
    #     rel_obj = Relation(arg1=arg1_obj, arg2=arg2_obj, **rel)
    #
    #     relation_list.append(rel_obj)
    #
    # ## 事件初始化
    # events = example.get("events", [])
    #
    # for env in events:
    #     trigger = env.pop("trigger")
    #     tri_references = trigger.pop("references")
    #     tri_reference_obj = [Reference(**data) for data in tri_references]
    #     trigger_obj = Entity(references=tri_reference_obj, **trigger)
    #
    #     argument_list = []
    #     arguments = env.pop("arguments")
    #     for arg_content in arguments:
    #         arg_content_references = arg_content.pop("references", [])
    #         arg_reference_obj = [Reference(**data) for data in arg_content_references]
    #         argument_list.append(Entity(references=arg_reference_obj, **arg_content))
    #
    #     event_obj = Event(trigger=trigger_obj, arguments=argument_list, **env)




def arguments_dfs(env:Dict):
    arguments = env.pop("arguments")
    if "arguments" in env:
        arguments_dfs(env)

    argument_list = []
    arguments = env.pop("arguments")
    for arg_content in arguments:
        arg_content_references = arg_content.pop("references", [])
        arg_reference_obj = [Reference(**data) for data in arg_content_references]
        argument_list.append(Entity(references=arg_reference_obj, **arg_content))

