#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/27 12:31
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : convert.py
from __future__ import annotations

from typing import Text, Any, List

from liyi_cute.shared.imports.schemas.schema import Example
from liyi_cute.utils.io import write_text_file, examples_as_json


def convert_example_data(
    examples: List[Example], out_file: Text, output_format: Text, **kwargs: Any
) -> None:
    """
    :param examples:
    :param out_file:
    :param output_format:
    :return:
    """

    if not (isinstance(examples, List)):
        raise TypeError("data_file type is not in (Example or Text)")

    if output_format == "json":
        output= examples_as_json(examples, **kwargs)
    else:
        raise ValueError("....")

    write_text_file(file_path=out_file, content=output)







