#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/2 12:20
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : lm_tokenizer.py
from __future__ import annotations

from typing import Optional, Dict, Text, Any, List

from transformers import AutoTokenizer

from liyi_cute.processor.tokenizers.tokenizer import Tokenizer
from liyi_cute.shared.exceptions import ParamNotExistException
from liyi_cute.shared.imports.schemas.schema import TraningExample


class LanguageModelTokenizer(Tokenizer):
    defaults = {
        "pretrained_model_name_or_path": "bert-base-uncased",
        "add_special_tokens": True,
        "max_length": 512,
        "padding":"max_length",
        "return_offsets_mapping":True
    }
    keep_keys = ["input_ids", "token_type_ids", "attention_mask", "offset_mapping","sequence_ids"]

    def __init__(self, component_config: Optional[Dict[Text, Any]]):
        super().__init__(component_config)
        self.task_name = self.component_config.get("task_name", None)
        if self.task_name is None:
            raise ParamNotExistException("miss parameter task_name")

        self.tokenizer = AutoTokenizer.from_pretrained(self.component_config.get("pretrained_model_name_or_path"))

    def tokenize(self, train_example: Optional[TraningExample]):
        encoded = self.process(text=train_example.cut_text)
        alignment_tags = self.label_alignment(encoded, train_example.cut_entities)
        train_example.true_ner_tag = alignment_tags

        for key in self.keep_keys:
            setattr(train_example, key, encoded[key])

        return train_example

    def process(self, text:Text)->Dict:
        ## key ['input_ids', 'token_type_ids', 'attention_mask', 'offset_mapping']
        encoded = self.tokenizer(text,
                                add_special_tokens=self.component_config.get("add_special_tokens"),
                                max_length=self.component_config.get("max_length"),
                                padding=self.component_config.get("padding"),
                                return_offsets_mapping=self.component_config.get("return_offsets_mapping"))

        keep_encoded = {key: encoded[key] for key in encoded}
        if "sequence_ids" in self.keep_keys:
            keep_encoded["sequence_ids"] = encoded.sequence_ids()
        return keep_encoded
