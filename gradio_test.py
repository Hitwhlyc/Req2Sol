import gradio as gr
import demo_output
import time
import neo4j_add
import re

need_list = []

def create_link_text(url):
    return f"点击这里查看更多信息: {url}"


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
            need_list.append(low_price)
            text = neo4j_add.return_lowprice(need_list[0], need_list[1], need_list[2], need_list[3], need_list[4])
        else:
            text = "未匹配最低价格"
    else:
        text = neo4j_add.return_charactor_list(message)

    return text


    # for i in range(len(text)):
    #     time.sleep(0.1)
    #     yield "机器人回复: " + text[: i+1]
        
        
demo = gr.ChatInterface(
    fn=chatbot_response,
    title="ICES个性化空调推荐聊天机器人",
    css="./css/test1.css").queue()

if __name__ == "__main__":
    demo.launch()


