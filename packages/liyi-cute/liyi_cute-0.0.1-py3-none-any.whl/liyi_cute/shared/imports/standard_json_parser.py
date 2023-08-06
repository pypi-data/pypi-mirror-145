#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/4 15:18
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : standard_json_parser.py
from __future__ import annotations

import os
from typing import Optional, Iterable, Union

from liyi_cute.shared.imports.base_parser import BasePaeser


class StandardJsonPaeser(BasePaeser):
    def __init__(self,task_name, ignore_types: Optional[Iterable[str]] = None, error: str = "raise"):
        super().__init__(task_name,ignore_types, error)


    def parse(self, dirname: Union[str, bytes, os.PathLike], encoding: str = "utf-8", lang="en"):
        pass
