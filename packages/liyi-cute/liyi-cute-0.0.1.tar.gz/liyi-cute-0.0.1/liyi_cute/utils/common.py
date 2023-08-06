#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/27 14:56
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : common.py

from __future__ import annotations

import copy
import glob
import itertools
import os
import logging

from collections.abc import Iterable
from typing import Union, Optional, Dict, Text, Any, List


def iter_file_groups(
    dirname: Union[str, bytes, os.PathLike],
    exts: Union[str, Iterable[str]],
    missing: str = "error",
) -> Iterable[tuple[str, list[str]]]:
    def _format_ext(ext):
        return f'.{ext.lstrip(".")}'

    def _iter_files(dirname):
        for dirpath, _, filenames in os.walk(dirname):
            for filename in filenames:
                if os.path.splitext(filename)[1] in exts:
                    yield os.path.join(dirpath, filename)

    if isinstance(dirname, bytes):
        dirname = dirname.decode()  # type: ignore

    missings = {"error", "ignore"}
    if missing not in missings:
        raise ValueError(f"Param `missing` should be in {missings}")

    if isinstance(exts, str):
        return glob.iglob(
            os.path.join(dirname, f"**/*{_format_ext(exts)}"), recursive=True
        )

    exts = {*map(_format_ext, exts)}
    num_exts = len(exts)
    files = _iter_files(dirname)
    for key, group in itertools.groupby(
        sorted(files), key=lambda x: os.path.splitext(os.path.relpath(x, dirname))[0]
    ):
        sorted_group = sorted(group, key=lambda x: os.path.splitext(x)[1])
        if len(sorted_group) != num_exts and missing == "error":
            raise RuntimeError(f"Missing files: {key!s}.{exts}")

        yield key, sorted_group


def override_defaults(
    defaults: Optional[Dict[Text, Any]], custom: Optional[Dict[Text, Any]]
) -> Dict[Text, Any]:
    """Override default config with the given config.
    code  from rasa 2.4.1
    We cannot use `dict.update` method because configs contain nested dicts.

    Args:
        defaults: default config
        custom: user config containing new parameters

    Returns:
        updated config
    """
    if defaults:
        config = copy.deepcopy(defaults)
    else:
        config = {}

    if custom:
        for key in custom.keys():
            if isinstance(config.get(key), dict):
                config[key].update(custom[key])
            else:
                config[key] = custom[key]

    return config


def init_logger(log_file=None, log_file_level=logging.NOTSET):
    """
    :param log_file: str, 文件目录
    :param log_file_level: str, 日志等级
    """
    log_format = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                                   datefmt='%m/%d/%Y %H:%M:%S')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    logger.handlers = [console_handler]
    if log_file and log_file != '':
        file_handler = logging.FileHandler(log_file,encoding="utf-8")
        file_handler.setLevel(log_file_level)
        logger.addHandler(file_handler)
    return logger

def check_bio(tags:List)->bool:
    """
    检测输入的tags是否是bio编码
    如果不是bio编码
    那么错误的类型
    (1)编码不在BIO中
    (2)第一个编码是I
    (3)当前编码不是B,前一个编码不是O
    :param tags:
    :return:
    """
    for i, tag in enumerate(tags):
        if tag == 'O':
            continue
        tag_list = tag.split("-")
        if len(tag_list) != 2 or tag_list[0] not in set(['B','I']):
            #非法编码
            return False
        if tag_list[0] == 'B':
            continue
        elif i == 0 or tags[i-1] == 'O':
            #如果第一个位置不是B或者当前编码不是B并且前一个编码0，则全部转换成B
            tags[i] = 'B' + tag[1:]
        elif tags[i-1][1:] == tag[1:]:
            # 如果当前编码的后面类型编码与tags中的前一个编码中后面类型编码相同则跳过
            continue
        else:
            # 如果编码类型不一致，则重新从B开始编码
            tags[i] = 'B' + tag[1:]
    return True


def bio_to_bioes(tags:List)->List:
    """
    把bio编码转换成bioes编码
    返回新的tags
    :param tags:
    :return:
    """
    new_tags = []
    for i, tag in enumerate(tags):
        if tag == 'O':
            # 直接保留，不变化
            new_tags.append(tag)
        elif tag.split('-')[0] == 'B':
            # 如果tag是以B开头，那么我们就要做下面的判断
            # 首先，如果当前tag不是最后一个，并且紧跟着的后一个是I
            if (i+1) < len(tags) and tags[i+1].split('-')[0] == 'I':
                # 直接保留
                new_tags.append(tag)
            else:
                # 如果是最后一个或者紧跟着的后一个不是I，那么表示单子，需要把B换成S表示单字
                new_tags.append(tag.replace('B-','S-'))
        elif tag.split('-')[0] == 'I':
            # 如果tag是以I开头，那么我们需要进行下面的判断
            # 首先，如果当前tag不是最后一个，并且紧跟着的一个是I
            if (i+1) < len(tags) and tags[i+1].split('-')[0] == 'I':
                # 直接保留
                new_tags.append(tag)
            else:
                # 如果是最后一个，或者后一个不是I开头的，那么就表示一个词的结尾，就把I换成E表示一个词结尾
                new_tags.append(tag.replace('I-', 'E-'))

        else:
            raise Exception('非法编码')
    return new_tags

def bioes_to_bio(tags:List)->List:
    """
    BIOES->BIO
    :param tags:
    :return:
    """
    new_tags = []
    for i, tag in enumerate(tags):
        if tag.split('-')[0] == "B":
            new_tags.append(tag)
        elif tag.split('-')[0] == "I":
            new_tags.append(tag)
        elif tag.split('-')[0] == "S":
            new_tags.append(tag.replace('S-','B-'))
        elif tag.split('-')[0] == "E":
            new_tags.append(tag.replace('E-','I-'))
        elif tag.split('-')[0] == "O":
            new_tags.append(tag)
        else:
            raise Exception('非法编码格式')
    return new_tags



