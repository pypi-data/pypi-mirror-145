#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/27 10:49
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : pmid_parser.py
from __future__ import annotations
from typing import Union, List, Optional, Dict, Text
from collections import Iterable
import os, json, re
import logging

from tqdm import tqdm

from .base_parser import BasePaeser
from .schemas.schema import Example, Entity
from liyi_cute.utils.common import iter_file_groups
logger = logging.getLogger(__file__)

class PmidParser(BasePaeser):
    exts = {".json"}
    support_save = {".pkl", ".json" }
    support_task_name = {"ner"} #  "ner", "rel" "env", "attr"
    types = {"T"}
    def __init__(self, task_name, ignore_types: Optional[Iterable[str]] = None, error: str = "raise"):
        super().__init__(task_name,ignore_types, error)

    def _parse_json(self, input_path:str, encoding:str, key)->Example:
        entities, relations, events = [], [], []

        js_data = json.load(open(input_path, 'r', encoding="utf-8"))
        text = ""
        annotations = []
        for item in js_data["passages"]:
            if item["text"]:
                text = text + item["text"] + " "
                for anns in item["annotations"]:
                    if anns["text"].strip() != "":
                        annotations.append([anns["locations"][0]["offset"],
                                            anns["locations"][0]["offset"] + anns["locations"][0]["length"],
                                            anns["text"],
                                            anns["infons"]["type"]])
        text = text.rstrip()

        ## check annotations
        annotations = self.check_annotations(text, annotations)

        # Format entities.
        entities = self._format_entities(annotations)
        self._check_entities(entities.values())

        example = Example(text=text,
                          task_name=self.task_name,
                          entities=list(entities.values()),
                          relations=relations,
                          events=events,
                          id=key)
        return example

    def _check_entities(self, entities):  # pylint: disable=no-self-use
        pool = {}
        for entity in entities:
            id_ = pool.setdefault((entity.start, entity.end), entity.id)
            if id_ != entity.id:
                self._raise(
                    RuntimeError(
                        "Detected identical span for"
                        f" different entities: [{id_}, {entity.id}]"
                    )
                )

    def _format_entities(
            self, annotations
    )->Dict:
        entities = {}
        num_entities = 0
        for ann in annotations:
            entities.update({
                "T" + str(num_entities+1):Entity(
                    mention=ann[2],
                    type=ann[3],
                    start=ann[0],
                    end=ann[1],
                    id = "T" + str(num_entities+1)
                )
            })
            num_entities = num_entities+1
        return entities


    @staticmethod
    def check_annotations(text: str, annotations: List) -> List:
        """
        :param text:
        :param annotations:
        :return:
        """
        for an in annotations:
            start_id = an[0]
            end_ids = an[1]
            if text[start_id:end_ids] != an[2]:
                logger.warning("text: " + text)
                logger.warning("start_ids: " + str(start_id))
                logger.warning("end_ids: " + str(end_ids))
                logger.warning("text label: " + text[start_id:end_ids])
                logger.warning("annotations content: " + an[2])
                an[2] = text[start_id:end_ids]

        return annotations

    def parse(self,  dirname: Union[str, bytes, os.PathLike], encoding: str = "utf-8")->List[Example]:
        examples = []
        file_groups = iter_file_groups(
            dirname,
            self.exts,
            missing="error" if self.error == "raise" else "ignore",
        )
        for key, json_file in tqdm(file_groups):
            example = self._parse_json(json_file[0], encoding=encoding, key=key)
            examples += [example]

        examples.sort(key=lambda x: x.id if x.id is not None else "")
        self.examples = examples

        return self.examples




