from neo4j import GraphDatabase
import itertools
# import output_charactor
import demo_output


neo4j_uri = "bolt://localhost:7687"
neo4j_user = "" #此处输入neo4j知识图谱的账号
neo4j_password = "" #此处输入neo4j知识图谱的密码

products_plan = []
compressor_plan = []
electrical_machinery_plan = []
cold_machinery_plan = []
evaporator_plan = []
charactor_plan = []


#查找与需求有关的产品特征
def find_charactor_with_need(tx, need_name):
    #执行Cypher查询来找出与需求有关的产品特征信息
    charactor_result = tx.run(
        '''
        MATCH (i:KeyNeed {name:$need_name})-[:has_charactor]->(c:InstanceCharactor)
        RETURN c.name AS CHARACTOR
        ''', need_name = need_name
    )
    charactor_result_data = charactor_result.data()
    return charactor_result_data

#查找与特征有关的产品级信息
def find_product_with_charactor(tx, charactor_name):
    #执行Cypher查询来找出与特征有关的连接压缩机的产品级信息
    compress_product_result = tx.run(
        '''
        MATCH (i:InstanceCharactor {name:$charactor_name})<-[:has_capability]-(c:CompressorCompany)-[:has_instance]->(ic:InstanceCompressor)<-[:include]-(ai:AirCondition_Instance)
        RETURN ai.name AS PRODUCT
        ''', charactor_name = charactor_name
    )
    compress_product_data = compress_product_result.data()
    # 执行Cypher查询来找出与特征有关的连接电机的产品级信息
    electrical_machinery_product_result = tx.run(
        '''
        MATCH (i:InstanceCharactor {name:$charactor_name})<-[:has_capability]-(c:InstanceElectricalMachinery)<-[:include]-(ai:AirCondition_Instance)
        RETURN ai.name AS PRODUCT
        ''', charactor_name=charactor_name
    )
    electrical_machinery_product_data = electrical_machinery_product_result.data()
    # 执行Cypher查询来找出与特征有关的连接冷凝器的产品级信息
    cold_machinery_product_result = tx.run(
        '''
        MATCH (i:InstanceCharactor {name:$charactor_name})<-[:has_capability]-(c:InstanceColdMachinery)<-[:include]-(ai:AirCondition_Instance)
        RETURN ai.name AS PRODUCT
        ''', charactor_name=charactor_name
    )
    cold_machinery_product_data = cold_machinery_product_result.data()
    # 执行Cypher查询来找出与特征有关的连接蒸发器的产品级信息
    evaporator_product_result = tx.run(
        '''
        MATCH (i:InstanceCharactor {name:$charactor_name})<-[:has_capability]-(c:InstanceEvaporator)<-[:include]-(ai:AirCondition_Instance)
        RETURN ai.name AS PRODUCT
        ''', charactor_name=charactor_name
    )
    evaporator_product_data = evaporator_product_result.data()
    data = compress_product_data + electrical_machinery_product_data + cold_machinery_product_data + evaporator_product_data
    return data

#获取产品的颜色
def find_color_with_product(tx, single_product_plan_final):
    single_color_with_product = tx.run(
        '''
        MATCH (i:AirCondition_Instance{name:$single_product_plan_final})-[:include]->(c:InstanceColor)
        RETURN c.name AS ProductColor
        ''', single_product_plan_final = single_product_plan_final
    )
    color_with_product_data = single_color_with_product.data()
    return color_with_product_data

# 获取产品的厂家和型号
def find_company_with_product(tx, single_product_plan_final):
    single_company_with_product = tx.run(
        '''
        MATCH (i:AirCondition_Instance{name:$single_product_plan_final})<-[:has_instance]-(com:AirConditionType)
        RETURN com.name AS ProductCompany
        ''', single_product_plan_final = single_product_plan_final
    )
    company_with_product_data = single_company_with_product.data()
    return company_with_product_data

#获取产品价格
def find_price_with_product(tx, single_product_plan_final):
    single_price_with_product = tx.run(
        '''
        MATCH(a:AirCondition_Instance{name:$single_product_plan_final})
        RETURN a.price AS Price
        ''', single_product_plan_final = single_product_plan_final
    )
    price_with_product_data = single_price_with_product.data()
    return price_with_product_data

