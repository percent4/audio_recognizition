#-*- coding: utf-8 -*-

import time
import hashlib
import base64
import urllib
import urllib.parse
import urllib.request
import os


# 讯飞的语音识别地址
URL = "http://api.xfyun.cn/v1/service/v1/iat"
# 我的api_key,供大家测试用，在实际工程中请换成自己申请的应用的APPID和API_KEY
APPID = "5b45d5d1"
API_KEY = "3dc216cce6add574caf49935c5b90e99"

# 获取请求头
def getHeader(aue, engineType):
    curTime = str(int(time.time()))
    param = "{\"aue\":\""+aue+"\""+",\"engine_type\":\"" + engineType + "\"}"
    paramBase64 = base64.b64encode(bytes(param, "utf-8"))

    m2 = hashlib.md5()
    m2.update(bytes(API_KEY + curTime, "utf-8") + paramBase64)
    checkSum = m2.hexdigest()

    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }

    return header

# 打开音频文件
def getBody(filepath):
    binfile = open(filepath, 'rb')
    data = {'audio': base64.b64encode(binfile.read())}
    return data

def iflywebapi_res(audioFilePath):
    aue = "raw" # 音频编码
    engineType = "sms16k" # 普通话
    # 音频文件，根据自己的需求修改，最好是wav格式
    #audioFilePath ="E:\\1-1.wav"  # 识别结果：“你好。”
    #r = requests.post(URL, headers=getHeader(aue, engineType), data=getBody(audioFilePath))
    data = urllib.parse.urlencode(getBody(audioFilePath)).encode('utf-8')
    request = urllib.request.Request(url=URL, headers=getHeader(aue, engineType), data=data, method="POST")
    response = urllib.request.urlopen(request)
    # 响应结果, code为0表示成功
    print(response.read().decode('utf-8'))

def main():
    dir = "E:\一贯机器人\一贯机器人\语音\语音对比测试\wav"
    for file in os.listdir(dir):
        if file.endswith(".wav"):
            try:
                audioFilePath = "%s\\%s"%(dir, file)
                iflywebapi_res(audioFilePath)
            except urllib.error.URLError as err:
                print('Network problem.')

main()