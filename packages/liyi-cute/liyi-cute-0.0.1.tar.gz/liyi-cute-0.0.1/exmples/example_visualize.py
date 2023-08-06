#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/29 20:33
# @Author  : Yizheng Dai
# @Email   : 387942239@qq.com
# @File    : example_visualize.py
from liyi_cute.vis.visualization import spacy_visualize
import spacy
spacy.load("en_core_web_sm")

if __name__ == '__main__':

    # doc = {'text': 'ALK-rearranged squamous cell lung carcinoma responding to crizotinib: A missing link in the field of non-small cell lung cancer? ALK-rearrangements are mainly encountered in lung adenocarcinomas and allow treating patients with anti-ALK targeted therapy. ALK-rearranged squamous cell lung carcinomas are rare tumors that can also respond to anti-ALK-targeted therapy. Nevertheless, ALK screening is not always performed in patients with squamous cell lung carcinomas making the identification and treatment of this molecular tumor subtype challenging. We intend to report a rare case of ALK-rearranged lung squamous cell carcinoma with response to crizotinib therapy. We report clinical, pathological, immunohistochemical and fluorescent in situ hybridization data concerning a patient having an ALK-rearranged squamous cell lung cancer diagnosed in our institution. The patient was a 58-year old woman with a metastatic-stage lung cancer. Histopathological and immunohistochemical analyses were performed on a bronchial biopsy sample and concluded in a non-keratinizing squamous cell lung carcinoma expressing strongly cytokeratin 5/6, p63 and p40, which are classic hallmarks of lung squamous cell carcinomas, but also cytokeratin 7 which is more commonly expressed in lung adenocarcinomas. The tumor did not express thyroid transcription factor-1. ALK rearrangement was searched because of the never-smoker status of the patient and resulted in strong positive fluorescent in situ hybridization test and ALK/p80 immunohistochemistry. The patient responded to crizotinib therapy during 213 days. Our observation points out the interest of considering ALK screening in patients with metastatic lung squamous cell carcinomas, especially in patients lacking a usual heavy-smoker clinical history. The histopathological and immunohistochemical features of this particular tumor highlighting the overlapping criteria between lung adenocarcinomas and rare ALK-rearranged squamous cell lung carcinomas could also be relevant to extend ALK screening to tumors with intermediate phenotypes between squamous cell carcinomas and adenocarcinomas and/or arising in non-smokers.', 'ents': [{'start': 0, 'end': 3, 'label': 'Gene'}]}
    #
    # html = spacy_visualize(doc, style="ent", manual=True, mode="img", output_path="001.svg")
    # print(1)
    import spacy
    from spacy import displacy
    from pathlib import Path

    nlp = spacy.load("en_core_web_sm")
    sentences = ["When Sebastian Thrun started working on self-driving cars at Google in 2007, few people outside of the company took him seriously."]
    for sent in sentences:
        doc = nlp(sent)
        svg = displacy.render(doc, style="ent", jupyter=False)
        file_name = "111.svg"
        output_path = Path(file_name)
        output_path.open("w", encoding="utf-8").write(svg)
