# -*- coding:UTF-8 -*-

# author:user
# contact: test@test.com
# datetime:2022/3/29 16:40
# software: PyCharm

"""
文件说明：
    
"""
from __future__ import annotations
from typing import Dict

from spacy import displacy
import spacy


from liyi_cute.shared.exceptions import NotExistException
from liyi_cute.utils.constants import GRADIENTS

def spacy_visualize(doc:Dict, options={}, style="dep",
                    manual=False, jupyter=False, mode="html",
                    lang="en_core_web_sm"):
    """
    :param doc:
    ent example: {"text": "But Google is starting from behind.", "ents": [{"start": 4, "end": 10, "label": "ORG"],"title": None}
    dep example: dep = {"words": [{"text": "This", "tag": "DT"}, {"text": "is", "tag": "VBZ"}], "arcs": [{"start": 0, "end": 1, "label": "nsubj", "dir": "left"}]}
    :param options:
    :param style:
    :param manual: Don't parse `Doc` and instead expect a dict/list of dicts.
    :param jupyter:
    :param mode: html, serve
    :param mode: lang
    :return:
    """
    spacy.load(lang)

    if not options:
        options = spacy_options(doc)

    if mode=="html":
        return displacy.render(doc, style=style, options=options,
                               manual=manual, jupyter=jupyter)

    displacy.serve(doc, style=style, manual=manual, options=options)

def spacy_options(doc:Dict)->Dict:
    """
    :param doc:
    :return:
    """
    labels = set()
    ents = doc.get("ents", [])
    for en in ents:
        if "label" not in en:
            raise NotExistException(f"key error: label")
        labels.add(en.get("label"))
    op_labels = []
    op_colors = {}

    for index, label in enumerate(labels):
        idx = index%len(labels)
        op_labels.append(label.upper())
        op_colors.update({label.upper():GRADIENTS[idx]})

    return {"ents": op_labels, "colors": op_colors}

def check_doc(doc, style="dep"):
    pass
