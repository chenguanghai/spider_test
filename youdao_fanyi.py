# coding:utf-8
import json
import random
import sys
import urllib
import urllib2
import hashlib

import time

reload(sys)
sys.setdefaultencoding('utf-8')

# 1.构建url   http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule
url="http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
# 2.构建请求头
headers={
    "Accept":" application/json, text/javascript, */*; q=0.01",
    "Accept-Language":" zh-CN,zh;q=0.9",
    "Connection":" keep-alive",
    # "Content-Length":" 335",
    "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie":" OUTFOX_SEARCH_USER_ID=-45819934@10.168.8.61; JSESSIONID=aaaJSJxPKCKBHcyGKpdlw; OUTFOX_SEARCH_USER_ID_NCOO=1811417338.2702374; ___rl__test__cookies=1523694124275",
    "Host":" fanyi.youdao.com",
    "Origin":" http://fanyi.youdao.com",
    "Referer":" http://fanyi.youdao.com/",
    "User-Agent":" Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    "X-Requested-With":" XMLHttpRequest",
    }

#3.构建查询字典
n=raw_input("请输入需要翻译的内容:")
S="fanyideskweb"
r=str(int(time.time()*1000)+random.randint(0,10))
D = "ebSeFb%=XZ%T[KZ)c(sy!"
sign=hashlib.md5(S+n+r+D).hexdigest()      #md5(S + n + r + D)    从js中找到
params={
    "i":n,  # n
    "from":"AUTO",
    "to":"AUTO",
    "smartresult":"dict",
    "client":S,   # S
    "salt":r,   # r
    "sign":sign,
    "doctype":"json",
    "version":"2.1",
    "keyfrom":"fanyi.web",
    "action":"FY_BY_CLICKBUTTION",
    "typoResult":"false",
}
data=urllib.urlencode(params)
# 4.发送请求
request=urllib2.Request(url,data,headers)
request.add_header('Content-Length',len(data))
response=urllib2.urlopen(request)
# 5.获取响应
res=json.loads(response.read())
ret=res["translateResult"][0][0]['tgt']
print ret