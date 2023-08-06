#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/30 19:40
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : test.py

import pickle
import spacy
from liyi_cute.shared.imports.pmid_parser import PmidParser
from spacy.gold import docs_to_json, biluo_tags_from_offsets, spans_from_biluo_tags
nlp = spacy.load('en_core_web_sm')

# obj = PmidParser(task_name="ner", error="ignore")
# examples = obj.parse(r"../data/pmcid")
#
# with open("../data/output/pmcid.pkl", "wb") as f:
#     pickle.dump(examples, f)

with open("../data/output/pmid.pkl","rb") as f:
    examples=pickle.load(f)

print(len(examples))
## 转cnoll格式的文件
"""
[{"id":"001",
"text":""
"p":[{
      "id":"1",
      "short_text":""
      "text_list":[],
      "tag_list":[],
      "entities":[],
      "relations":[]
}]
}
]

"""
TRAIN_DATA = []
for example in examples:
    text = example.text
    id = example.id
    entities_list = example.entities
    entities = []
    TRAIN_DATA.append((id, text, {"entities": [(ent.start, ent.end, ent.type.upper())for ent in entities_list]}))

all_data = []
all_tags = []
docs = []
for id, text, annot in TRAIN_DATA:
    doc = nlp(text)
    try:
        tags = biluo_tags_from_offsets(doc, annot['entities'])
    except Exception as e:
        print(id, "---")
        continue
    entities = spans_from_biluo_tags(doc, tags)
    doc.ents = entities
    data = []
    tags = []
    for token in doc:
        if token.is_sent_end:
            ent_iob = token.ent_iob_
            if token.ent_iob_ !="O":
                ent_iob = token.ent_iob_ + "-" + token.ent_type_
            data.append(token.text)
            tags.append(ent_iob)
            all_data.append(data)
            all_tags.append(tags)
            data = []
            tags = []
        else:
            data.append(token.text)
            ent_iob = token.ent_iob_
            if token.ent_iob_ != "O":
                ent_iob = token.ent_iob_ + "-" + token.ent_type_
            tags.append(ent_iob)


# a = docs_to_json(docs)
txt_w = open("../data/output/pmid.txt", 'w', encoding='utf-8')
for idx in range(len(all_data)):
    assert len(all_data[idx])==len(all_tags[idx]), "长度不一致"
    cont = list(zip(all_data[idx],all_tags[idx])) #[(),()]
    for c in cont:
        txt_w.write("\t".join(c)+"\n")
    txt_w.write("\n")

txt_w.close()