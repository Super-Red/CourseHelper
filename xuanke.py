# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
import pickle
import os
from PIL import Image
from io import BytesIO
# # 方法一：登录成功后，把chrome的cookiestring拷贝出来，然后每次get网页时一起提交上去
# cookies={"JSESSIONID":"0000C6Y47Cmd46RNcAYqr4pzXaQ:16mk94c6h"}
# r=requests.get("http://bkxk.xmu.edu.cn/xsxk/index.html", cookies=cookies)
# print(r.text)

# 方法二：登录时单独取一次验证码，保存到jpg文件里供人工识别。
if not os.path.exists("xuanke.cookie"):
    session=requests.Session()
    h={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"}
    session.headers.update(h)
    data={ "username":"17420132200463",
    "password":"215055",
    "checkCode":"",
    }
    r=session.get("http://bkxk.xmu.edu.cn/xsxk/login.html")
    #print(r.text)
    params={"now":"Sat Apr 30 2016 01:46:50 GMT 0800"}
    r=session.get("http://bkxk.xmu.edu.cn/xsxk/getCheckCode",params=params)
    # 执行这句需要pil模块，如果没装的话，可以注释掉这句，然后把图片保存到文件后再查看。
    Image.open(BytesIO(r.content)).show()


    #open("a.jpg",'wb').write(r.content)

    data["checkCode"]=input("check code: ")
    r=session.post("http://bkxk.xmu.edu.cn/xsxk/login.html",data=data)
    open('t1.html','wb').write(r.content)
    pickle.dump(session,open("xuanke.cookie",'wb'))
else:
    session=pickle.load(open("xuanke.cookie",'rb'))

# r=session.get("http://bkxk.xmu.edu.cn/xsxk/localInfo.html")
# open('t.html','wb').write(r.content)
# print(len(r.text))
# r=session.get("http://bkxk.xmu.edu.cn/xsxk/qxxxx.html")
# open('t.html','wb').write(r.content)
# print(len(r.text))

url="http://bkxk.xmu.edu.cn/xsxk/calJxbRs.html?method=getRsToZxxk"
data={"jxbs":"""[{"jxbid":"201531300200101935533"}]""","xxlx":"3"}
h={"Content-Type":"application/x-www-form-urlencoded","X-Requested-With":"XMLHttpRequest"}
r=session.post(url,data=data, headers=h)
print(r.text)