#获取产品链接
def find_herf_with_product(tx, single_product_plan_final):
    single_herf_with_product = tx.run(
        '''
        MATCH(a:AirCondition_Instance{name:$single_product_plan_final})
        RETURN a.herf AS Herf
        ''', single_product_plan_final = single_product_plan_final
    )
    herf_with_product_data = single_herf_with_product.data()
    return herf_with_product_data

# 将产品级组装方案的零部件信息扩充进来（压缩机）
def find_charactor_product_with_compressor(tx, single_product_plan_final):
    single_product_with_compressor = tx.run(
        '''
        MATCH (i:AirCondition_Instance{name:$single_product_plan_final})-[:include]->(ic:InstanceCompressor)
        RETURN ic.name AS ProductWithInstanceCompressor
        ''', single_product_plan_final = single_product_plan_final
    )
    product_with_compressor_data = single_product_with_compressor.data()
    return product_with_compressor_data


# 将产品级组装方案的零部件信息扩充进来（电机）
def find_charactor_product_with_electrical_machinery(tx, single_product_plan_final):
    single_product_with_electrical_machinery = tx.run(
        '''
        MATCH (i:AirCondition_Instance{name:$single_product_plan_final})-[:include]->(ie:InstanceElectricalMachinery)
        RETURN ie.name AS ProductWithInstanceElectricalMachinery
        ''', single_product_plan_final = single_product_plan_final
    )
    product_with_electrical_machinery_data = single_product_with_electrical_machinery.data()
    return product_with_electrical_machinery_data


# 将产品级组装方案的零部件信息扩充进来（冷凝器）
def find_charactor_product_with_cold_machinery(tx, single_product_plan_final):
    single_product_with_cold_machinery = tx.run(
        '''
        MATCH (i:AirCondition_Instance{name:$single_product_plan_final})-[:include]->(ic:InstanceColdMachinery)
        RETURN ic.name AS ProductWithInstanceColdMachinery
        ''', single_product_plan_final = single_product_plan_final
    )
    product_with_cold_machinery_data = single_product_with_cold_machinery.data()
    return product_with_cold_machinery_data

# 将产品级组装方案的零部件信息扩充进来（蒸发器）
def find_charactor_product_with_evapoartor(tx, single_product_plan_final):
    single_product_with_evapoartor = tx.run(
        '''
        MATCH (i:AirCondition_Instance{name:$single_product_plan_final})-[:include]->(ie:InstanceEvaporator)
        RETURN ie.name AS ProductWithInstanceEvaporator
        ''', single_product_plan_final = single_product_plan_final
    )
    product_with_evapoartor_data = single_product_with_evapoartor.data()
    return product_with_evapoartor_data

# 将产品级组装方案的零部件信息扩充进来（四通阀）
def find_charactor_product_with_valve(tx, single_product_plan_final):
    single_product_with_valve = tx.run(
        '''
        MATCH (i:AirCondition_Instance{name:$single_product_plan_final})-[:include]->(iv:InstanceValve)
        RETURN iv.name AS ProductWithInstanceValve
        ''', single_product_plan_final = single_product_plan_final
    )
    product_with_valve_data = single_product_with_valve.data()
    return product_with_valve_data


#查找与特征有关的压缩机厂商信息
def find_compressor_company_with_charactor(tx, charactor_name):
    #执行Cypher查询来找出与特征有关的压缩机厂商信息
    compress_company_result = tx.run(
        '''
        MATCH (i:InstanceCharactor {name:$charactor_name})<-[:has_capability]-(c:CompressorCompany)
        RETURN c.name AS CompressorCompany
        ''', charactor_name = charactor_name
    )
    data = compress_company_result.data()
    if not data:
        data.append({'CompressorCompany': '海立'})
    return data

#查找与特征有关的电机信息
def find_electrical_machinery_with_charactor(tx, charactor_name):
    #执行Cypher查询来找出与特征有关的电机信息
    electrical_machinery_result = tx.run(
        '''
        MATCH (i:InstanceCharactor {name:$charactor_name})<-[:has_capability]-(e:InstanceElectricalMachinery)
        RETURN e.name AS InstanceElectricalMachinery
        ''', charactor_name = charactor_name
    )
    data = electrical_machinery_result.data()
    if not data:
        #如果没有找到相匹配的电机，则返回默认值
        data.append({'InstanceElectricalMachinery': '48w交流电机'})
    return data

