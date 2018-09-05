#coding:utf-8
'''
#1.对于普通网站进行爬虫
import requests
from bs4 import BeautifulSoup
url = "http://news.qq.com/"
wbdata = requests.get(url).text
soup = BeautifulSoup(wbdata,'lxml')
news_titles = soup.select("div.text > em.f14 > a.linkto")

for n in news_titles:
    title = n.get_text()
    link = n.get("href")
    data = {
        '标题':title,
        '链接':link
    }
    print (data)
'''

'''
#2..对于用js网页加载的网站进行爬虫
import requests
import  json

url = 'http://www.toutiao.com/api/pc/focus/'
wbdata = requests.get(url).text

data = json.loads(wbdata)
news = data['data']['pc_feed_focus']

for n in news:
    title = n['title']
    img_url = n['image_url']
    url = n['media_url']
    print(url,title,img_url)
'''

'''
#3.多进程高并发对网站进行爬虫
import requests
from bs4 import BeautifulSoup
import re

url = 'https://sou.zhaopin.com/jobs/searchresult.ashx?jl=广州&kw=python&sm=0&p=1'
wbdata = requests.get(url).content
soup = BeautifulSoup(wbdata,'lxml')

items = soup.select("div#newlist_list_content_table > table")
count = len(items) - 1
#print(count) #输出一页有多少个职位

job_count = re.findall(r"共<em>(.*?)</em>个职位满足条件",str(soup))[0]
pages = (int(job_count) // count) + 1
#print(pages)   #输出有多少页



import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool

def get_zhaopin(page):
    url = 'https://sou.zhaopin.com/jobs/searchresult.ashx?jl=广州&kw=python&sm=0&p={0}'.format(page)
    print("第{0}页".format(page))
    wbdata = requests.get(url).content
    soup = BeautifulSoup(wbdata, 'lxml')

    job_name = soup.select("table.newlist > tr > td.zwmc > div > a")
    salarys = soup.select("table.newlist > tr > td.zwyx")
    locations = soup.select("table.newlist > tr > td.gzdd")
    companys = soup.select("table.newlist > tr > td.gsmc")
    times = soup.select("table.newlist > tr > td.gxsj > span")


    for name, salary, location, company, time in zip(job_name, salarys, locations, companys, times):
        data = {
            'name': name.get_text(),
            'salary': salary.get_text(),
            'location': location.get_text(),
            'company': company.get_text(),
            'time': time.get_text(),
        }
        print(data)

if __name__ == '__main__':
    pool = Pool(processes=6)
    pool.map_async(get_zhaopin, range(1, pages+1))
    pool.close()
    pool.join()
'''

'''
#4.使用Selenium--以抓取QQ空间好友说说
from bs4 import BeautifulSoup
from selenium import webdriver
import time

driver = webdriver.PhantomJS(executable_path="F:\\phantomjs浏览器\\phantomjs_339f7.exe")
driver.maximize_window()

def get_shuoshuo(qq):
    driver.get('http://user.qzone.qq.com/{}/311'.format(qq))
    time.sleep(5)
    try:
        driver.find_element_by_id('login_div')
        a = True
    except:
        a = False
    if a ==True:
        driver.switch_to.frame('login_frame')
        driver.find_element_by_id('switcher_plogin').click()
        driver.find_element_by_id('u').clear()  # 选择用户名框
        driver.find_element_by_id('u').send_keys('346408611')
        driver.find_element_by_id('p').clear()
        driver.find_element_by_id('p').send_keys('a060812251473')
        driver.find_element_by_id('login_button').click()
        time.sleep(3)
    driver.implicitly_wait(3)
    try:
        driver.find_element_by_id('QM_OwnerInfo_Icon')
        b = True
    except:
        b = False
    if b == True:
        driver.switch_to.frame('app_canvas_frame')
        content = driver.find_elements_by_css_selector('.content')
        stime = driver.find_elements_by_css_selector('.c_tx.c_tx3.goDetail')
        for con, sti in zip(content, stime):
            data = {
                'time': sti.text,
                'shuos': con.text
            }
        print(data)
    pages = driver.page_source
    soup = BeautifulSoup(pages, 'lxml')


    cookie = driver.get_cookies()
    cookie_dict = []
    for c in cookie:
        ck = "{0}={1};".format(c['name'], c['value'])
        cookie_dict.append(ck)
        i = ''
        for c in cookie_dict:
            i += c
        print('Cookies:', i)
        print("==========完成================")

        driver.close()
        driver.quit()


if __name__ == '__main__':
    get_shuoshuo('1090185058')
'''

'''
#5.将今日头条爬取到的数据放入数据库
import requests
import json
import pymysql

conn = pymysql.connect(host='localhost', port=3307, user='root', password='usbw', db='toutiao', charset='gb2312')
cursor = conn.cursor()

url = 'http://www.toutiao.com/api/pc/focus/'
wbdata = requests.get(url).text

data = json.loads(wbdata)
news = data['data']['pc_feed_focus']

for n in news:
    title = n['title']
    img_url = n['image_url']
    url = n['media_url']
    print(url, title, img_url)
    cursor.execute("INSERT INTO data(title,img_url,url)VALUES('{0}','{1}','{2}');".format(title, img_url, url))
    conn.commit()

cursor.close()
conn.close()
'''

#6.将智联招聘爬取到的数据放入数据库中
import requests
from bs4 import BeautifulSoup
import re
import pymysql

url = 'https://sou.zhaopin.com/jobs/searchresult.ashx?jl=珠海&kw=python&isadv=0&sg=9e47328cac73417fa919dc6a80d3fd36&p=1'
wbdata = requests.get(url).content
soup = BeautifulSoup(wbdata,'lxml')

items = soup.select("div#newlist_list_content_table > table")
count = len(items) - 1
#print(count) #输出一页有多少个职位

job_count = re.findall(r"共<em>(.*?)</em>个职位满足条件",str(soup))[0]
pages = (int(job_count) // count) + 1
#print(pages)   #输出有多少页



import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import pymysql

conn = pymysql.connect(host='localhost', port=3307, user='root', password='usbw', db='zhaopin', charset='gb2312')
cursor = conn.cursor()

def get_zhaopin(page):
    url = 'https://sou.zhaopin.com/jobs/searchresult.ashx?jl=珠海&kw=python&isadv=0&sg=9e47328cac73417fa919dc6a80d3fd36&p={0}'.format(page)
    #print("第{0}页".format(page))
    wbdata = requests.get(url).content
    soup = BeautifulSoup(wbdata, 'lxml')

    job_name = soup.select("table.newlist > tr > td.zwmc > div > a")
    salarys = soup.select("table.newlist > tr > td.zwyx")
    locations = soup.select("table.newlist > tr > td.gzdd")
    companys = soup.select("table.newlist > tr > td.gsmc")
    times = soup.select("table.newlist > tr > td.gxsj > span")


    for name, salary, location, company, time in zip(job_name, salarys, locations, companys, times):
        data = {
            'name': name.get_text(),
            'salary': salary.get_text(),
            'location': location.get_text(),
            'company': company.get_text(),
            'time': time.get_text(),
        }
        #print(data['name'])
        print(data)
        cursor.execute("INSERT INTO data(name,salary,location,company,time)VALUES('{0}','{1}','{2}','{3}','{4}');".format(data['name'], data['salary'], data['location'], data['company'], data['time']))
        conn.commit()

    cursor.close()
    conn.close()

if __name__ == '__main__':
    pool = Pool(processes=6)
    pool.map_async(get_zhaopin, range(1, pages+1))
    pool.close()
    pool.join()