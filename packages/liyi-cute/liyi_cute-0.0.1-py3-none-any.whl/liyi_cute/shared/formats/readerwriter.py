#!/usr/bin/env python
# -*- coding: utf-8 -*-
# code come from https://github.com/RasaHQ/rasa/blob/rasa/shared/nlu/training_data/formats/readerwriter.py#L49
# @Time    : 2022/3/27 16:24
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : readerwriter.py
from __future__ import annotations

import abc
import json
from typing import Text, List, Any, Union, Dict
from pathlib import Path

from liyi_cute.utils.io import read_file, write_text_file
from liyi_cute.shared.imports.schemas.schema import Example

class ExamplesDataReader(abc.ABC):
    """Reader for NLU training data.
    """

    def __init__(self) -> None:
        """Creates reader instance."""
        self.filename: Text = ""

    def read(self, filename: Union[Text, Path], **kwargs: Any) -> "List[Example]":
        """Reads TrainingData from a file."""
        self.filename = str(filename)
        return self.reads(read_file(filename), **kwargs)

    @abc.abstractmethod
    def reads(self, s: Text, **kwargs: Any) -> "List[Example]":
        """Reads TrainingData from a string."""
        raise NotImplementedError

class ExamplseDataWriter:
    """A class for writing training data to a file."""

    def dump(self, filename: Text, example_data: "Example") -> None:
        """Writes a TrainingData object to a file."""
        s = self.dumps(example_data)
        write_text_file(s, filename)

    def dumps(self, example_data: "Example") -> Text:
        """Turns TrainingData into a string."""
        raise NotImplementedError

class JsonExamplesDataReader(ExamplesDataReader):
    """A class for reading JSON files."""

    def reads(self, s: Text, **kwargs: Any) -> "Example":
        """Transforms string into json object and passes it on."""
        js = json.loads(s)
        return self.read_from_json(js, **kwargs)

    def read_from_json(self, js: Dict[Text, Any], **kwargs: Any) -> "Example":
        """Reads TrainingData from a json object."""
        raise NotImplementedError