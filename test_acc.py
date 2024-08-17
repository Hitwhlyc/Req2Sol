import json

json_with_response_path = "/data/liyuchen/test_output/Bloom_7B/Bloom_7B_with_eda/data_Bloom_7B_with_eda_epoch_4.json"
x1 = 0
with open(json_with_response_path, 'r') as f:
    data_with_response = json.load(f)
x2 = len(data_with_response)
for i in data_with_response:
    if i['response'] == i['output']:
        x1 = x1 + 1
acc = x1/x2
print(x2)
print(x1)
print(acc)