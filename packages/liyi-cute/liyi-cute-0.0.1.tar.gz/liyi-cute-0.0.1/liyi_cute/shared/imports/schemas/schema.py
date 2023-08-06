# -*- coding:UTF-8 -*-

# author:user
# contact: test@test.com
# datetime:2022/3/29 12:31
# software: PyCharm

"""
文件说明：
    
"""
from __future__ import annotations

from typing import Optional, Union, Text, List, Dict, Tuple
from collections.abc import Iterable
import dataclasses

"""
#################################### 加载文件中间数据 ##################################
"""
@dataclasses.dataclass
class Entity(object):
    mention: str
    type: str
    start: int
    end: int
    id: Optional[str] = None

@dataclasses.dataclass
class Relation(object):
    type: str
    arg1: Entity
    arg2: Entity
    id: Optional[str] = None

@dataclasses.dataclass
class Event(object):
    id: Optional[str] = None

@dataclasses.dataclass
class Example(object):
    text: Union[str, Iterable[str]]
    entities: list[Entity] = dataclasses.field(default_factory=list)
    relations: list[Relation] = dataclasses.field(default_factory=list)
    events: list[Event] = dataclasses.field(default_factory=list)
    id: Optional[str] = None
    task_name:Optional[str] = None

"""
############################### 预处理中间数据 ################################
"""
# {'sub_id': 0, 'cut_text': 'KRAS G12V mutation',
# 'cut_entities': [[0, 4, 'KRAS', 'GENE']]}]}

@dataclasses.dataclass
class TraningExample(object):
    text:Text
    cut_text: Text
    sub_id: int
    cut_number: int = dataclasses.field(default_factory=0)
    entities:List[Entity] = dataclasses.field(default_factory=list)
    cut_entities:List[Entity] = dataclasses.field(default_factory=list)
    cut_len: int = dataclasses.field(default_factory=0)
    id: Optional[str] = None
    task_name:Optional[str] = None
    input_ids: List[int] = dataclasses.field(default_factory=list)
    attention_mask: List[int] = dataclasses.field(default_factory=list)
    token_type_ids: List[int] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class TraningNerExample(TraningExample):
    true_ner_tag: List[str] = dataclasses.field(default_factory=list)
    pre_ner_tag: List[str] = dataclasses.field(default_factory=list)
    offset_mapping:List[Tuple] = dataclasses.field(default_factory=list)

"""
###################################### 可视化 #################################
"""
@dataclasses.dataclass
class VisEnt(object):
    start:int
    end:int
    label:Text

@dataclasses.dataclass
class VisEntExample(object):
    text: Text
    ents: List[VisEnt] = dataclasses.field(default_factory=list)
    title:str = None

@dataclasses.dataclass
class VisDepWord(object):
    text:str
    tag:str

@dataclasses.dataclass
class VisDepArc(object):
    start:int
    end:int
    label:str
    dir:str

@dataclasses.dataclass
class VisDepExample(object):
    words:List[VisDepWord] = dataclasses.field(default_factory=list)
    arcs:List[VisDepArc] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class VisExample(object):
    visent:VisEntExample
    visdep:VisDepExample
    id: str = None




