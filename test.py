import json
from transformers import AutoModelForCausalLM, AutoTokenizer, LlamaTokenizer, set_seed
from peft import PeftModel
import torch
import os
import re
import itertools
from tqdm import tqdm

os.environ['CUDA_LAUNCH_BLOCKING'] = '1'
os.environ['TORCH_USE_CUDA_DSA'] = '1'

def extract_test_after_colon(sentence):
    target_str = "### Response:"
    pattern = rf'{re.escape(target_str)}(.*)'
    match = re.search(pattern, sentence)
    if match:
        return match.group(1).strip()
    else:
        return None
    


fine_tune_path = ""#放入微调后的模型
json_preview_path = ""#放入验证集的json文件
with open(json_preview_path, 'r') as f:
    data_without_response = json.load(f)
base_model = ""#基模型路径
model = AutoModelForCausalLM.from_pretrained(base_model,  trust_remote_code=True, max_length=4096, torch_dtype=torch.float16,device_map="auto")
model = model.eval()
with torch.no_grad():
    for i in tqdm(data_without_response):
        prompt = """Below is an instruction that describes a task Write a response that appropriately completes the request.\n\n 

                            ### Instruction:
                            {sentence}
                                
                            ### Response:""".format(sentence = i['instruction'])
        # device = torch.device('cuda:auto')
        tokenizer = AutoTokenizer.from_pretrained("#基模型路径", trust_remote_code=True)
        ipt1 = tokenizer.encode(prompt, return_tensors="pt").to('cuda')
        lora = PeftModel.from_pretrained(model, fine_tune_path)

        # device = torch.device('cuda:3')
        lora.half()

        x = tokenizer.decode(model.generate(inputs=ipt1)[0], skip_special_tokens=True, max_new_tokens = 10)
        charactor = extract_test_after_colon(x)
        print(charactor)
        i['response'] = charactor
data_with_response_path = "#验证文件输出路径"
os.mknod(data_with_response_path)
with open(data_with_response_path, "w") as f:
    json.dump(data_without_response, f, ensure_ascii=False)
    