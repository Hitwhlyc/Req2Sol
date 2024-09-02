# Req2Sol
A Large Language Model capable of understanding Requirements to recommend the product assembly Solutions
## requirements
- python==3.8 <br>
- gradio==4.41.0 <br>
- neo4j==5.23.1 <br>
- numpy==1.26.4 <br>
- peft==0.12.0 <br>
- torch==2.1.2 <br>
## Brief Introduction
In the field of industrial assembly, user needs are increasingly intertwined with the final product assembly. Currently, the work done in the industry tends to describe specific concepts and related physical facilities in industrial assembly, which makes it difficult to meet the connection between user needs and products. We innovatively associate user needs with products through knowledge graphs, achieving full process control from user needs to industrial product assembly.
## A quick start
For all base models, we adopted the LoRA fine-tuning method for instruction fine-tuning training to balance computational resources and model performance. <br>
### Base models
- [Bloomz-7b1](https://huggingface.co/bigscience/bloomz-7b1)
- [Meta-Llama-3-8B](https://modelscope.cn/models/LLM-Research/Meta-Llama-3-8B)
- [Yi-6B](https://modelscope.cn/models/01ai/Yi-6B)
- [Mistral-7B-Instruct-v0.2](https://modelscope.cn/models/AI-ModelScope/Mistral-7B-Instruct-v0.2)
## Dataset acquisition method
The design of prompt words plays an important role in this study, as it determines the quality of the generated question and answer pairs. For this purpose, we designed multiple prompt words for verification and manually compared the corresponding results. Finally, we selected the group of prompt words with the best manual evaluation effect for generating instruction fine-tuning question answer pairs. The Chinese content has been translated into English. <br>
The training set data example for instruction fine-tuning is as follows: <br>

```
    {
        "instruction": "\n        请对以下句子进行意图识别。如果句子内容偏向于准备购买一款空调或者是寻求空调装配方案的推荐，请从给定的用户需求点中，挑选出最符合该句子描述的用户需求点。\n        用户需求点列表：[防护功能, 长时间居家办公, 大房间, 制冷制热]，\n        基于句子的内容和上下文，选择一个最符合句子描述的用户需求点；如果句子内容与此无关，或者无法明确判断其意图，请直接用通用模型理解其含义\n        句子：我希望空调制冷效果快，有什么推荐的吗？\n    ",
        "input": "",
        "output": "制冷制热"
    },
```

## Dataset
In this system, we have set up two types of datasets, one is the normal dataset·`./dataset/original_question.json` and enhanced dataset with data augmentation·`./dataset/aug_question.json.json`

##


