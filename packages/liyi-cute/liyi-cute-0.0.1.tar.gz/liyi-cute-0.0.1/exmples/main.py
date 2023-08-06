# -*- encoding: utf-8 -*-
'''
Filename         :main.py
Description      :
Time             :2022/03/26 00:32:41
Author           :daiyizheng
Email            :387942239@qq.com
Version          :1.0
'''

# 关系标注
# ann 转 json
## ann 中的数据
import json
import os
import random
import logging

from tqdm import tqdm

logger = logging.getLogger(__file__)


class PubTatorParseData(object):
    def __init__(self) -> None:
        self.alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                         't', 'u', 'v', 'w', 'x', 'y', 'z',
                         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                         'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.special_symbols = ["(", ")", ",", ".", "/", ">", "<", ";", "-"]

    def check_annotations(self, train_texts, infomations) -> bool:
        for an in infomations.values():
            start_id = an[0]
            end_ids = start_id + an[1]
            if train_texts[start_id:end_ids] != an[2]:
                logger.warning("start_ids: " + str(start_id))
                logger.warning("end_ids: " + str(end_ids))
                logger.warning("text content: " + train_texts[start_id:end_ids])
                logger.warning("annotations content: " + an[2])
                return False
        return True

    def parse_biocjson(self, input_path, output_path):
        json_data_list = os.listdir(input_path)
        for index, file_name in tqdm(enumerate(json_data_list)):
            output_file_name = os.path.join(output_path, file_name.split(".")[0] + ".txt")
            text, infomations = self.load_json(os.path.join(input_path, file_name))
            is_aligned_tag = self.check_annotations(text, infomations)
            ## 文本和实体是否对齐
            if is_aligned_tag:
                all_tokens, all_tags = self.__json2txt(text, infomations)
                self.save_file(all_tokens, all_tags, output_file_name)
            else:
                logger.warning("文本与实体未对齐：" + file_name)

    def load_json(self, input_path):
        data = json.load(open(input_path, 'r', encoding="utf-8"))
        text = ""
        infomations = {}
        for item in data["passages"]:
            if item["text"]:
                text = text + item["text"] + " "
                for anns in item["annotations"]:
                    if anns["text"].strip() != "":
                        infomations.update({anns["locations"][0]["offset"]: [anns["locations"][0]["offset"],
                                                                             anns["locations"][0]["length"],
                                                                             anns["text"], anns["infons"]["type"]]})
        text = text.rstrip()
        return text, infomations

    def __json2txt(self, text, infomations):
        idx = 0
        all_tokens = []
        all_tags = []
        while (idx < len(text)):
            ## 标注信息
            if idx in infomations:
                start = infomations[idx][0]
                end = start + infomations[idx][1]
                type_name = infomations[idx][3]
                tokens_list = text[start:end].split(" ")
                tags_list = ["B-" + type_name]
                for _ in tokens_list[1:]:
                    tags_list.append("I-" + type_name)
                all_tokens += tokens_list
                all_tags += tags_list
                idx = end
            else:
                ## 空格直接换行
                if text[idx] == " ":
                    idx = idx + 1
                elif text[idx] in self.alphabet:
                    i = idx
                    idx = idx + 1
                    ## 纯字母xxx 或者 多字母拼接xx-xx 或者字母和数字拼接xx123
                    while (idx < len(text) - 1 and (
                            text[idx] in self.alphabet or text[idx] == "-" or text[idx] in self.digits)):
                        idx = idx + 1
                    all_tokens.append(text[i:idx])
                    all_tags.append("O")
                else:
                    # 如果是数字或者小数点数字
                    if text[idx].isdigit():
                        i = idx
                        idx = idx + 1
                        while (idx < len(text) - 1 and (text[idx].isdigit() or (
                                idx < len(text) - 2 and text[idx] == "." and text[idx + 1] != " "))):
                            idx = idx + 1
                        all_tokens.append(text[i:idx])
                        all_tags.append("O")
                    ## 句子结束. 后面多加一个加换行
                    if text[idx] == "." and idx < len(text) - 2 and text[idx + 1] == " ":
                        all_tokens.append(text[idx])
                        all_tags.append("O")
                        idx = idx + 1
                        ## 换行
                        all_tokens.append("\n")
                        all_tags.append("\n")
                    else:
                        all_tokens.append(text[idx])
                        all_tags.append("O")
                        idx = idx + 1
        assert len(all_tokens) == len(all_tags), "tokens length is not equal tags length"
        return all_tokens, all_tags

    def save_file(self, all_tokens, all_tags, output_path):
        with open(output_path, "w", encoding="utf-8") as fw:
            for tn, tg in zip(all_tokens, all_tags):
                if tn != "\n":
                    fw.write(tn + "\t" + tg)
                    fw.write("\n")
                else:
                    fw.write("\n")

    def split_data(self, input_path, shuffle=True, split_rate=0.95):
        all_tokens, all_tags = self.load_token_tag(input_path)
        all_content = list(zip(all_tokens, all_tags))
        n_total = len(all_content)
        offset = int(n_total * split_rate)
        if n_total == 0 or offset < 1:
            return all_content, []
        if shuffle:
            random.shuffle(all_content)
        return all_content[:offset], all_content[offset:]

    def load_token_tag(self, input_path, format_type="txt"):
        file_list = os.listdir(input_path)
        file_path_list = [os.path.join(input_path, file_name) for file_name in file_list if
                          file_name.endswith(format_type)]
        all_tokens = []
        all_tags = []
        for p in tqdm(file_path_list):
            tokens, tags = self.__read_txt(p)
            all_tokens.extend(tokens)
            all_tags.extend(tags)

        return all_tokens, all_tags

    def __read_txt(self, input_path):
        all_tokens = []
        all_tags = []
        per_file_tokens = []
        per_file_tags = []
        with open(input_path, 'r', encoding="utf-8") as fr:
            lines = fr.readlines()
            for line in lines:
                line = line.strip()
                if line:
                    line_list = line.split("\t")
                    if len(line_list) == 2:
                        per_file_tokens.append(line_list[0])
                        per_file_tags.append(line_list[1])
                else:
                    if per_file_tokens:
                        all_tokens.append(per_file_tokens)
                        all_tags.append(per_file_tags)
                    per_file_tokens = []
                    per_file_tags = []
        return all_tokens, all_tags

    def save_json(self, data):
        pass


if __name__ == '__main__':
    ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(ROOT_PATH, "../../", "datasets", "pubtator_dataset", "output", "pmcid")
    ob = PubTatorParseData()
    ob.parse_biocjson(DATA_PATH, DATA_PATH)
    # train, valid = ob.split_data(DATA_PATH)
    print(1)
