# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 13:17:16 2020
程序功能：可以爬取电影天堂网站所有的电影名称，电影详情，磁力链接
@author: emperor
"""

import requests
#import re
import bs4
import pandas as pd
import datetime
#获取网页
def getHTMLText(url):
    try:
         headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'}
         r = requests.get(url, headers = headers, timeout = 30)
         r.raise_for_status()
         r.encoding = r.apparent_encoding
         return r.text
    except requests.HTTPError as e:
        print(e)
        print("HTTPError")
    except requests.RequestException as e:
        print(e)
    except:
        print("Unknown Error !")
#解析网页
def parseHtml(html):
    bsObj = bs4.BeautifulSoup(html, "html.parser")
    info = []#储存所有信息
    #获取电影列表
    tblist = bsObj.find_all('table', attrs = {'class':'tbspan'})
    #对一页里面的每一个电影单独解析处理
    for item in tblist:
        movie = []
        link = item.b.find_all('a')[1]
        
        #获取电影名称
        movie_name = link["title"]
        
        #获取电影详情的url
        url = "https://www.dy2018.com"+link["href"]
        
        #将电影的名称和详情链接放入movie列表
        movie.append(movie_name)
        movie.append(url)
        #print(movie)
        try:
            temp = bs4.BeautifulSoup(getHTMLText(url), "html.parser")#解析电影详情页
            tbody = temp.find_all('tbody')
            #将电影下载链接放入movie列表
            for i in tbody:
                download = i.a.text
                movie.append(download)
            #print(movie)
            #将电影信息全部放入电影列表中
            info.append(movie)
        except Exception as e:
            print(e)
    return info
#储存电影信息
def saveDate(data):
    file_name = '电影天堂.csv'#可用正则表达式，自动选取名字
    
    dataFrame = pd.DataFrame(data)
    dataFrame.to_csv(file_name, mode='a', index=False, sep=',', header=False)
#主函数
def main():
    start_url = "https://www.dy2018.com/"
    depth = 1#翻页器，可以自定义翻页数
    style = 20#不同类型的电影，共20类
    for j in range(style):
        print("正在爬取第" + str(1+j) + "类电影信息")
        first_url = start_url + str(1+j) + "/index"
        for i in range(depth):
            print("正在爬取第" + str(1+i) + "页电影信息")
            if i == 0:
                url = first_url + ".html" #处理第一页,可设计处理“1”，实现不同类型的电影爬取
            else:    
                url = first_url + "_" +str(i*2) + ".html"#翻页
            html = getHTMLText(url)
            movies = parseHtml(html)
            saveDate(movies)
if __name__ == '__main__':
    print('爬虫开始启动')
    start_time = datetime.datetime.now()
    main()
    end_time = datetime.datetime.now()
    print("程序总共用时：{:}".format(end_time - start_time))
    print('爬取页面结束')
