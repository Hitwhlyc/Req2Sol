import gradio as gr
import sft_llm_output
import neo4j_add
import time
from googletrans import Translator
import requests
import hashlib
import requests
import base64
import urllib.parse
import json
import os
import re

need_list = []

def create_link_text(url):
    return f"点击这里查看更多信息: {url}"


def translate_zn_to_en_baidu(text):
    APP_ID = ''#Call its own APP-ID
    SECRET_KEY = ''#Call its own SECRET_KEY
    #
    url = ""#Using Baidu Translate URL
    salt = str(time.time())
    sign = hashlib.md5((APP_ID + text + salt + SECRET_KEY).encode('utf-8')).hexdigest()
    params = {
        'q': text,
        'from': 'zh',
        'to': 'en',
        'appid': APP_ID,
        'salt': salt,
        'sign': sign
    }
    response = requests.get(url, params=params)
    result = response.json()
    # Add error handling and logging
    if 'trans_result' in result:
        return result['trans_result'][0]['dst']
    else:
        print(f"Translation API response error (returning original text): {result}")
        return text

def chatbot_response(message, history):
    print(repr(message))
    if "我想要" in message:
        pattern = re.compile(r'我想要(.*?)特征空调装配方案') 
        # 查找匹配项
        match = pattern.search(message)
        # 如果找到了匹配项，则提取 "XX"
        if match:  
            match_charactor = match.group(1)  
            text = neo4j_add.return_product_charactor(match_charactor)
            pattern_text = re.compile(r"在数据库中不存在")
            match_text = pattern_text.search(text)
            if not match_text:
            # text = create_link_text("https://docs.qq.com/pdf/DZVFoYnNNbk1JZkp2?", "特征空调装配方案")
                need_list.append(match_charactor)
        else:
            text = "未找到特征空调装配方案相关的请求"
    elif "颜色" in message:
        pattern_color =re.compile(r'搭配颜色是(.*?)空调')
        # 查找颜色匹配项
        match_color = pattern_color.search(message)
        # 如果找到了匹配项，则提取
        if match_color:
            color = match_color.group(1)
            text = neo4j_add.return_color(color)
            pattern_text = re.compile(r"在数据库中不存在")
            match_text = pattern_text.search(text)
            if not match_text:
                need_list.append(color)
        else:
            text = "未找到颜色相关的请求"
    elif "厂家" in message:
        pattern_company = re.compile(r"关于厂家和类型，我需要(.*?)的空调")
        # 查找厂家类型匹配项
        match_company = pattern_company.search(message)
        # 如果找到了匹配项，则提取
        if match_company:
            company = match_company.group(1)
            text = neo4j_add.return_company(company)
            pattern_text = re.compile(r"在数据库中不存在")
            match_text = pattern_text.search(text)
            if not match_text:
                need_list.append(company)
        else:
            text = "未找到厂家和类型相关的请求"
    elif "最高接受价格" in message:
        pattern_maxprice = re.compile(r'关于购买空调的最高接受价格为(.*?)元')
        # 查找最高价格匹配项
        match_maxprice = pattern_maxprice.search(message)
        # 如果找到了匹配项，则提取
        if match_maxprice:
            max_price = match_maxprice.group(1)
            text = neo4j_add.return_maxprice(max_price)
            pattern_text = re.compile(r"最高价格不能小于等于0")
            match_text = pattern_text.search(text)
            if not match_text:
                need_list.append(max_price)
        else:
            text = "未匹配最高价格"
    elif "最低接受价格" in message:
        pattern_lowprice = re.compile(r'关于购买空调的最低接受价格为(.*?)元')
        # 查找最低价格匹配项
        match_lowprice = pattern_lowprice.search(message)
        # 如果找到了匹配项，则提取
        if match_lowprice:
            low_price = match_lowprice.group(1)
            if int(low_price) >= int(need_list[3]):
                text = "最低价格不能高于最高价格，请重新输入：关于购买空调的最低接受价格为XX元"
            else:
                need_list.append(low_price)
                print(need_list)
                text = neo4j_add.return_product(need_list[0], need_list[1], need_list[2], need_list[3], need_list[4])    
        else:
            text = "未匹配最低价格"
    elif "该产品详细的装配方案" in message:
        text = neo4j_add.return_lowprice(need_list[0], need_list[1], need_list[2], need_list[3], need_list[4])
    elif "我不需要替换相关零部件" in message:
        text = "结束"
    elif "我要换" in message:
        pattern_compressor = re.compile(r'我要换压缩机为(.*?)型号')
        match_compressor = pattern_compressor.search(message)
        if match_compressor:
            compressor_change = match_compressor.group(1)
        else:
            compressor_change = ""
        pattern_electrical_machinery = re.compile(r'我要换电机为(.*?)型号')
        match_electrical_machinery = pattern_electrical_machinery.search(message)
        if match_electrical_machinery:
            electrical_machinery_change = match_electrical_machinery.group(1)
        else:
            electrical_machinery_change = ""
        pattern_cold_machinery = re.compile(r'我要换冷凝器为(.*?)型号')
        match_cold_machinery = pattern_cold_machinery.search(message)
        if match_cold_machinery:
            cold_machinery_change = match_cold_machinery.group(1)
        else:
            cold_machinery_change = ""
        pattern_evaporator = re.compile(r'我要换蒸发器为(.*?)型号')
        match_evaporator = pattern_evaporator.search(message)
        if match_evaporator:
            evaporator_change = match_evaporator.group(1)
        else:
            evaporator_change = ""
        text = neo4j_add.find_new_change(compressor_change, electrical_machinery_change, cold_machinery_change, evaporator_change)
    else:
        text = neo4j_add.return_charactor_list(message)
    history.append((message+"\n"+translate_zn_to_en_baidu(message), text+"\n"+translate_zn_to_en_baidu(text)))
    return history


with gr.Blocks() as demo:
    # Customize CSS
    gr.HTML("""
        <style>
            .gradio-container {
                width: 1000vw !important;
                height: 1000vh !important;
                max-width: 1500px !important;
                max-height: 3000px !important;
            }
            .gradio-textbox {
                width: 100% !important;
                height: 100px !important;
            }
            .gradio-chatbot {
                height: calc(80vh - 300px) !important;
            }
            .footer {
                display: none !important;
            }
            .message-container {
                display: flex;
                flex-direction: column;
            }
            .message {
                display: flex;
                align-items: flex-start;
                margin-bottom: 10px;
            }
            .avatar {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                margin-right: 10px;
            }
            .message-content {
                background-color: #f1f1f1;
                border-radius: 10px;
                padding: 10px;
                max-width: 80%;
            }
            .user-message .message-content {
                background-color: #d1e7dd;
            }
            .bot-message .message-content {
                background-color: #e2e3e5;
            }
        </style>
        """)
    # Dialogue History
    history = gr.State([])
    # Title and description
    gr.Markdown(
        "# Ices personalized air conditioning recommendation chatbot")
    # Display conversation history
    chatbox = gr.Chatbot()
    #Input box
    with gr.Row():
        user_input = gr.Textbox(placeholder="Type your message here...", label="Your Message")
        submit_button = gr.Button("Send")
    # Process user input and update conversation history
    submit_button.click(chatbot_response, inputs=[user_input, history], outputs=chatbox)



# Splash screens
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=8087)