#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/2 22:55
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : metric.py

"""
准确率: accuracy = 预测对的元素个数/总的元素个数
查准率：precision = 预测正确的实体个数 / 预测的实体总个数
召回率：recall = 预测正确的实体个数 / 标注的实体总个数
F1值：F1 = 2 *准确率 * 召回率 / (准确率 + 召回率)
"""
from __future__ import annotations

from typing import List
import time


from seqeval.metrics import f1_score
from seqeval.metrics import precision_score
from seqeval.metrics import accuracy_score
from seqeval.metrics import recall_score
from seqeval.metrics import classification_report


def nerMetrics(true_labels, pre_labels, logger):
    """
    :param true_labels 真实标签数据 [O,O,B-OR, I-OR]
    :param pre_labels 预测标签数据 [O,O,B-OR, I-OR]
    :param logger 日志实例
    """
    start_time = time.time()
    acc = accuracy_score(true_labels, pre_labels)
    f1score = f1_score(true_labels, pre_labels, average='macro')
    report = classification_report(true_labels, pre_labels, digits=4)
    msg = '\nTest Acc: {0:>6.2%}, Test f1: {1:>6.2%}'
    logger.info(msg.format(acc, f1score))
    logger.info("\nPrecision, Recall and F1-Score...")
    logger.info("\n{}".format(report))
    time_dif = time.time() - start_time
    logger.info("Time usage:{0:>.6}s".format(time_dif))