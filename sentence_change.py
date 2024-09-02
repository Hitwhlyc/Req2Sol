import random
import json
import os

def getSentence(text):
    sentence_content = text.split("句子：", 1)[1].split("\n", 1)[0].strip() 
    return sentence_content
def getCharactor(text):
    trimmed_string = text.strip()
    start_index = trimmed_string.find('[') + 1
    end_index = trimmed_string.find(']')
    extracted_string = trimmed_string[start_index:end_index]
    return extracted_string


def insert_symbol(text):
    insert_symbols = ['！', '？', '，', '；']
    # 确定要插入的符号数量，1到2个
    num_symbols_to_insert = random.randint(3, 4)
    # 确保句子不是空的，并且有足够的空间插入符号  
    if len(text) > 0 and num_symbols_to_insert <= len(text):  
        # 生成随机索引列表，用于插入符号。索引不能相同且不能是字符串的开头或结尾  
        insert_indices = sorted(random.sample(range(1, len(text) - 1), num_symbols_to_insert))
        # 遍历索引列表，在相应的位置插入符号  
        modified_sentence = list(text)  # 将字符串转换为列表以便插入  
        for index in insert_indices:  
            # 随机选择一个符号插入  
            symbol_to_insert = random.choice(insert_symbols)  
            modified_sentence.insert(index, symbol_to_insert)
    # 将列表转换回字符串  
    modified_sentence = ''.join(modified_sentence)
    return modified_sentence  


json_preview_path = "/data/liyuchen/datasets/test_question.json"
with open(json_preview_path, 'r') as f:
    data_without_response = json.load(f)
for i in data_without_response:
    x = i['instruction']
    change_sentence = getSentence(x)
    change_sentence_again = insert_symbol(change_sentence)
    print(change_sentence_again)
    charactor = getCharactor(x)
    print(charactor)
    i['instruction'] = "\n        请对以下句子进行意图识别。如果句子内容偏向于准备购买一款空调或者是寻求空调装配方案的推荐，请从给定的用户需求点中，挑选出最符合该句子描述的用户需求点。\n        用户需求点列表：[制冷制热, 空气净化, 稳定运行, 噪声水平, 送风方式, 智能控温, 空气质量, 节能性能, 环保认证, 外观风格, 尺寸与安装, 价格定位, 性价比, 儿童, 青少年, 老年人, 过敏, 哮喘, 慢性病, 长时间居家办公, 长时间居家学习, 经常户外运动, 炎热潮湿地区, 寒冷地区, 小房间, 大房间, 电气安全, 防护功能]，\n        基于句子的内容和上下文，选择一个最符合句子描述的用户需求点；如果句子内容与此无关，或者无法明确判断其意图，请直接用通用模型理解其含义\n        句子：" + change_sentence_again + "\n    "
data_with_change_instruction_path = "./datasets/test_question_with_change_instruction_new.json"
os.mknod(data_with_change_instruction_path)
with open(data_with_change_instruction_path, "w") as f:
    json.dump(data_without_response, f, ensure_ascii=False)