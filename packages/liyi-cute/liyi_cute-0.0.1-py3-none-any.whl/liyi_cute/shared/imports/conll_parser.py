#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/4 16:06
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : conll_parser.py
"""
conll 格式转换
Be  O
EU	B-ORG
rejects	O
German	B-MISC
call	O

序列化数据
Text: Be EU rejects German call
entities:[Entity(id = "T1", start=1, end=2, metion="EU"), type="MISC"]
"""

from __future__ import annotations

import os
from typing import Optional, Iterable, Union, Text, List, Tuple

from tqdm import tqdm

from liyi_cute.shared.exceptions import NotImplementedException
from liyi_cute.shared.imports.base_parser import BasePaeser
from liyi_cute.shared.imports.schemas.schema import Entity, Example
from liyi_cute.utils.common import bioes_to_bio, iter_file_groups
from liyi_cute.utils.io import read_file

class ConllParser(BasePaeser):
    exts = {".txt"}

    def __init__(self,task_name, ignore_types: Optional[Iterable[str]] = None, error: str = "raise"):
        super().__init__(task_name,ignore_types, error)

    def _load_data(self, file_path:Text, encoding:Text)-> Tuple[List[list], List[list]]:
        lines = read_file(file_path, encoding)

        line = lines.strip()
        all_data = []
        all_tag = []
        if line:
            lines_list = lines.split("\n\n")
            for line_s in lines_list:
                line_list = line_s.split("\n")
                data = []
                tag = []
                for line in line_list:
                    if not line.strip():
                        continue
                    data.append(line.split("\t")[0])
                    tag.append(line.split("\t")[1])
                # entity_obj = self._serialization_data(data, tag, mode)
                all_data.append(data)
                all_tag.append(tag)
        return all_data, all_tag

    def _parse_txt(self, file_path:Text, encoding:Text="utf-8", mode="train")->List[Example]:
        all_data, all_tag = self._load_data(file_path=file_path, encoding=encoding)
        ## 判断标注类型 BIO BIOES BMSE...
        tag_type = self._tag_type(all_tag)
        if tag_type == "BEIOS":
            new_all_tag = []
            for t in all_tag:
                new_all_tag.append(bioes_to_bio(t))
            all_tag = new_all_tag

        ## 序列化
        examples = []
        for idx in range(len(all_data)):
            examples.append(self._serialization_data(all_data[idx], all_tag[idx], mode))
        return examples


    def _en_serialization(self, data:List, tag:List, mode)->Example:
        text = ""
        entities = []
        tag_len = len(tag)
        index = 0
        ids = 1
        while index<tag_len:
            text = text + data[index] if index==0 else text + " "+ data[index]
            if tag[index][0]=="B":
                type = tag[index].split("-")[1]
                start = len(text) - len(data[index])
                mention = data[index]
                while index+1 <tag_len and tag[index+1][0]=="I":
                    index+=1
                    text += " " + data[index]
                    mention +=  " " + data[index]
                end = len(text)
                entities.append(Entity(id=f"T{str(ids)}", start=start, end=end, mention=mention.rstrip(), type=type))
                ids+=1
                index+=1
            else:
                index += 1
        return Example(id=mode, task_name=self.task_name, text=text, entities=entities)

    def _serialization_data(self, data:List, tag:List, mode:Text)->Example:
        if self.lang=="en":
            return self._en_serialization(data, tag, mode)
        elif self.lang=="ch":
            raise NotImplementedException
        else:
            raise NotImplementedException


    def parse(self, dirname: Union[str, bytes, os.PathLike], encoding: str = "utf-8"):
        examples = []
        file_groups = iter_file_groups(
            dirname,
            self.exts,
            missing="error" if self.error == "raise" else "ignore",
        )
        for key, file_path in tqdm(file_groups):
            examples+=self._parse_txt(file_path[0], encoding=encoding, mode=os.path.split(file_path[0])[1].split(".")[0])

        return examples

