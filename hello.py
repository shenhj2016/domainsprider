#encoding=utf-8
import Queue
import random
import sys
import time
import ssl
import json
import urllib2
import logging
# pip
import MySQLdb
from pinyin.pinyin import PinYin
import requests

from proxy import proxy

reload(sys)
sys.setdefaultencoding('utf-8')

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT)
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

class DataException(RuntimeError):
    def __init__(self, arg):
        self.args = arg

def getUrl(domain):
    l = time.time();
    url = "https://whois.bj.baidubce.com/whois?callback=jQuery110205128862345316428_" + \
    str(l - 1000 * 60) + \
    "&ie=utf-8&oe=utf-8&format=javascript&domain=" + \
    domain + \
    "&_=" + str(l);
    return url


def sendDomain(domain,proxies):
    # 2. 表示忽略未经核实的SSL证书认证
    context = ssl._create_unverified_context()
    request = urllib2.Request(getUrl(domain), headers=headers)
    # 以下三段设置代理
    proxy_s = urllib2.ProxyHandler(proxies)
    opener = urllib2.build_opener(proxy_s)
    urllib2.install_opener(opener)

    # 3. 在urlopen()方法里 指明添加 context 参数
    response = urllib2.urlopen(request, context=context)
    res = response.read()
    logging.info(res)
    str = res[res.index("({") + 1: res.index(");")]
    data = json.loads(str, encoding="utf-8").get("data")
    if data == None :
        raise DataException("data is None")
    data["expirationDate"] = data.get("expirationDate").replace("年", "-").replace("月", "-").replace("日", "")
    data["registrationDate"] = data.get("registrationDate").replace("年", "-").replace("月", "-").replace("日", "")
    logging.info(data)
    return data

def findByDomain(domain):
    sql = "SELECT * FROM `DOMAIN` WHERE `domain` = '%s' " % (domain)
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    if len(results) > 0:
        return True
    else:
        return False


def addDoamin(data):
    sql = "INSERT INTO `DOMAIN`(`domain`, `status`, `queryTime`, `registrant`, `registrationDate`, `expirationDate`) \
           VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % \
          (data.get("domain"),data.get("status"), data.get("queryTime"), data.get("registrant"), data.get("registrationDate"), data.get("expirationDate"))
    try:
        cursor.execute(sql)
    except Exception as e:
        raise e
    return cursor.fetchone()


def updateDomain(data):
    sql = "UPDATE `DOMAIN` SET `status`= '%s', `queryTime` = '%s', `registrant` = '%s', `registrationDate` = '%s', `expirationDate` = '%s' where `domain` = '%s'" % \
          (data.get("status"), data.get("queryTime"), data.get("registrant"),data.get("registrationDate"), data.get("expirationDate"),data.get("domain"))
    try:
        cursor.execute(sql)
    except Exception as e:
        raise e
    return cursor.fetchone()



def init():
    global file, en, test, DB, cursor,ip_queue
    en = int(sys.argv[2])
    if en > 0:  # 英文需要传0，中文需要传1
        test = PinYin()
        test.load_word()
    # 打开数据库连接
    DB = MySQLdb.connect("47.99.121.124", "root", "123456", "test", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = DB.cursor()
    DB.autocommit(True)
    # 获取代理
    ip_queue = proxy.get_all_ip()


if __name__ == '__main__':
    context = ssl._create_unverified_context()
    # 以下三段设置代理
    proxy_s = urllib2.ProxyHandler({"http":"http://36.48.73.16:80"})
    opener = urllib2.build_opener(proxy_s)
    urllib2.install_opener(opener)
    request = urllib2.Request("http://shenhj.frp.ngarihealth.com/welcome", headers=headers)

    # 3. 在urlopen()方法里 指明添加 context 参数
    response = urllib2.urlopen(request, context=context)
    res = response.read()
    print res
    # init()
    # # 但是每次都这么写实在太繁琐，所以，Python引入了with语句来自动帮我们调用close()方法
    # with open(sys.argv[1], 'r') as f:
    #     for line in f.readlines():
    #         try:
    #             term = line.strip()
    #             if en > 0:# 英文需要传0，中文需要传1
    #                 if len(term) > 15:
    #                     continue
    #                 term = test.hanzi2pinyin_split(term,"")
    #             else:
    #                 if len(term) > 9:
    #                     continue
    #             time.sleep(3)
    #             domain = term + ".com"
    #             domain = domain.encode("utf-8")
    #             proxy_ip = ip_queue.get()
    #             proxies = {'http': proxy_ip}
    #             print proxies
    #             data = sendDomain(domain=domain,proxies=proxies)
    #             if findByDomain(domain):
    #                 updateDomain(data)
    #             else:
    #                 addResult = addDoamin(data)
    #         except DataException as dataerror:
    #             logging.exception(dataerror.message)
    #             try:
    #                 time.sleep(3)
    #                 proxy_ip = ip_queue.get()
    #                 proxies = {'http': proxy_ip}
    #                 data = sendDomain(domain=domain,proxies=proxies)
    #                 if findByDomain(domain):
    #                     updateDomain(data)
    #                 else:
    #                     addResult = addDoamin(data)
    #             except Exception as e:
    #                 logging.exception(e)
    #                 continue
    #         except Exception as e:
    #             logging.exception(e)
    # DB.close()

