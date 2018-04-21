# coding:utf-8

import sys

from multiprocessing import Pool
import requests
import time

reload(sys)
sys.setdefaultencoding('utf-8')
from pymongo import MongoClient
from random import choice
from bs4 import BeautifulSoup

"""
    多线程，随机代理ip，随机user-agent爬取腾讯招聘网
"""

#1.测试自己的代理Ip是否有用，没用就删除Ip 测试网站：http://www.neihanpa.com/
# mongodb链接
client=MongoClient('127.0.0.1',port=27017)

db=client.test
conn=db.tencent

#url
BASE_URL='https://hr.tencent.com/position.php'
#请求头
HEADERS_USER=[
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3"
        ]
#代理服务器
PROXIES=[{'https':'maozhaojun:ntkn0npx@114.67.224.167:16819'},{'http':'120.76.79.24:80'}]
# 发送请求的方法
def send_request(url,params={},i=0):
    print '【info】正在发送请求...'
    try:
        response=requests.get(url=url,params=params,proxies=choice(PROXIES),headers={'User-Agent':choice(HEADERS_USER)})
        # 调用处理页面的方法
        dispose_page(response.content)
    except Exception as e :
        i+=1
        if i==3:
            print '3次请求失败！'
            return
        else:
            print '【info】请求失败，正在重发请求第%d次：%s'%(i,str(e))
            send_request(url,params,i=i)


def dispose_page(html):
    """提取需要的数据，保存"""
    soup=BeautifulSoup(html,'lxml')
    #获取十个职位的节点列表
    node_list=soup.select('.even,.odd')
    #定义空字典保存数据
    for node in node_list:
        item={}
        item['职位名称'] = node.select('td a')[0].get_text()
        item['职位链接'] = "https://hr.tencent.com/"+ node.select('td a')[0].get('href')
        item['职位类别'] = node.select('td')[1].get_text()
        item['需要人数'] = node.select('td')[2].get_text()
        item['工作地点'] = node.select('td')[3].get_text()
        item['发布时间'] = node.select('td')[4].get_text()
        conn.insert(item)

if __name__ == '__main__':
    # 开启多进程
    start=int(raw_input('请输入开始页：'))
    end=int(raw_input('请输入结束页：'))
    # １创建进程池 Pool(参数是表示工作进程的数量)
    pool = Pool(10)
    for i in range(start,end+1):
        # ２添加任务到进程池中
        num=(i-1)*10
        params={'start':num}
        pool.apply_async(func=send_request, args=(BASE_URL,params))
        time.sleep(1)

    # ３　关闭进程池  －－不允许再添加新的任务了
    pool.close()

    # ４　等待所有任务执行完成  tixing:主进程一旦退出　进程池中所有的工作进程全部退出
    pool.join()


