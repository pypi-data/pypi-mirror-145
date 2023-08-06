#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/2 10:05
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : tokenizer.py
from __future__ import annotations

from typing import Optional, Dict, Any, Text, List

from liyi_cute.processor.component import Component
from liyi_cute.shared.imports.schemas.schema import Entity


class Tokenizer(Component):
    # {"input_ids":[], "token_type_ids":[], "attention_mask":[], "offset_mapping":[]}
    keep_keys = ["input_ids", "token_type_ids", "attention_mask", "offset_mapping"]
    def __init__(self,component_config: Optional[Dict[Text, Any]] = None):
        super().__init__(component_config)
        self.component_config = component_config

    def tokenize(self, text):

        raise NotImplementedError

    def label_alignment(self, encoded:Dict, annotaion:List[Entity], start_position_id=0, end_postion_id=0) -> List[Text]:
        offset_mapping = encoded['offset_mapping']
        squence_ids = encoded['sequence_ids']
        label = ["O"] * len(offset_mapping)
        for label_ids, loc in enumerate(annotaion):
            start_char = int(loc.start)
            end_char = int(loc.end)
            label_text = loc.mention
            tag_text = loc.type

            # token start index
            token_start_index = 0
            while squence_ids[token_start_index] != start_position_id:
                token_start_index += 1
            # token end index
            token_end_index = len(offset_mapping) - 1
            while squence_ids[token_end_index] != end_postion_id:
                token_end_index -= 1

            while token_start_index < len(offset_mapping) and offset_mapping[token_start_index][0] <= start_char:
                token_start_index += 1
            token_start_index -= 1

            while offset_mapping[token_end_index][1] >= end_char:
                token_end_index -= 1
            token_end_index += 1
            label[token_start_index] = "B-" + tag_text
            for idt in range(token_start_index + 1, token_end_index + 1):
                label[idt] = "I-" + tag_text
        return label


