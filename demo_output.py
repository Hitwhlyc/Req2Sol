import json
from transformers import AutoModelForCausalLM, AutoTokenizer, LlamaTokenizer, set_seed
from peft import PeftModel
import torch
import os
import re
import itertools
from tqdm import tqdm


fine_tune_path = ""#此处放入微调的路径
base_model = "" #此处放入基模型路径
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
                    {sentence}
                                
                    ### Response:""".format(sentence = s)
    # device = torch.device('cuda:auto')
    tokenizer = AutoTokenizer.from_pretrained("#此处放入基模型路径", trust_remote_code=True)
    ipt1 = tokenizer.encode(prompt, return_tensors="pt")
    lora = PeftModel.from_pretrained(model, fine_tune_path)

    # # device = torch.device('cuda:3')
    lora.half()

    x = tokenizer.decode(model.generate(inputs=ipt1)[0], skip_special_tokens=True, max_new_tokens = 10)
    print(x)
    charactor = extract_test_after_colon(x)
    print("1"+charactor)
    return charactor

if __name__ == "__main__":
    s = input("请输入：")
    charactor = demo_outputs(s)
    print(charactor)
    
    

