# -*- codeing = utf-8 -*-
# @Time : 2021/3/11 22:45
# @Author : 任家辉
# @file kozzulioj.py
# @Software:PyCharm
import re
import requests
import pandas as pd
import json
import time
import numpy as nm
import tkinter as tk
from pyecharts import options as opts
from pyecharts.charts import Bar, Timeline
from pyecharts.commons.utils import JsCode
from pyecharts.faker import Faker
findlink2=re.compile(r'\d*?--(.*?)<a href=mail\.php\?to_user=\d*?>短消息</a></caption>')
findlink=re.compile(r"</td><td>(\d*-\d*-\d* \d*:\d*:\d*)</td><td class='hidden-xs'>LOCAL</td></tr>")
findlink1=re.compile(r'><td>(\d*)</td><td><a href=')
findlink3=re.compile(r'(\d*)-(\d*)-(\d*) (\d*):(\d*):(\d*)')
find=re.compile('id=(.*?)&j')
#

def main():
    print("本程序本质上是\n爬虫技术，pandas操纵excel技术和绘图模块使用的结合，只适用于zzulioj网站，可以督促大家努力刷题")
    print("模块有点多，请添加完毕后再运行代码")
    print('----------------------------------------------------------------------------')
    a=input("请输入学号前10位（如果你们班没几个人刷oj还是算了,没有视觉爽感）：")
    i=int(input('请输入班级人数（数字应>=10,因为是绘制的前十名，所以不够十人会报错,有时输入的数字大于10也会报错，那是因为有人没有用学号注册账号）：'))
    bj=input('请输入你的专业和班级（例如：智能物联三班）：')

    url=get_url(a,i)  #获取网址
    x=0
    TIME = []
    Names=[]
    for U in url:
        tm = get_allu(U)
        if tm!=[]:
            x += 1
            w = []
            if x <= 9:
                nn = '0' + str(x)
            else:
                nn = str(x)
            ur=re.findall(find,U)[0]
            name = get_name(ur)
            if tm != []:
                for i in tm:
                    for j in i:
                        w.append(j)
                w = set(w)
            time = []
            for i in w:
                # ac = int(i[0:4] + i[5:7] + i[8:10] + i[11:13] + i[14:16] + i[17:19])
                ac = int(i[0:4] + i[5:7] + i[8:10])
                time.append(ac)
            print('爬取',name,'完成')
            TIME.append(time)
            Names.append(name)

    save(Names,TIME,a,bj)

def get_name(ur):
    nameurl = 'http://acm.zzuli.edu.cn/userinfo.php?user='+ur
    name=re.findall(findlink2,requests.get(nameurl).text)[0]
    if name==[]:
        return '此人未注册账号'
    else:
        return name
def numbers(list,a):
    w=0
    for i in list:
        if i==a:
            w+=1
    return w

def get_allu(url):
    list=[]
    while True:
        html=requests.get(url).text
        id=re.findall(findlink1,html)
        if id==[]:
            break
        else:
            id=id[-1]
        html1 = requests.get(url).text
        TIME = re.findall(findlink, html)
        url=url+'&top='+id
        list.append(TIME)
        if len(TIME)<20:
            break
        else:
            continue
    return list
def get_url(a,i):
    urlist=[]
    for j in range(1,int(i)+1):
        if j<=9:
            url='http://acm.zzuli.edu.cn/status.php?user_id='+a+'0'+str(j)+'&jresult=4'
        else:
            url='http://acm.zzuli.edu.cn/status.php?user_id='+a+str(j)+'&jresult=4'
        urlist.append(url)
    return urlist
def get_text(url):
    html=requests.get(url).text
    TIME=re.findall(findlink,html)
    return TIME
def save(names,times,Class,bj):
    all={}
    # print(names)
    # 建立表格内容，字典中key为列首，value为内容
    for namd,time in zip(names,times):
        all[namd]=time
    df = pd.DataFrame.from_dict(all,orient='index')
    end=chane(times,all)
    # 将索引设为ID或者name（以上面代码为例)
    # df = df.set_index("name")
    # print(df)
    # 创建excel表并且存入数据
    dfp = pd.DataFrame.from_dict(end, orient='index')
    # print(dfp)
    # print(dfp.loc[].to_list()[1:])
    dzh='D:/zzulioj'+Class+'.xlsx'
    dfp.to_excel(dzh)
    picture(dzh,names,bj)

def chane(allt,zd):
    # print(allt)
    L=[]
    # print(allt)
    for lt in allt:
        for t in lt:
            L.append(t)
    L.sort()
    L=set(L)
    nmls=[]
    for n in L:
        nmls.append(n)
    zong={}
    zong['昵称']=nmls
    nmls.sort()
    for name in zd.keys():
        num=[]
        m=0
    # print(allt.values())
        for i in L:
            list=zd[name]
            N=numbers(list,int(i))
            m+=N
            num.append(m)
        zong[name]=num
        # print(zong)
    return zong
def list(df1,k):
    # print(df1)
    data=df1.loc[0:,k].to_list()[1:]
    # print(data)
    return data

def picture(dzh,namelist,bj):

    df=pd.read_excel(dzh)
    data = df.loc[0].to_list()[1:]
    # x = Faker.choose()
    tl = Timeline()
    tl.add_schema(is_auto_play=False, play_interval=500, is_loop_play=False)
    k = 0
    aaa = namelist
    for i in data:  # data为时间
        # data=list(df1,k)[0]
        # X=df1.columns.to_list()
        X = aaa
        Y = list(df, k)
        s = {'昵称': X, '刷题量': Y}
        tem = pd.DataFrame(s)
        tem = tem.sort_values(by='刷题量', ascending=True)
        X = tem['昵称'].to_list()
        Y = tem['刷题量'].to_list()
        k += 1
        bar = (
            Bar()
                ########
                .add_xaxis(X[-10:])
                .add_yaxis(bj, Y[-10:])
                .reversal_axis()
                # .add_yaxis("商家B", Faker.values())
                .set_global_opts(
                title_opts=opts.TitleOpts("{}排名".format(i)),
                graphic_opts=[
                    opts.GraphicGroup(
                        graphic_item=opts.GraphicItem(
                            rotation=JsCode("Math.PI / 4"),
                            bounding="raw",
                            right=100,
                            bottom=110,
                            z=100,
                        ),
                        children=[
                            opts.GraphicRect(
                                graphic_item=opts.GraphicItem(
                                    left="center", top="center", z=100
                                ),
                                graphic_shape_opts=opts.GraphicShapeOpts(
                                    width=400, height=50
                                ),
                                graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                                    fill="rgba(10,10,10,0.3)"
                                ),
                            ),
                            opts.GraphicText(
                                graphic_item=opts.GraphicItem(
                                    left="center", top="center", z=200
                                ),
                                graphic_textstyle_opts=opts.GraphicTextStyleOpts(
                                    text="{}排名".format(i),
                                    font="bold 26px Microsoft YaHei",
                                    graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                                        fill="#fff"
                                    ),
                                ),
                            ),
                        ],
                    )
                ],
            )
        )
        tl.add(bar, "{}年".format(i))
    tl.render(bj+"zzulioj排名.html")
    print("----------------------")
    print("绘图完成\n排名图已存在您的电脑中")
    print("文件名为："+bj+"zzulioj排名.html")
    print("----------------------")
    print('下次想看可以直接打开文件，不必再次运行代码')
    print("保护zzulioj，是你我的责任！！！")
    print("----------------------")
if __name__ == '__main__':
    main()