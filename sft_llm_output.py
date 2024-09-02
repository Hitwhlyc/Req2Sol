import json
from transformers import AutoModelForCausalLM, AutoTokenizer, LlamaTokenizer, set_seed
from peft import PeftModel
import torch
import os
import re
import itertools
from tqdm import tqdm


fine_tune_path = ""#Insert fine-tuning path
base_model = "" #Insert into the base model path
def extract_test_after_colon(sentence):
    target_str = "### Response:"
    pattern = rf'{re.escape(target_str)}(.*)'
    match = re.search(pattern, sentence)
    if match:
        return match.group(1).strip()
    else:
        return None
    

def demo_outputs(s):
    model = AutoModelForCausalLM.from_pretrained(base_model,  trust_remote_code=True, max_length=4096, torch_dtype=torch.float16,device_map="auto")
    model = model.eval()
    with torch.no_grad():
        prompt = """Below is an instruction that describes a task Write a response that appropriately completes the request.\n\n 

                    ### Instruction:
                    \n        请对以下句子进行意图识别。如果句子内容偏向于准备购买一款空调或者是寻求空调装配方案的推荐，请从给定的用户需求点中，挑选出最符合该句子描述的用户需求点。\n        用户需求点列表：[制冷制热, 空气净化, 稳定运行, 噪声水平, 送风方式, 智能控温, 空气质量, 节能性能, 环保认证, 外观风格, 尺寸与安装, 价格定位, 性价比, 儿童, 青少年, 老年人, 过敏, 哮喘, 慢性病, 长时间居家办公, 长时间居家学习, 经常户外运动, 炎热潮湿地区, 寒冷地区, 小房间, 大房间, 电气安全, 防护功能]，\n        基于句子的内容和上下文，选择一个最符合句子描述的用户需求点；如果句子内容与此无关，或者无法明确判断其意图，请直接用通用模型理解其含义\n        句子：{sentence}\n    
                                
                    ### Response:""".format(sentence = s)
    # device = torch.device('cuda:auto')
    tokenizer = AutoTokenizer.from_pretrained("#Insert into the base model path", trust_remote_code=True)
    ipt1 = tokenizer.encode(prompt, return_tensors="pt")
    lora = PeftModel.from_pretrained(model, fine_tune_path)

    # # device = torch.device('cuda:3')
    lora.half()

    x = tokenizer.decode(model.generate(inputs=ipt1)[0], skip_special_tokens=True, max_new_tokens = 10)
    charactor = extract_test_after_colon(x)
    return charactor
    

