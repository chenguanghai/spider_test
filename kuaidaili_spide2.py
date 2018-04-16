# coding:utf-8

import sys
import requests
import re
import time
from lxml import etree

reload(sys)
sys.setdefaultencoding('utf-8')

class KuaiDaiLISpider(object):
    """
    爬取快代理的免费代理ip，然后自己用爬取到的ip访问百度成功保留
    """
    def __init__(self):
        """初始化请求网址，以及正则表达式"""
        self.url="https://www.kuaidaili.com/free/inha/"
        self.check_url='"http://www.baidu.com/"'
        self.headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}
        self.xpath="//td[@data-title='IP']/text()|//td[@data-title='PORT']/text()"
        self.start_page=int(raw_input("请输入从多少页开始爬取:"))
        self.end_page=int(raw_input("请输入爬到多少页结束:"))
        self.proxies={"http": "maozhaojun:ntkn0npx@114.67.224.167:16819"}
    def send_request(self,url,query={}):
        """发送请求，返回响应"""
        print url
        response=requests.get(url,params=query,proxies=self.proxies,headers=self.headers)
        return response

    def parse_page(self,response):
        """提取每一页的Ip和端口并返回"""
        html_obj = etree.HTML(response)
        ip_ports=html_obj.xpath(self.xpath)
        return ip_ports

    def save_ip(self,proxies):
        """保存可以用的Ip到文件夹"""
        with open('ip_port.txt','a') as f:
            f.write('***************************')
            f.write(proxies)
            f.write('\n')

    def check_ip(self,ip_ports):
        """通过访问百度页面测试代理服务器是否有效，有效则返回，无效不返回"""
        # 用于将获得的数据[ip,port,ip,port....]转换为[(prot,ip),(port,ip)]更方便后面使用
        list_ip=[]
        while True:
            if not len(ip_ports):
                break
            a=ip_ports.pop()
            b=ip_ports.pop()
            ip_port_tuple=(a,b)
            list_ip.append(ip_port_tuple)

        # 用于存放可以使用的Ip
        can_use=[]
        for li in list_ip:
            #根据协议类型，选择不同的代理
            proxy = {"http": "http://%s:%s"%(li[1],li[0])}
            print proxy
            try:
                response = requests.get("http://www.baidu.com", proxies=proxy, headers=self.headers,timeout=1)
            except Exception as e :
                #不能使用的ip
                print '【ip:%s,不能使用】'%li[1]
                continue
            else:
                #能使用的ip
                html = response.content
                print html
                can_use.append(li)
            #返回所有能使用的ip
            return can_use




    def main(self):
        """调度器"""
        #1.拼接url,发送请求
        for i in range(self.start_page,self.end_page+1):
            print '【Info】:当前爬取第'+str(i)+'页ip....'
            url=self.url+str(i)+'/'
            # 获取html二进制内容
            html=self.send_request(url).content
            ip_ports=self.parse_page(html)
            proxies=self.check_ip(ip_ports)
            if proxies:
                self.save_ip(str(proxies))






if __name__ == '__main__':
    kdl=KuaiDaiLISpider()
    kdl.main()

