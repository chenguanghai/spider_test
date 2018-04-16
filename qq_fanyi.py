# coding:utf-8
import json
import sys

import time
import urllib
import urllib2

reload(sys)
sys.setdefaultencoding('utf-8')

"""
    需求:调用腾讯翻译接口实现翻译功能
    目标网址：http://fanyi.qq.com/api/translate
    请求方式:post
    请求头：copy

"""
# 1.构建url
url="http://fanyi.qq.com/api/translate"

# 2.构建请求头,请求头中的content-length：需要自动改变
headers={
    "Accept":" application/json, text/javascript, */*; q=0.01",
    "Accept-Language":" zh-CN,zh;q=0.9",
    "Connection":" keep-alive",
    "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie":" fy_guid=5b0c027e-66b7-4cfb-8210-8293d520391d; pgv_info=ssid=s220663073; ts_last=fanyi.qq.com/; ts_refer=www.baidu.com/link; pgv_pvid=6402727363; ts_uid=2703521484; qtv=593385a241b91739; qtk=3Sl/zSqS/DD+k8KNjl1sTrK6oc/axn+DARxYqQUbXr5LnFe2QWgryDQCqmQmpZTk07cZzbJ3j+mE3uuRGFHJhuWzWxZiPcShdg6i1o04BJfT+hWLMaLH8rFsDi1CPEc3SLe2iIWo6+xwfCka4cE8Gg==; openCount=2",
    "Host":" fanyi.qq.com",
    "Origin":" http://fanyi.qq.com",
    "Referer":" http://fanyi.qq.com/",
    "User-Agent":" Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    "X-Requested-With":" XMLHttpRequest",
}
# 3.构建请求参数   1523691748254.0
#                  1523690882505
params={
    "source":"auto",
    "target":"auto",
    "sourceText":raw_input("请输入要翻译的内容:"),
    "sessionUuid":"translate_uuid"+str(int(time.time()*1000)),
}
data=urllib.urlencode(params)
# 4.发送请求
request=urllib2.Request(url,data,headers)
request.add_header('Content-Length',len(data))
# 5.得到响应
response=urllib2.urlopen(request)
res=response.read()
dict_obj = json.loads(res)
print(dict_obj['translate']['records'][0]['targetText'])