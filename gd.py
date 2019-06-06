# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 18:41:43 2019

"""

from urllib.parse import quote
from urllib import request
import json
import os
import webbrowser
 
amap_web_key = 'a3200989b59c71b1fabac246b9ebcbce'
poi_search_url = "http://restapi.amap.com/v3/place/text"
poi_boundary_url = "https://ditu.amap.com/detail/get/detail"


cityname = input("输入地点：")  #"天津"
classfiled = input("输入类别：") #"旅游景点"
print("请稍等") 
# 根据城市名称和分类关键字获取poi数据
def getpois(cityname, keywords):
    i = 1
    poilist = []
    while True:  # 使用while循环不断分页获取数据
        result = getpoi_page(cityname, keywords, i)
        result = json.loads(result)  # 将字符串转换为json
        if result['count'] == '0':
            break
        poilist.extend(result['pois'])
        i = i + 1
#    print(poilist)
    return poilist

def write_to_json(poilist,cityname,classfield):
    l2=[]
    l3=['lng','lat','title']
    l4=[]
    for i in range(len(poilist)):
        st=poilist[i]['location']
        a=st.split(',')
        l2.append(a[0])
        l2.append(a[1])
        l2.append(poilist[i]['name'])        
        n=dict(zip(l3,l2))
        l4.append(n)
        del l2[:]
    
    if os.path.exists("W:/Desktop/Map/file/employee.json") :
        os.remove("W:/Desktop/Map/file/employee.json")

    with open("W:/Desktop/Map/file/employee" +'.txt', 'a+',encoding="utf-8")as fp: 
        jsonArr = 'train(['
        fp.write(jsonArr+"\n")
        fp.close() 
   
    for items in l4[:-2]:
        with open("W:/Desktop/Map/file/employee" +'.txt', 'a+',encoding="utf-8")as fp: 
#            jsonArr = json.dumps(dict(items),ensure_ascii=False)
            jsonArr = str(items)
            fp.write(jsonArr+",\n")
            fp.close() 
    with open("W:/Desktop/Map/file/employee" +'.txt', 'a+',encoding="utf-8")as fp: 
#        jsonArr = json.dumps(dict(l4[-1]),ensure_ascii=False)
        jsonArr = str(l4[-1])+'])'
        fp.write(jsonArr+"\n")
        fp.close() 
    filename = "W:/Desktop/Map/file/employee" +'.txt'
    portion = os.path.splitext(filename)
    newname = portion[0]+".json"
    os.rename(filename,newname)

# 将返回的poi数据装入集合返回
def hand(poilist, result):
    # result = json.loads(result)  # 将字符串转换为json
    pois = result['pois']
    for i in range(len(pois)):
        poilist.append(pois[i])
 
 
# 单页获取pois
def getpoi_page(cityname, keywords, page):
    req_url = poi_search_url + "?key=" + amap_web_key + '&extensions=all&keywords=' + quote(
        keywords) + '&city=' + quote(cityname) + '&citylimit=true' + '&offset=25' + '&page=' + str(
        page) + '&output=json'
    data = ''
    with request.urlopen(req_url) as f:
        data = f.read()
        data = data.decode('utf-8')
    return data
 
# 获取城市分类数据
 
pois = getpois(cityname, classfiled)
 
# 将数据写入json
write_to_json(pois, cityname, classfiled)
url = 'file:///W:/Desktop/Map/Map.html'
webbrowser.open(url)
print (webbrowser.get())
#print('写入成功')
 