#查找与特征有关的冷凝器信息
def find_cold_machinery_with_charactor(tx, charactor_name):
    #执行Cypher查询来找出与特征有关的冷凝器信息
    cold_machinery_result = tx.run(
        '''
        MATCH (i:InstanceCharactor {name:$charactor_name})<-[:has_capability]-(c:InstanceColdMachinery)
        RETURN c.name AS InstanceColdMachinery
        ''', charactor_name = charactor_name
    )
    data = cold_machinery_result.data()
    if not data:
        #如果没有找到相匹配的冷凝器，则返回默认值
        data.append({'InstanceColdMachinery': '24组双排冷凝器'})
    return data

#查找与特征有关的蒸发器信息
def find_evaporator_with_charactor(tx, charactor_name):
    #执行Cypher查询来找出与特征有关的蒸发器信息
    evaporator_result = tx.run(
        '''
        MATCH (i:InstanceCharactor {name:$charactor_name})<-[:has_capability]-(e:InstanceEvaporator)
        RETURN e.name AS InstanceEvaporator
        ''', charactor_name = charactor_name
    )
    data = evaporator_result.data()
    if not data:
        #如果没有找到相匹配的蒸发器，则返回默认值
        data.append({'InstanceEvaporator': '34根5mm细铜管'})
    return data


def return_charactor_list(s):
    path = "/data/ices/liyuchen/newFinetune/output/liyuchen2"
    # 连接到Neo4j数据库
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
    with driver.session() as session:
        #执行查询
        '''
            在demo_output处运行微调后的大模型并给出结果，具体代码详见demo_output.py
        '''
        need_name = demo_output.demo_outputs(s)
        print("根据您的需求描述，您可能想要" + need_name + "需求的空调装配方案，基于此空调装配方案我们有如下特征与之对应：")
        charactor_name_list = session.read_transaction(find_charactor_with_need, need_name)
        for i in charactor_name_list:
            charactor_plan.append(i['CHARACTOR'])
        str_list = ",".join(charactor_plan)
        str_final = "根据您的需求描述，您可能想要" + need_name + "需求的空调装配方案，基于此空调装配方案我们有" + str_list +"特征与之对应，请问您需要哪种特征空调，直接输入：我想要XX特征空调装配方案即可"
        return str_final


def return_product_charactor(charactor_name):
    str_charactor_plan = "根据您的选择，您需要具有" + charactor_name + "特征的空调装配方案，对于厂家和类型您有什么样的需求，请输入：关于厂家和类型，我需要XX的空调\n"
    return str_charactor_plan

def return_company(company_name):
    str_company = "关于厂家和类型，您选择了" + company_name + "的空调，对于颜色您有什么样的需求，请输入：搭配颜色是XX空调\n"
    return str_company

def return_color(color):
    str_color = "关于颜色，您选择了" + color + "的空调，对于最高价格您有什么样的需求，请输入：关于购买空调的最高接受价格为XX元\n"
    return str_color

def return_maxprice(maxprice):
    str_max_price =  "关于最高价格，您选择了" + maxprice + "元，对于最低价格您有什么样的需求，请输入：关于购买空调的最低接受价格为XX元\n"
    return str_max_price

