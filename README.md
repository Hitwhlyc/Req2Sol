# Req2Sol
A Large Language Model capable of understanding Requirements to recommend the product assembly Solutions
## requirements
python==3.8 <br>
gradio==4.41.0 <br>
neo4j==5.23.1 <br>
numpy==1.26.4 <br>
peft==0.12.0 <br>
torch==2.1.2 <br>
## Brief Introduction
In the field of industrial assembly, user needs are increasingly intertwined with the final product assembly. Currently, the work done in the industry tends to describe specific concepts and related physical facilities in industrial assembly, which makes it difficult to meet the connection between user needs and products. We innovatively associate user needs with products through knowledge graphs, achieving full process control from user needs to industrial product assembly.
## A quick start
For all base models, we adopted the LoRA fine-tuning method for instruction fine-tuning training to balance computational resources and model performance.
**Base models**


