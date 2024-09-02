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
### Dataset acquisition method
The design of prompt words plays an important role in this study, as it determines the quality of the generated question and answer pairs. For this purpose, we designed multiple prompt words for verification and manually compared the corresponding results. Finally, we selected the group of prompt words with the best manual evaluation effect for generating instruction fine-tuning question answer pairs. The Chinese content has been translated into English. <br>
The training set data example for instruction fine-tuning is as follows: <br>

```
    {
        "instruction": "\n        请对以下句子进行意图识别。如果句子内容偏向于准备购买一款空调或者是寻求空调装配方案的推荐，请从给定的用户需求点中，挑选出最符合该句子描述的用户需求点。\n        用户需求点列表：[防护功能, 长时间居家办公, 大房间, 制冷制热]，\n        基于句子的内容和上下文，选择一个最符合句子描述的用户需求点；如果句子内容与此无关，或者无法明确判断其意图，请直接用通用模型理解其含义\n        句子：我希望空调制冷效果快，有什么推荐的吗？\n    ",
        "input": "",
        "output": "制冷制热"
    },
```
The relevant question and answer pairs generated through the above operation can be used for preliminary instruction fine-tuning. However, due to the limited number of scenarios and related demand points in the industrial assembly field, it cannot meet the needs of large-scale fine-tuning. Moreover, sentiment analysis using large language models is an important task, but high performance often depends on the size and quality of the training data. <br>
Therefore, we referred to Jason Wei's work  and conducted data augmentation based on EDA,effectively improving the performance of text classification tasks.  <br>
- [EDA](https://github.com/jasonwei20/eda_nlp) <br>

Specifically, this study conducted large-scale data augmentation and enhancement on text data through operations such as synonym replacement, random insertion, random swapping, and random deletion. The original small batch data was transformed into a large batch of data, effectively expanding the size of the training data.
### Dataset
In this system, we have set up two types of datasets, one is the normal dataset·`./dataset/original_question.json` and enhanced dataset with data augmentation·`./dataset/aug_question.json.json`
## Train
### Training Details
We conducted experiments on four NVIDIA GeForce RTX3090s under the experimental conditions. In terms of fine-tuning, this study used lora fine-tuning with lora_r set to 8, lora_alpha set to 16, lora_dropout set to 0.05, batch_2 set to 4, and epochs set to 10. This study set one epoch to output the corresponding results and evaluated them on the validation set under normal and chaotic conditions. We selected four base models, Meta-Llama-3-8B, BLOOMz-7B1, Yi-6B, and Mistral-7B-Instruct-v0.2, for evaluation
### LoRA download
LoRA weight can be downloaded through Baidu Netdisk：
- Bloomz-7b1：[Baidu Netdisk](https://pan.baidu.com/s/1f4XeybVUflwMS_TNlr7yTw?pwd=7jbs)
- Meta-Llama-3-8B：[Baidu Netdisk](https://pan.baidu.com/s/1f4XeybVUflwMS_TNlr7yTw?pwd=7jbs)
- Yi-6B：[Baidu Netdisk](https://pan.baidu.com/s/1f4XeybVUflwMS_TNlr7yTw?pwd=7jbs)
- Mistral-7B-Instruct-v0.2：[Baidu Netdisk](https://pan.baidu.com/s/1f4XeybVUflwMS_TNlr7yTw?pwd=7jbs)
## Comparison of Model Effects
### Choose Base Model
The results under normal conditions and under chaotic conditions are shown in the following two tables。
- Table1：Normal data

  
| Accuracy | 1  | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | Avg |
|:------------- |:---------------| :-------------|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|
|Meta-Llama-3-8B(without-eda)|0.6952|0.7357|0.7738|0.7571|0.7548|0.7929|0.7857|0.7952|0.8048|0.8095|0.77047|
|Meta-Llama-3-8B(with-eda)|0.7619|0.7714|0.7667|0.8048|0.7762|0.7738|0.8071|0.8|0.8262|0.8286|**0.79167**|
|Bloomz-7b1(without-eda)|0.781|0.7643|0.7429|0.7548|0.7714|0.7881|0.8|0.7857|0.7905|0.7905|0.77692|
|Bloomz-7b1(with-eda)|0.7857|0.769|0.7952|0.8167|0.8048|0.8167|0.7595|0.8071|0.8119|0.8476|**0.80142**|
|Yi-6B(without-eda)|0.7286|0.781|0.7262|0.7357|0.7667|0.7929|0.7738|0.7833|0.781|0.7786|0.76478|
|Yi-6B(with-eda)|0.8|0.8024|0.7833|0.7976|0.7381|0.7786|0.8024|0.8071|0.7952|0.8071|**0.79118**|
|Mistral-7B-Instruct-v0.2(without-eda)|0.6405|0.7095|0.5643|0.7262|0.719|0.7595|0.7667|0.7833|0.769|0.7714|**0.72094**|
|Mistral-7B-Instruct-v0.2(with-eda)| 0.6786|0.6881|0.6786|0.4048|0.6|0.6214|0.6929|0.7024|0.731|0.7548|0.65526|

- Table2：chaotic data

| Accuracy | 1  | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | Avg |
|:------------- |:---------------| :-------------|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|
|Meta-Llama-3-8B(without-eda)|0.6952|0.7357|0.7738|0.7571|0.7548|0.7929|0.7857|0.7952|0.8048|0.8095|0.77047|
|Meta-Llama-3-8B(with-eda)|0.7619|0.7714|0.7667|0.8048|0.7762|0.7738|0.8071|0.8|0.8262|0.8286|**0.79167**|
|Bloomz-7b1(without-eda)|0.781|0.7643|0.7429|0.7548|0.7714|0.7881|0.8|0.7857|0.7905|0.7905|0.77692|
|Bloomz-7b1(with-eda)|0.7857|0.769|0.7952|0.8167|0.8048|0.8167|0.7595|0.8071|0.8119|0.8476|**0.80142**|
|Yi-6B(without-eda)|0.7286|0.781|0.7262|0.7357|0.7667|0.7929|0.7738|0.7833|0.781|0.7786|0.76478|
|Yi-6B(with-eda)|0.8|0.8024|0.7833|0.7976|0.7381|0.7786|0.8024|0.8071|0.7952|0.8071|**0.79118**|
|Mistral-7B-Instruct-v0.2(without-eda)|0.6405|0.7095|0.5643|0.7262|0.719|0.7595|0.7667|0.7833|0.769|0.7714|**0.72094**|
|Mistral-7B-Instruct-v0.2(with-eda)| 0.6786|0.6881|0.6786|0.4048|0.6|0.6214|0.6929|0.7024|0.731|0.7548|0.65526|
