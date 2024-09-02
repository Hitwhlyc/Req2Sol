<p align="center" width="100%">
<a href="https://github.com/SCIR-HI/Huatuo-Llama-Med-Chinese/" target="_blank"><img src="assets/logo/logo_new.png" alt="SCIR-HI-HuaTuo" style="width: 60%; min-width: 300px; display: block; margin: auto;"></a>
</p>

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
###Base models <br>
[Bloomz-7b1](URL "[Bloommz-7b1](https://modelscope.cn/models/AI-ModelScope/bloomz-7b1)") <br>
[Meta-Llama-3-8B](URL "[Meta-Llama-3-8B](https://modelscope.cn/models/LLM-Research/Meta-Llama-3-8B)") <br>
[Yi-6B](URL "[Yi-6B](https://modelscope.cn/models/01ai/Yi-6B)") <br>
[Mistral-7B-Instruct-v0.2](URL "[Mistral-7B-Instruct-v0.2](https://modelscope.cn/models/AI-ModelScope/Mistral-7B-Instruct-v0.2)") <br>


