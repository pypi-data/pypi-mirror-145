from operator import mod
import requests
import json
import matplotlib.pyplot as plt
import numpy as np
import os


def get_model_path():
    return os.path.dirname(__file__)
def get_loss(dc,ac_lower,ac_upper,freq_lower,freq_upper,model,calc_type):
    """计算损耗

    Args:
        dc (A): 直流电流
        ac_lower (A): 纹波pk-pk的最大值
        ac_upper (A): 纹波pk-pk的最小值
        freq_lower (MHz): 频率的最小值
        freq_upper (MHz): 频率的最大值
        model (model): 参数模型
        calc_type(str): Frequency|Ripple
    Returns:
        list:分别是0:电流ripple，1：交流损耗,2:直流损耗
    """
    _url = 'https://www.coilcraft.com/api/partssearch/explore-losses'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Mobile Safari/537.36',
        'request-context':'appId=cid-v1:b8de02ec-3510-4f92-b94d-04ab30614bc6',
        'accept':'application/json, text/plain, */*',
        'content-type':'application/json;charset=UTF-8',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'zh-CN,zh;q=0.9'
    }
    if(freq_upper<freq_lower):
        print("Check frequency value")
        return
    if(ac_upper<ac_lower):
        print("Check ripple value")
    payload ={
        "ExploreLossesInputModel":{
            "Frequency":{
                "Lower":freq_lower,
                "Upper":freq_upper
            },
            "RippleCurrent":{
                "Lower":ac_lower,
                "Upper":ac_upper,
                "UnitString":"A"
            },
            "CurrentIDC":dc,
            "AmbientTemperature":25,
            "Interval":10,
            "GraphType":calc_type
        },
        "LossCalculationData":model
    }
    x = requests.post(_url, data =json.dumps(payload),headers=headers)
    data = json.loads(x.text)
    data = data['LossCalculationData'][0]['LossCalculations']
    x_val = []
    ac_loss_val = np.array([])
    dc_loss_val = np.array([])
    temp_val = np.array([])

    for item in data:
        x_val.append(item['XAxis'])
        ac_loss_val = np.append(ac_loss_val,item['ACLoss'])
        dc_loss_val = np.append(dc_loss_val,item['DCLoss'])
        temp_val    = np.append(temp_val,item['PartTemperature'])
    return [x_val,ac_loss_val,dc_loss_val,temp_val]

def get_loss_by_ripple(part_num,dc,ac_lower,ac_upper,freq):
    """固定频率，计算损耗

    Args:
        dc (A): 直流电流
        ac_lower (A): 纹波pk-pk的最大值
        ac_upper (A): 纹波pk-pk的最小值
        model (model): 参数模型
        freq (MHz): 频率的最小值
    Returns:
        list:分别是0:电流ripple，1：交流损耗,2:直流损耗
    """
    # print(get_model_path())
    with open(get_model_path()+f'/model/{part_num}.txt','r') as f:
        model = f.read()
        # print(model)
    return get_loss(dc,ac_lower,ac_upper,freq,freq,[json.loads(model)],"Ripple")
def get_loss_by_frequency(part_num,dc,ac,freq_lower,freq_upper):
    """固定纹波量，计算损耗

    Args:
        dc (A): 直流电流
        ac (A): 纹波pk-pk的最大值
        model (model): 参数模型
        freq_lower (MHz): 频率的最小值
        freq_upper (MHz): 频率的最大值
    Returns:
        list:分别是0:电流ripple，1：交流损耗,2:直流损耗
    """
    with open(get_model_path()+f'/model/{part_num}.txt','r') as f:
        model = f.read()
        # print(model)
    return get_loss(dc,ac,ac,freq_lower,freq_upper,[json.loads(model)],"Frequency")

if __name__ =='__main__':
    with open('./model/XGL6060-122.txt','r') as f:
        model = f.read()
    # print(type(model))
    data = get_loss_by_ripple(1,0,1,1,[json.loads(model)])
    plt.plot(data[0],data[1]+data[2])
    plt.show()    