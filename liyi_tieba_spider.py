# coding:utf-8
import urllib
import urllib2
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# https://tieba.baidu.com/f?kw=%E6%9D%8E%E6%AF%85
# &pn=0,&pn=50,&pn=100 每页的贴子数量  pn=(page-1)*50
BASE_URL = 'https://tieba.baidu.com/f?'

def save_html(response,file_name):
    with open('./spider_files/tieba/'+file_name,'w') as f:
        f.write(response)

def send_request(tieba_name,page):
    """
    :param tieba_name 要爬取的贴吧名字
    :param pn 要爬取的页数
    :return: response 
    """
    # 1、构建请求头
    headers={
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "BAIDUID=4FFC242A9168D67A772F6A9C8DD6FCAD:FG=1; BIDUPSID=4FFC242A9168D67A772F6A9C8DD6FCAD; PSTM=1523613115; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=1464_19036_21103_26182_22075; TIEBAUID=cb23caae14130a0d384a57f1; TIEBA_USERTYPE=7bc17a41cfc710bc640d8911; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1523614836; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1523615019; PSINO=7",
        "Host": "tieba.baidu.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    }
    # 2、构建url
    query = {
        'kw': tieba_name,
        'pn': page*50
    }
    query_str = urllib.urlencode(query=query)
    url = BASE_URL + query_str
    request=urllib2.Request(url,headers=headers)
    # 3、发送请求
    try:
        response=urllib2.urlopen(request)
        response = response.read()
        return response
    except Ellipsis as e:
        print e
        return ''

if __name__ == '__main__':
    tieba_name=raw_input('请输入要爬取的贴吧名：')
    tieba_name=tieba_name.encode('gbk')
    page = int(raw_input('请输入要爬取的页数：'))
    for p in range(1, page + 1):
        print '正在爬取【%s】吧，当前爬取%d页' % (tieba_name, p)
        response=send_request(tieba_name,p)
        file_name=tieba_name+str(p)+'.html'
        save_html(response,file_name)
