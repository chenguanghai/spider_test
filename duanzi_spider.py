# coding:utf-8
import base64
from Queue import Queue
import sys
import threading

import re

import pymongo
from pymongo import MongoClient

reload(sys)
sys.setdefaultencoding('utf-8')
import requests
from lxml import etree
import random
from redis.client import StrictRedis

HEADERS_USER=[
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3"
        ]

# //a[@class='title'and @title]/@href    xpath提取规则
#  http://www.neihanpa.com/article/index_2.html  第二页
class DuanZiSpider(object):
    """内涵吧爬虫：爬取段子以及段子中的图片"""

    def __init__(self):
        """初始化对象"""
        self.base_url = 'http://www.neihanpa.com/article'
        self.start_index = int(raw_input('请输入开始页:'))
        self.end_index = int(raw_input('请输入结束页:'))
        self.headers = HEADERS_USER
        # 创建队列存储页面
        self.queue=Queue(int(self.end_index-self.start_index))
        #  创建匹配规则获取urls
        self.xpath_urls='//a[@class="title"and @title]/@href '
        # 创建Redis链接
        self.redis_cli=StrictRedis('127.0.0.1')

    def send_request(self, url, query={}):
        """发送请求"""
        print '线程: %s ，正在爬取页面: %s' % (threading.current_thread(),url)
        s = requests.session()
        s.keep_alive = False
        response=requests.get(url, params=query,headers={'User-Agent': random.choice(self.headers)})
        return response.content

    def  __open(self):
        self.client = pymongo.MongoClient(host="127.0.0.1", port=27017)
        self.db = self.client.test
        self.collection = self.db.neihan


    def save_content(self,html):
        """保存内容到mangodb"""
        html_obj=etree.HTML(html)
        # 找到段子文本
        content_str=''
        contents=html_obj.xpath('//div[@class="detail"]//p/text()')
        for co in contents:
            content_str+=(co+'\n')
        # 段子标题
        title=html_obj.xpath('//h1[@class="title"]/text()')

        # 段子图片保存在本地，返回名字，保存路径到mangodb
        img=html_obj.xpath('//div[@class="detail"]//img/@src')
        try:
            url=img[0]
        except Exception as e :
            print e
            return
        try:
            file_name=re.search(r'/(\w+\.png)$',url).group(1)
        except Exception as e:
            file_name=base64.b16encode('dadasda')+'.png'
            print "图片名称提取失败"
        response=self.send_request(url)
        with open(r'd:/neihan/images/'+file_name,'wb') as f :
            f.write(response)

        self.__open()
        item_list={}
        item_list['title']=title[0]
        item_list['img_path']=url
        item_list['content']=content_str
        print "[INFO] 正在写入MongoDB"
        print self.client
        try:
            self.collection.insert(item_list)
            print "[INFO] 写入成功!"
        except Exception as e :
            print '写入mongodb失败'


    def parse_index_page(self,html):
        """处理抓取url页面内容"""
        html_obj = etree.HTML(html)
        urls = html_obj.xpath(self.xpath_urls)
        print urls
        # 抓取到的url存入Redis
        for url in urls:
            self.redis_cli.lpush('urls',url)
            # print '保存:%s,ok'%url

    def do_job(self):
        """爬虫开始工作"""
        while True:
            i=self.queue.get()
            # 执行任务
            url = self.base_url + '/index_' + str(i) + '.html'
            html = self.send_request(url)
            self.parse_index_page(html)


            while True:
                # 从Redis获取url爬取
                url_detail=self.redis_cli.rpop('urls')
                if not url_detail:
                    break
                detail_url="http://www.neihanpa.com"+url_detail
                detail_html=self.send_request(detail_url)
                self.save_content(detail_html)

            # 每执行完一个任务通知队列
            self.queue.task_done()

    def main(self):
        # 创建9个线程的线程池
        for _ in range(1, 10):
            t = threading.Thread(target=duanzi.do_job)
            # 设置成守护线程，主线程退出，所有线程也会挂掉
            t.daemon = True
            # 开启线程
            t.start()
        # 循环获取页面，加入到队列



if __name__ == '__main__':
    duanzi = DuanZiSpider()
    duanzi.main()
    for i in range(duanzi.start_index, duanzi.end_index + 1):
        print i
        duanzi.queue.put(i)

    duanzi.queue.join()


"""
    爬取内涵段子：
    1.根据输入的爬取起，止页获取爬取的总页数，存入队列，加锁
    2.多线程获取锁从队列取出爬取页面的页码
    3.获取页面信息解析出需要的段子具体的url地址，存入Redis加锁lpush(){'dunaziurl':['url1','url2',...]}，
    4.从Redis读取rpop()需要爬取的段子url地址，（Redis单个客户端读取数据不会出现数据错误因为Redis就是单进程单线程，只要在多个客户端同时操作一个key时也很难出现并发数据错误问题）
    5.根据url获取页面段子详情，保存图片，返回图片路径
    6.提取需要的数据字典{'title':'','content':'','imgurl':''}，将数据保存到MongoDB
"""