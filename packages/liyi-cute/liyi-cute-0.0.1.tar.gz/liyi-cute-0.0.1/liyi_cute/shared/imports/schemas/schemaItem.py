# -*- coding:UTF-8 -*-

# author:user
# contact: test@test.com
# datetime:2022/3/29 14:21
# software: PyCharm

"""
文件说明：
    
"""
from marshmallow import Schema, fields, post_load

from .schema import Entity, Relation, Event, Example, TraningNerExample, TraningExample


class EntitySchema(Schema):
    mention = fields.Str()
    type = fields.Str()
    start = fields.Int()
    end = fields.Int()
    id = fields.Str(default=None)

    @post_load
    def make_entity(self, data, **kwargs):
        return Entity(**data)


class RelationSchema(Schema):
    type = fields.Str()
    arg1 = fields.Nested(EntitySchema())
    arg2 = fields.Nested(EntitySchema())
    id = fields.Str(default=None)

    @post_load
    def make_relation(self, data, **kwargs):
        return Relation(**data)


class EventSchema(Schema):
    id = fields.Str(default=None)

    @post_load
    def make_event(self, data, **kwargs):
        return Event(**data)

class ExampleSchema(Schema):
    text = fields.Str()
    entities = fields.List(fields.Nested(EntitySchema()))
    relations = fields.List(fields.Nested(RelationSchema()))
    events = fields.List(fields.Nested(EventSchema()))
    id = fields.Str(default=None)
    task_name = fields.Str(default=None)

    @post_load
    def make_example(self, data, **kwargs):
        return Example(**data)


"""
######################## 处理文本 ######################
"""

class TraningExampleSchema(Schema):
    text = fields.Str()
    cut_text = fields.Str()
    sub_id = fields.Integer()
    cut_number = fields.Integer(default=0)
    entities = fields.List(fields.Nested(EntitySchema()))
    cut_entities = fields.List(fields.Nested(EntitySchema()))
    cut_len = fields.Integer(default=0)
    id = fields.Str(default=None)
    task_name = fields.Str(default=None)
    input_ids = fields.List(fields.Integer())
    attention_mask = fields.List(fields.Integer(), default=list())
    token_type_ids  = fields.List(fields.Integer(), default=list())


class TraningNerExampleSchema(TraningExampleSchema):
    true_ner_tag = fields.List(fields.Str(), default=list())
    pre_ner_tag = fields.List(fields.Str(), default=list())
    offset_mapping = fields.List(fields.Tuple((fields.Integer(), fields.Integer())), default=list())

    @post_load
    def make_train_ner_example(self, data, **kwargs):
        return TraningNerExample(**data)