def return_lowprice(charactor_name, company_name, color, maxprice, lowprice):
    # 连接到Neo4j数据库
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
    with driver.session() as session:
        str_low_price = "关于最低价格，您选择了" + lowprice + "元。" + '\n' + "根据上述描述，为您推荐产品集以及可以替换的零部件级装配方案如下：\n"
        products = session.read_transaction(find_product_with_charactor, charactor_name)
        compressor_company_name = session.read_transaction(find_compressor_company_with_charactor, charactor_name)
        electrical_machinery_name = session.read_transaction(find_electrical_machinery_with_charactor, charactor_name)
        cold_machinery_name = session.read_transaction(find_cold_machinery_with_charactor, charactor_name)
        evaporator_name = session.read_transaction(find_evaporator_with_charactor, charactor_name)
        for product in products:
            products_plan.append(product['PRODUCT'])
        for cn in compressor_company_name:
            compressor_plan.append(cn['CompressorCompany'])
        for emn in electrical_machinery_name:
            electrical_machinery_plan.append(emn['InstanceElectricalMachinery'])
        for cmn in cold_machinery_name:
            cold_machinery_plan.append(cmn['InstanceColdMachinery'])
        for en in evaporator_name:
            evaporator_plan.append(en['InstanceEvaporator'])
        str_low_price = str_low_price + "产品级装配方案：\n"
        j = 1
        products_plan_final = set(products_plan)
        for p in products_plan_final:
            single_color_with_product = session.read_transaction(find_color_with_product, p)
            # print("颜色：" + single_color_with_product[0]['ProductColor'] + '\n')
            if single_color_with_product[0]['ProductColor'] != color:
                continue
            single_company_with_product = session.read_transaction(find_company_with_product, p)
            if single_company_with_product[0]['ProductCompany'] != company_name:
                continue
            single_price_with_product = session.read_transaction(find_price_with_product, p)
            if int(single_price_with_product[0]['Price']) > int(maxprice) or int(single_price_with_product[0]['Price']) < int(lowprice):
                continue
            single_herf_with_product = session.read_transaction(find_herf_with_product, p)
            print(single_herf_with_product[0]['Herf'])
            if single_herf_with_product[0]['Herf'] == '无':
                continue
            single_product_with_commpressor = session.read_transaction(find_charactor_product_with_compressor, p)
            single_product_with_electrical_machinery = session.read_transaction(find_charactor_product_with_electrical_machinery, p)
            single_product_with_cold_machinery = session.read_transaction(find_charactor_product_with_cold_machinery, p)
            single_product_with_evaporator = session.read_transaction(find_charactor_product_with_evapoartor, p)
            single_product_with_valve = session.read_transaction(find_charactor_product_with_valve, p)
            str_low_price = str_low_price + "推荐产品" + str(j) + "：" + p + '\n'
            # print("推荐产品" + str(j) + "：" + p)
            str_low_price =str_low_price + "该产品装配方案为:\n" +  "颜色：" + single_color_with_product[0]['ProductColor'] + '\n' + "价格：" + str(single_price_with_product[0]['Price']) + '\n' + "压缩机：" + single_product_with_commpressor[0]['ProductWithInstanceCompressor'] + '\n' + "电机：" + single_product_with_electrical_machinery[0]['ProductWithInstanceElectricalMachinery'] + '\n' + "冷凝器：" + single_product_with_cold_machinery[0]['ProductWithInstanceColdMachinery'] + '\n' + "蒸发器：" + single_product_with_evaporator[0]['ProductWithInstanceEvaporator'] + '\n' + "四通阀：" + single_product_with_valve[0]['ProductWithInstanceValve'] + '\n' + "链接：" +  single_herf_with_product[0]['Herf'] + '\n'
            # print("该产品装配方案为:\n" + "压缩机：" + single_product_with_commpressor[0]['ProductWithInstanceCompressor'] + '\n' + "电机：" + single_product_with_electrical_machinery[0]['ProductWithInstanceElectricalMachinery'] + '\n' + "冷凝器：" + single_product_with_cold_machinery[0]['ProductWithInstanceColdMachinery'] + '\n' + "蒸发器：" + single_product_with_evaporator[0]['ProductWithInstanceEvaporator'] + '\n' + "四通阀：" + single_product_with_valve[0]['ProductWithInstanceValve'])
            j = j + 1
            if j == 2:
                break
        # combinations = itertools.product(compressor_plan, electrical_machinery_plan, cold_machinery_plan, evaporator_plan)
        str_low_price = str_low_price + "零部件替换装配方案：\n" + "压缩机列表：\n" + '[' + ','.join(str(i) for i in compressor_plan) + ']' + "\n"
        str_low_price = str_low_price + "电机列表：\n" + '[' + ','.join(str(i) for i in electrical_machinery_plan) + ']' + "\n"
        str_low_price = str_low_price + "冷凝器列表：\n" + '[' + ','.join(str(i) for i in cold_machinery_plan) + ']' + "\n"
        str_low_price = str_low_price + "蒸发器列表：\n" + '[' + ','.join(str(i) for i in evaporator_plan) + ']' + "\n"
        # print("零部件替换装配方案：")
        # print("压缩机列表：")
        # print(compressor_plan)
        # print("电机列表：")
        # print(electrical_machinery_plan)
        # print("冷凝器列表：")
        # print(cold_machinery_plan)
        # print("蒸发器列表：")
        # print(evaporator_plan)
        
        return str_low_price



