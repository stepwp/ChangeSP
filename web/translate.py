"""网页翻译接口"""
import os
import sys
import uuid
import random
import requests
from hashlib import md5


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.config import cfg


def bing_translate(texts, to='zh-Hans'):
    """使用Bing翻译文本（默认翻译为简体中文）"""
    api_url = "https://api.cognitive.microsofttranslator.com/translate"
    params = {'api-version': '3.0', 'to': to}
    headers = {
        'Ocp-Apim-Subscription-Key': cfg.Translate.bing_key,
        'Ocp-Apim-Subscription-Region': cfg.Translate.bing_region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    body = [{'text': texts}]
    # https://docs.microsoft.com/zh-cn/azure/cognitive-services/translator/reference/v3-0-reference#errors
    request = requests.post(api_url, params=params, headers=headers, json=body)
    response = request.json()

    return response[0]['translations']


def baidu_translate(texts, to='zh'):
    """使用百度翻译文本（默认翻译为简体中文）"""
    api_url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    appid = cfg.Translate.baidu_appid
    appkey = cfg.Translate.baidu_key
    salt = random.randint(0, 0x7FFFFFFF)
    sign_input = appid + texts + str(salt) + appkey
    sign = md5(sign_input.encode('utf-8')).hexdigest()
    payload = {'appid': appid, 'q': texts, 'from': 'auto', 'to': to, 'salt': salt, 'sign': sign}
    r = requests.post(api_url, params=payload, headers=headers)
    result = r.json()
    return result


if __name__ == "__main__":
    print(baidu_translate('Hello world~'))