#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/27 13:08
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : base_parser.py
from __future__ import annotations

import pickle
from typing import Optional, Text, Union, Dict, List
from collections import Iterable
import re, os, logging
from copy import deepcopy

from liyi_cute.shared.exceptions import NotImplementedException, NotExistException, FileNotFoundException, \
    NotSupportedException
from liyi_cute.shared.imports.schemas.schema import Example


class BasePaeser(object):
    exts = {".ann", ".txt", ".json"}
    support_task_name = {"ner", "rel" "env", "attr"}
    types = {"T", "R", "*", "E", "N", "AM"}
    supported_language_list = ["en", "zh"]
    support_save = {".pkl", ".json", "txt", "yml", "txt"}
    errors = {"raise", "ignore"}
    def __init__(self, task_name, ignore_types: Optional[Iterable[str]] = None, error: str = "raise", lang="en"):
        self.examples:List = []
        ##任务类型
        if task_name not in self.support_task_name:
            raise NotImplementedException("The task interface is not implemented")
        self.task_name = task_name

        ## 判断忽略的类型
        self.re_ignore_types: Optional[re.Pattern] = None
        if ignore_types:
            unknown_types = set(ignore_types) - self.types
            if unknown_types:
                raise NotExistException(f"Unknown types: {unknown_types!r}")
            ## 忽略类型正则
            self.re_ignore_types = re.compile(r"|".join(re.escape(x) for x in ignore_types))

        ##
        if error not in self.errors:
            raise NotExistException(f"`error` should be in {self.errors!r}")
        self.error = error

        ## 支持语言
        if lang not in self.supported_language_list:
            raise NotExistException(f"{lang} is not support")
        self.lang = lang

    def _should_ignore_line(self, line:Text):
        if self.re_ignore_types:
            return re.match(self.re_ignore_types, line)

        return False

    def _raise(self, error)->None:
        if self.error == "raise":
            raise error

    def _raise_invalid_line_error(self, line:Text)->None:
        self._raise(NotExistException(f"Invalid line: {line}"))


    def save_example(self, examples: List[Example], output: Text) -> None:
        file_ext = os.path.splitext(output)[1]
        if not os.path.exists(os.path.dirname(output)):
            raise FileNotFoundException(f"{os.path.dirname(output)}:path not exits")

        if file_ext not in self.support_save:
            raise NotSupportedException

        with open(output, "wb") as f:
            pickle.dump(examples, f)

    def load_example(self, input: Text) -> List[Example]:
        with open(input, "rb") as f:
            examples = pickle.load(f)

        return examples

    def parse(self,  dirname: Union[str, bytes, os.PathLike], encoding: str = "utf-8"):
        raise NotImplementedError

    @staticmethod
    def filter_sample(examples, keep_content:List, filter_type="ner"):
        if not isinstance(keep_content, List):
            raise ValueError

        if filter_type=="ner":
            new_examples = deepcopy(examples)
            for example in new_examples:
                entities = []
                for ent in example.entities:
                    if ent.type in keep_content:
                        entities.append(ent)
                example.entities = entities
            return new_examples

    def entities(self):
        entities_set = self.entity_type()
        entities = {key:set() for key in entities_set}

        for example in self.examples:
            for ent in example.entities:
                entities[ent.type].add(ent.mention)
        return entities

    def _tag_type(self, all_tag:List[List]):
        if not (isinstance(all_tag, list) and isinstance(all_tag[0], list)):
            raise ValueError
        tag_type = "".join(sorted(list(set([tag.split("-")[0] for tags in all_tag for tag in tags]))))
        if tag_type == "BIO":
            return "BIO"
        elif tag_type == "BEIOS":
            return "BEIOS"
        else:
            raise NotImplementedError

    def entity_type(self):
        entities_set = set()
        for example in self.examples:
            for ent in example.entities:
                entities_set.add(ent.type)
        return entities_set

    def relations(self):
        raise NotImplementedError

    def relation_type(self):
        raise NotImplementedError

    @classmethod
    def create(cls, **kwargs):
        task_name = kwargs.pop("task_name", None)
        ignore_types = kwargs.pop("ignore_types", None)
        error = kwargs.pop("error", "raise")

        return cls(task_name=task_name,
                   ignore_types=ignore_types,
                   error=error)