def main():
    path = "" #此处输入微调后大模型的路径 
    # 连接到Neo4j数据库
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
    with driver.session() as session:
        #执行查询
        '''
            在demo_output处运行微调后的大模型并给出结果，具体代码详见demo_output.py
        '''
        s = input("请输入：")
        need_name = demo_output.demo_outputs(s)
        print("根据您的需求描述，您可能想要" + need_name + "需求的空调装配方案，基于此空调装配方案我们有如下特征与之对应：")
        charactor_name_list = session.read_transaction(find_charactor_with_need, need_name)
        for i in charactor_name_list:
            charactor_plan.append(i['CHARACTOR'])
        print(charactor_plan)
        charactor_name = input("请选择具备哪一款特征的空调：")
        print("根据您的选择，您需要具有" + charactor_name + "特征的空调装配方案，产品级和零部件级的装配方案如下：")
        products = session.read_transaction(find_product_with_charactor, charactor_name)
        compressor_company_name = session.read_transaction(find_compressor_company_with_charactor, charactor_name)
        electrical_machinery_name = session.read_transaction(find_electrical_machinery_with_charactor, charactor_name)
        cold_machinery_name = session.read_transaction(find_cold_machinery_with_charactor, charactor_name)
        evaporator_name = session.read_transaction(find_evaporator_with_charactor, charactor_name)
        for product in products:
            products_plan.append(product['PRODUCT'])
        for cn in compressor_company_name:
            compressor_plan.append(cn['CompressorCompany'])
        for emn in electrical_machinery_name:
            electrical_machinery_plan.append(emn['InstanceElectricalMachinery'])
        for cmn in cold_machinery_name:
            cold_machinery_plan.append(cmn['InstanceColdMachinery'])
        for en in evaporator_name:
            evaporator_plan.append(en['InstanceEvaporator'])
        print("产品级装配方案：")
        j = 1
        products_plan_final = set(products_plan)
        for p in products_plan_final:
            single_product_with_commpressor = session.read_transaction(find_charactor_product_with_compressor, p)
            single_product_with_electrical_machinery = session.read_transaction(find_charactor_product_with_electrical_machinery, p)
            single_product_with_cold_machinery = session.read_transaction(find_charactor_product_with_cold_machinery, p)
            single_product_with_evaporator = session.read_transaction(find_charactor_product_with_evapoartor, p)
            single_product_with_valve = session.read_transaction(find_charactor_product_with_valve, p)
            print("推荐产品" + str(j) + "：" + p)
            print("该产品装配方案为:\n" + "压缩机：" + single_product_with_commpressor[0]['ProductWithInstanceCompressor'] + '\n' + "电机：" + single_product_with_electrical_machinery[0]['ProductWithInstanceElectricalMachinery'] + '\n' + "冷凝器：" + single_product_with_cold_machinery[0]['ProductWithInstanceColdMachinery'] + '\n' + "蒸发器：" + single_product_with_evaporator[0]['ProductWithInstanceEvaporator'] + '\n' + "四通阀：" + single_product_with_valve[0]['ProductWithInstanceValve'])
            j = j + 1
        # combinations = itertools.product(compressor_plan, electrical_machinery_plan, cold_machinery_plan, evaporator_plan)
        print("零部件替换装配方案：")
        print("压缩机列表：")
        print(compressor_plan)
        print("电机列表：")
        print(electrical_machinery_plan)
        print("冷凝器列表：")
        print(cold_machinery_plan)
        print("蒸发器列表：")
        print(evaporator_plan)
if __name__ == "__main__":
    main()