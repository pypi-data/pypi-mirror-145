## 依赖
python=3.8.5

spacy==2.3.1
en-core-web-sm==2.3.0
marshmallow== 3.15.0 
transformers==4.17.0
setuptools-scm==6.4.2
seqeval == 1.2.2
## 序列化和反序列化
https://marshmallow.readthedocs.io/en/stable/
https://www.7forz.com/3694/
## 数据结构

```json
{
 "id": 1,
  "document": "xxxx",
  "": ""
}
```
# 信息抽取
实体抽取， 关系抽取，事件抽取， 属性抽取
以brat标注为例子:
标注文件开头标志
Entity: T
```yaml
[entities]
Protein
Entity

T8	Negative_regulation 659 668	deficient
T9	Gene_expression 684 694	expression
```
```json
{
"entities":[{"mention": "expression",
  "type": "Gene_expression",
  "start": 447,
  "end": 457,
  "id": "T1"}]
  }
```
Rlation: R
```yaml
[relations]

Protein-Component	Arg1:Protein, Arg2:Entity
Subunit-Complex	Arg1:Protein, Arg2:Entity

R1	Protein-Component Arg1:T11 Arg2:T19
R2	Protein-Component Arg1:T11 Arg2:T18

## 暂时不支持
Equiv	Arg1:Protein, Arg2:Protein, <REL-TYPE>:symmetric-transitive
*	Equiv T3 T4
```

```json
   {"relations": [{"type": "Part-of",
                 "arg1": {"mention": "c-Rel","type": "Protein","start": 139,"end": 144,"id": "T1"},
                 "arg2": {"mention": "NF-kappa B","type": "Complex", "start": 163, "end": 173, "id": "T2"},
                 "id": "R1"}]}
```

Event: E 暂时不支持
```yaml
[events]

Gene_expression Theme:Protein
Binding Theme+:Protein

E3	Binding:T9 Theme:T4 Theme2:T5 Theme3:T6
E4	Binding:T20 Theme:T16 Theme2:T17 Theme3:T19

## 暂时不支持
E6	Negative_regulation:T10 Cause:E3 Theme:E5
```
Attribute: A 暂时不支持
```yaml
[attributes]

Negation        Arg:<EVENT>
Confidence        Arg:<EVENT>, Value:Possible|Likely|Certain

```
# 解析不同格式文件，到统一的序列格式，


## 文件导出 yaml json pickle txt ann

## 功能
1. 解析
2. 数据格式转换
3. 导出
4. 可视化
5. 统计数据 (单词词频， 词表大小， 总共单词数量， 标签类型， 标签个数， 标签频数)