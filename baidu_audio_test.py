import os
import urllib.request
import urllib
import json
import base64

class BaiduRest:
    def __init__(self, cu_id, api_key, api_secert):
        # token认证的url
        self.token_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"
        # 语音合成的resturl
        #self.getvoice_url = "http://tsn.baidu.com/text2audio?tex=%s&lan=zh&cuid=%s&ctp=1&tok=%s"
        # 语音识别的resturl
        self.upvoice_url = 'http://vop.baidu.com/server_api'

        self.cu_id = cu_id
        self.getToken(api_key, api_secert)
        return

    def getToken(self, api_key, api_secert):
        # 1.获取token
        token_url = self.token_url % (api_key,api_secert)

        r_str = urllib.request.urlopen(token_url).read()
        token_data = json.loads(r_str.decode('utf-8'))
        self.token_str = token_data['access_token']
        #print(self.token_str)
        pass

    def getVoice(self, text, filename):
        # 2. 向Rest接口提交数据
        get_url = self.getvoice_url % (urllib.parse.quote(text), self.cu_id, self.token_str)

        voice_data = urllib.request.urlopen(get_url).read()
        # 3.处理返回数据
        voice_fp = open(filename,'wb+')
        voice_fp.write(voice_data)
        voice_fp.close()
        pass

    def getText(self, filename):
        # 2. 向Rest接口提交数据
        data = {}
        # 语音的一些参数
        data['format'] = 'wav'
        data['rate'] = 16000
        data['channel'] = 1
        data['cuid'] = self.cu_id
        data['token'] = self.token_str
        data['dev_pid'] = 1536
        wav_fp = open(filename,'rb')
        voice_data = wav_fp.read()
        data['len'] = len(voice_data)
        data['speech'] = base64.b64encode(voice_data).decode('utf-8')
        post_data = json.dumps(data)
        r_data = urllib.request.urlopen(self.upvoice_url,data=bytes(post_data,encoding="utf-8")).read()
        # 3.处理返回数据
        print(json.loads(r_data.decode('utf-8'))['result'])
        return json.loads(r_data.decode('utf-8'))['result']

if __name__ == "__main__":
    # 我的api_key,供大家测试用，在实际工程中请换成自己申请的应用的key和secert
    api_key = "DyQe7nOQGF2HNDUK3eNKa7HV"
    api_secert = "wmU7kZVEgs8rOZNK5TV4B4rdMZ5ygKWp"
    # 初始化
    bdr = BaiduRest("test_python", api_key, api_secert)
    # 语音文件存放目录
    dir = 'E:\\一贯机器人\\一贯机器人\\语音\\语音对比测试\\wav'

    for file in os.listdir(dir):
        if file.endswith(".wav"):
            try:
                audiofilename = '%s\\%s' % (dir, file)
                #语音识别
                result = bdr.getText(audiofilename)
            except Exception as err:
                print(err)
