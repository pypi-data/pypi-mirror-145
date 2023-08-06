#!/usr/bin/python3
# -*- coding: utf-8 -*-

#Version 2022.1
#Author:SunnyLi

import requests,requests_toolbelt,urllib3,removebg,ISS_Info,PIL,base64

def youdao_translate_AUTO(string):
    original_str = string
    stringdata = {
        'doctype': 'json',
        'type': 'AUTO',
        'i': original_str
    }
    url = "http://fanyi.youdao.com/translate"
    try:
        r = requests.get(url, params=stringdata)
        if r.status_code == 200:
            result = r.json()
            translate_result = result['translateResult'][0][0]["tgt"]
            return translate_result
    except:
        return "Error"

def baidu_OCR(apiKey,secretKey,imagePath):
    def getToken(apiKey,secretKey):
        getTokenUrl = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+apiKey+'&client_secret='+secretKey
        response = requests.get(getTokenUrl)
        data = response.json()
        token = data.get('access_token')
        return token
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/webimage'
    with open(imagePath,'rb') as f:
        image = f.read()
    b64Image = base64.b64encode(image)
    params = {'access_token': getToken(apiKey,secretKey)}
    data = {'image': b64Image}
    response = requests.post(url,params=params,data=data)
    content = response.json()
    result = content['words_result']
    result_list = []
    for i in range(len(result)):
        result_list.append(result[i]['words'])
    return result_list

if __name__ == "__main__":
	print("Please use XYZRequest as a module, thanks.")
	print("请将XYZRequest作为模块使用，谢谢")
	exit()