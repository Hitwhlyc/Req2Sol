# air-condition-chat-system
Examples of personalized recommendations in the field of air conditioning assembly
# requirements
python=3.8 <br>
gradio=4.41.0 <br>
neo4j=5.23.1 <br>
numpy=1.26.4 <br>
peft=0.12.0 <br>
torch=2.1.2 <br>
# Instructions
需要下载基模型并结合我们给出的lora微调信息进行融合，将lora微调文件路径放入demo_output.py文件中的第11行,基模型路径放入第13行
2.  导入知识图谱，并在neo4j_add.py第8行和第9行输入自己的账号和密码，账号密码获取在neo4j创建时即可知。
3.  通过python gradio_test.py即可运行相关程序
4.  知识图谱数据由于比较私人化，目前暂时未上传至gitee仓库中。
5.  初始微调数据详见original_question.json文件，由于数据增强后的文件内容过大，可以自行通过EDA: Easy Data Augmentation Techniques for Boosting Performance on Text Classification Tasks这篇论文进行相关复现，相关源码在github上也拥有。

