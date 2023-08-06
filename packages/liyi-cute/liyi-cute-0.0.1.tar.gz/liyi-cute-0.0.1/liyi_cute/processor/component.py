#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/2 13:23
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : component.py
from typing import Optional, Dict, Text, Any

from liyi_cute.utils.common import override_defaults


class Component(object):
    defaults = {}
    def __init__(self, component_config: Optional[Dict[Text, Any]] = None):

        if not component_config:
            component_config = {}

        self.component_config = override_defaults(
            self.defaults, component_config
        )


    @classmethod
    def load(cls):
        raise NotImplementedError

    @classmethod
    def create(cls, component_config: Dict[Text, Any],):
        return cls(component_config)

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        """Persists this component to disk for future loading.

        Args:
            file_name: The file name of the model.
            model_dir: The directory to store the model to.

        Returns:
            An optional dictionary with any information about the stored model.
        """
        pass