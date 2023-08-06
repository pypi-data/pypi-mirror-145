#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/27 14:56
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : io.py
from __future__ import annotations
import dataclasses
import json
from typing import Dict, Union, Text, Any, List
from pathlib import Path
import os

from liyi_cute.shared.exceptions import (FileIOException, FileNotFoundException)
from liyi_cute.shared.imports.schemas.schemaItem import ExampleSchema

from liyi_cute.shared.imports.schemas.schema import Example

DEFAULT_ENCODING = "utf-8"

def write_text_file(
    content: Text,
    file_path: Union[Text, Path],
    encoding: Text = DEFAULT_ENCODING,
    append: bool = False,
) -> None:
    """Writes text to a file. code come from
    Args:
        content: The content to write.
        file_path: The path to which the content should be written.
        encoding: The encoding which should be used.
        append: Whether to append to the file or to truncate the file.
    """
    mode = "a" if append else "w"
    with open(file_path, mode, encoding=encoding) as file:
        file.write(content)


def json_to_string(obj: Any, **kwargs: Any) -> Text:
    """Dumps a JSON-serializable object to string.
    code come from https://github.com/RasaHQ/rasa/blob/rasa/shared/nlu/training_data/formats/rasa.py#L109
    Args:
        obj: JSON-serializable object.
        kwargs: serialization options. Defaults to 2 space indentation
                and disable escaping of non-ASCII characters.
    Returns:
        The objects serialized to JSON, as a string.
    """
    indent = kwargs.pop("indent", 2)
    ensure_ascii = kwargs.pop("ensure_ascii", False)
    return json.dumps(obj, indent=indent, ensure_ascii=ensure_ascii, **kwargs)

def examples_as_json(examples: List[Example], **kwargs: Any)->str:
    """
    :param examples:
    :return:
    """
    examples =  ExampleSchema().dump(examples, many= True if isinstance(examples, List) else False)
    output = json_to_string(examples, indent=2, ensure_ascii=False, **kwargs)
    return output


def read_file(filename: Union[Text, Path], encoding: Text = DEFAULT_ENCODING) -> Any:
    """Read text from a file."""

    try:
        with open(filename, encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundException(
            f"Failed to read file, " f"'{os.path.abspath(filename)}' does not exist."
        )
    except UnicodeDecodeError:
        raise FileIOException(
            f"Failed to read file '{os.path.abspath(filename)}', "
            f"could not read the file using {encoding} to decode "
            f"it. Please make sure the file is stored with this "
            f"encoding.")


def read_json_file(filename: Union[Text, Path]) -> Any:
    """Read json from a file."""
    content = read_file(filename)
    try:
        return json.loads(content)
    except ValueError as e:
        raise FileIOException(f"Failed to read json from '{os.path.abspath(filename)}'. Error: {e}")