
import time, requests, re, json, threading
from time import sleep
from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO

# curriculumList
curriculum=[('201531300200101935533','英语诗歌阅读与创作'),
            ('201531300200200915538','德语电影欣赏'),
            ('2E861B267B250046E053D22200360046','英语口语'),
            ('2E861B267B400046E053D22200360046','英语口语'),
            ('2E861B267B280046E053D22200360046','英语口语'),
            ('2E861B267B2B0046E053D22200360046','英语口语'),
            ('2E861B267B2E0046E053D22200360046','英语口语'),
            ('2E861B267B310046E053D22200360046','英语口语'),
            ('2E861B267B340046E053D22200360046','英语口语'),
            ('2E861B267B370046E053D22200360046','英语口语'),
            ('2E861B267B3A0046E053D22200360046','英语口语'),
            ('2E861B267B3D0046E053D22200360046','英语口语'),
            ('31961CD7446D006EE053D2220036006E','税捐行政法'),
            ('201531300400300175539','人际心理学'),
            ('201531300600500095509','创业创造力'),
            ('30B84BB6093700EAE053D222003600EA','数理逻辑'),
            ('318A33481CB400DCE053D222003600DC','信息安全'),
            ('30CEC19FBB17005EE053D2220036005E','自适应网格方法'),
            ('30CEC19FBB23005EE053D2220036005E','利息理论'),
            ('30CEC19FBB2B005EE053D2220036005E','贝叶斯统计'),
            ('32A12C5C7DAC00B6E053D222003600B6','纳米科学前沿'),
            ('201531300900100815605','看电影学物理'),
            ('307560A2E5B4005AE053D2220036005A','今日化学（一）'),
            ('31463420DCAE00DAE053D222003600DA','今日化学（二）'),
            ('307560A2E5BA005AE053D2220036005A','无机化学新兴领域简介'),
            ('314610391F1B010EE053D2220036010E','有机化学新兴领域简介'),
            ('30D25F6872060016E053D22200360016','化学与逻辑'),
            ('307F230B3F4B001CE053D2220036001C','中国结（一）'),
            ('318A205C508D00F4E053D222003600F4','大学生创新创业训练'),
            ('306F68D7DCCF0002E053D22200360002','化工与生工前沿'),
            ('201531301100100205585','艾滋病与健康'),
            ('201531301200100455611','海洋生物学'),
            ('201531301200200825484','环境保护概论'),
            ('201531301500100465511','恶性肿瘤防治'),
            ('201531301500400535510','刮痧疗法'),
            ('201531301800000265545','开辟荆榛逐荷夷——郑成功收复台湾之战'),
            ('201531302600100715482','材料科学与工程导论'),
            ('3215C5DB9C73019CE053D2220036019C','当代国家形象与国际宣传专题（1945-2015）'),
            ('32157A5CC0DF0056E053D22200360056','新媒体、技术与社会'),
            ('3216A1427853010CE053D2220036010C','新闻中的跨文化传播'),
            ('3215C5DB9C76019CE053D2220036019C','文创产业与品牌传播'),
            ('3261C1ACFECF0088E053D22200360088','大数据营销'),
            ('324EB9A4BE5C0060E053D22200360060','新闻摄影的多模修辞分析'),
            ('3215C5DB9C79019CE053D2220036019C','影像视觉语言导论'),
            ('201531303600100455489','环境因素与健康'),
            ('201531400100100205576','美国人心态探索：观念和视角'),
            ('201531400200100285575','英语戏剧表演艺术'),
            ('201531400200100635531','英语电影欣赏'),
            ('30E72FF5BA49004EE053D2220036004E','日常法语'),
            ('31DE1F00BE0E00F2E053D222003600F2','商业社会与现代中国'),
            ('201531400700500015578','小提琴训练与世界名曲欣赏'),
            ('30D29FCABD9D00DEE053D222003600DE','初等代数几何'),
            ('307EB4C706910016E053D22200360016','Fourier级数与分析选讲'),
            ('3145D37770B80078E053D22200360078','能源化学前沿论坛'),
            ('3146439AE88500CAE053D222003600CA','能源材料基础'),
            ('201531401001300015503','磷与生活'),
            ('201531401200200095485','海洋环境'),
            ('201531401301400025501','IT企业文化'),
            ('201531401500100155486','乳房健康与肿瘤整形'),
            ('201531401500100165487','肿瘤放射治疗学'),
            ('201531401900300025521','教育学'),
            ('201531401900300045522','人力资源开发与管理'),
            ('201531402600100055483','大功率LED的封装与应用'),
            ('201531402600100065631','《生活与艺术中的材料学系列实验》之一'),
            ('31ED513F431F00E0E053D222003600E0','大学生生涯发展与规划'),
            ('31DE1F00B84700F2E053D222003600F2','记者是如何炼成的'),
            ('320140C2F5D501A0E053D222003601A0','西班牙语入门'),
            ('320140C2F5D801A0E053D222003601A0','西班牙语入门'),
            ('201531500400300045541','心理学入门'),
            ('314B1086936F00FAE053D222003600FA','人因学入门简介'),
            ('3210A12416D900A0E053D222003600A0','平面设计与艺术思维'),
            ('201531500900100015606','金融物理'),
            ('31463420DCB400DAE053D222003600DA','化学化工应用专题'),
            ('201531501300100045500','科学办学'),
            ('201531501300400025504','Latex排版技术'),
            ('201531501300400035612','物联网智能硬件创新实践与众筹验证'),
            ('201531501500100045512','肾脏保健常识'),
            ('201531501500400045513','中医基础理论介绍'),
            ('318A33481C9D00DCE053D222003600DC','社会探究的趣味'),
            ('201531501800000025546','台湾集团企业发展及国际化'),
            ('201531501900300025506','世界著名大学概览'),
            ('201531501900300045505','科举与高考'),
            ('3216A0A9975100FEE053D222003600FE','论文写作与期刊投稿'),
            ('32250946E4E90066E053D22200360066','中日关系史上代表性事件的表与里分析'),
            ('3216A142784D010CE053D2220036010C','影像与文化传播'),
            ('201531503100100075582','台湾流行文化研究'),
            ('31DE1F00B84D00F2E053D222003600F2','数据新闻'),
            ('31DE1F00B85000F2E053D222003600F2','中美国际新闻报道比较'),
            ('3216A0A9975400FEE053D222003600FE','创意思考与应用'),
            ('31DE1F00B85300F2E053D222003600F2','新闻评论写作'),
            ('33149A4299750172E053D22200360172','马克思主义新闻学理论与实践'),
            ('201531600100100085584','诺贝尔文学奖评述'),
            ('201531600100200025604','宋代文豪的日常生活'),
            ('201531600100200045602','中国农商社会概论'),
            ('32789E5AB9F301FAE053D222003601FA','韩国儒学与韩国文化'),
            ('32789E5AB9F901FAE053D222003601FA','儿童哲学的理论与实务'),
            ('326601543F68004CE053D2220036004C','哲学与文学'),
            ('326601543F6B004CE053D2220036004C','古希腊哲学导论'),
            ('3182D78EDC7300F2E053D222003600F2','音乐的观念'),
            ('2E874BFF1B5E00D0E053D222003600D0','视听韩国语'),
            ('2E874BFF1B6100D0E053D222003600D0','视听韩国语'),
            ('2E874BFF1B6400D0E053D222003600D0','视听韩国语'),
            ('201531600400100015569','风险分析与管控'),
            ('318A29C27B6600DEE053D222003600DE','与“众”不同的心理学'),
            ('201531600400300025554','认知神经科学'),
            ('201531600900100025607','现代征信学概论'),
            ('201531601006000025610','厦门大学ETC大学生创业培训之经济金融服务行业'),
            ('201531601006000045629','厦门大学ETC大学生创业培训之文化创意产业'),
            ('201531601006000055630','厦门大学ETC大学生创业培训之电子信息产业'),
            ('321809C3954901A6E053D222003601A6','音乐开启的现代科学'),
            ('201531601101000025567','生态之美大讲堂'),
            ('201531601101000035566','土壤，食品安全与人类健康'),
            ('201531601800000025617','两岸经贸热点问题'),
            ('201531601800000035618','台湾地理概论'),
            ('201531601900300015572','教育经典魅力'),
            ('201531602600100015523','生活与艺术中的材料学系列实验之二和之三'),
            ('201531603200000025552','新世纪里谈百年好“核”')]

# 先使用Session登录首页保存cookies，再用session实例请求checkCode，下载。
session = requests.Session()
r = session.get("http://bkxk.xmu.edu.cn/xsxk/login.html")
params = {"now":time.asctime()[:-13]+time.asctime()[-4:]+time.asctime()[-14:-4]+"GMT 0800"}
r = session.get("http://bkxk.xmu.edu.cn/xsxk/getCheckCode",params=params)
checkCodeImage = Image.open(BytesIO(r.content))
(width,height) = checkCodeImage.size
checkCodeImage = checkCodeImage.resize((60,int(height*60/width)),Image.ANTIALIAS)
courseidList=[]
courseSelected=[]
courseName = []
userData = {"username":"","password":"","checkCode":""}
root = Tk()
root.title("Course Helper")
button = []
threadlist = []


# 输入用户信息
def submit(userData,e1,e2,e3):
      global r 
      userData["username"] = e1.get()
      userData["password"] = e2.get()
      userData["checkCode"] = e3.get()
      e1['state'] = 'readonly'
      e2['state'] = 'readonly'
      e3['state'] = 'readonly'
      r = session.post("http://bkxk.xmu.edu.cn/xsxk/login.html",data=userData)
      if(len(re.findall(r'(?=<font color="red">)', r.text))>0):
            Label(root, font="Monaco 15", text="登录失败，请重启！").place(x=100,y=200)
      else:
            showCurriculum(root)
      r = session.get("http://bkxk.xmu.edu.cn/xsxk/localInfo.html")
      r = session.get("http://bkxk.xmu.edu.cn/xsxk/qxxxx.html")

def reset(e1,e2,e3):
      e1.set("")
      e2.set("")
      e3.set("")

def exit(quitFlag):
      quitFlag[0] = True
      button[0]['state']='normal'
      button[1]['state']='disabled'
      sleep(2)
      if (not getThread.is_alive()):
            print("You have successfully quit the programe\nRestart it if you wanna use it again")
      else : print("Something goes wrong!")
      getThread.join()

def populate(frame):
      for column in range(11):
            for row in range(10):
                  v = IntVar()
                  courseidList.append(v)
                  Checkbutton(frame, text=curriculum[10*column+row][1], variable=v).grid(row=row, column=column, sticky='w')
            Label(frame, text="%s-%s" % (int(column/2)+1, column%2+1)).grid(row=row+1, column=column, sticky='s')
      for row in range(7):
            Checkbutton(frame, text=curriculum[110+row][1],variable=v).grid(row=row, column=11, sticky='w')
      Label(frame, text="6-2").grid(row=10, column=11, sticky='s')

def qiangKe(courseSelected, quitFlag, courseName):   
      xuanKeUrl = 'http://bkxk.xmu.edu.cn/xsxk/elect.html'
      xuanKeParams = {
            'method':'handleZxxk',
            'jxbid':'',
            'xxlx':'3',
            'xklc':'2015304'}
      xuanKeHeader = {
            "Content-Type":"application/x-www-form-urlencoded",
            "X-Requested-With":"XMLHttpRequest"}     
      
      requestTime = 0
      while((len(courseSelected)>0)&(not quitFlag[0])):
            sleep(0.5)
            requestTime += 1
            for i in courseSelected:
                  name = courseName[courseSelected.index(i)]
                  xuanKeParams['jxbid']=i
                  data = {"jxbs":'''[{"jxbid":"'''+i+'''"}]''','xxlx':3}

                  r = session.post('http://bkxk.xmu.edu.cn/xsxk/calJxbRs.html?method=getRsToZxxk', data=data, headers=xuanKeHeader)
                  keXuanRenShu = re.findall(r'"yxrs":"(.*?)"',r.text)[0]
                  yiXuanRenShu = re.findall(r'"kxrs":"(.*?)"',r.text)[0]
                  print("%s 第 %d 次查询,人数：%d/%d" %(name, requestTime, int(keXuanRenShu), int(yiXuanRenShu)))
                  if(keXuanRenShu<yiXuanRenShu):
                        r = session.get(xuanKeUrl,params=xuanKeParams)
                        print(r.text)
                        if(json.loads(r.text)['success']):
                              courseSelected.remove(i)
                              courseName.remove(courseName[courseSelected.index(i)])
                              print("成功选上%s!!!!" % name)
            print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')

def getTheCourse(courseidList, courseSelected, quitFlag):
      button[0].config(state = 'disabled')
      courseSelected = []
      courseName = []
      for v in courseidList:
            if ((v.get()>0)&(curriculum[courseidList.index(v)][0] not in courseSelected)):
                  courseSelected.append(curriculum[courseidList.index(v)][0])
                  courseName.append(curriculum[courseidList.index(v)][1])
      print("你已选的课是",courseName)
      qiangKe(courseSelected, quitFlag, courseName)

def startThread(courseidList, courseSelected, quitFlag):
      global getThread
      quitFlag[0] = False
      button[0]['state']='disabled'
      button[1]['state']='normal'
      getThread = threading.Thread(target=getTheCourse,args=(courseidList, courseSelected, quitFlag))
      getThread.start()

def showCurriculum(root):
      canvas = Canvas(root, width=400, height=260, borderwidth=0)
      frame = Frame(canvas)
      hsb = Scrollbar(root, orient="horizontal", command=canvas.xview)
      canvas.configure(xscrollcommand=hsb.set)
      hsb.pack(side="bottom", fill="x")
      canvas.place(x=0, y=97)
      canvas.create_window((4,4), window=frame, anchor='nw')
      frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
      populate(frame)
      quitFlag = [False, ]
      getButton = Button(text="  抢 课   ",command=lambda:startThread(courseidList, courseSelected, quitFlag))
      getButton.place(x=100,y=356)
      button.append(getButton)
      quitButton = Button(text="  退 出   ",command=(lambda:exit(quitFlag)), state='disabled')
      quitButton.place(x=200,y=356)
      button.append(quitButton)

def onFrameConfigure(canvas):
      canvas.configure(scrollregion=canvas.bbox("all"))

def builtGUI(userData):
      root.geometry("400x400+500+200")
      root.resizable(False,False)
      Label(text="学号: ",font="Monaco 15").place(x=50,y=10)
      Label(text="密码: ",font="Monaco 15").place(x=50,y=40)
      Label(text="验证码: ",font="Monaco 15").place(x=50,y=70)
      (e1,e2,e3)=(StringVar(),StringVar(),StringVar())
      usernameEntry=Entry(width=15,textvariable=e1)
      passwordEntry=Entry(width=15,textvariable=e2)
      checkCodeEntry=Entry(width=5,textvariable=e3)
      usernameEntry.place(x=120,y=10)
      passwordEntry.place(x=120,y=40)
      checkCodeEntry.place(x=120,y=70)
      passwordEntry["show"] = "*" 
      codeImage = ImageTk.PhotoImage(checkCodeImage) 
      Label(root,image=codeImage).place(x=190,y=70)
      Button(text=" 登 录   ",command=lambda:submit\
          (userData,usernameEntry,passwordEntry,checkCodeEntry)).place(x=280,y=20)
      Button(text=" 重 置   ",command=lambda:reset(e1,e2,e3)).place(x=280,y=50) 

      root.mainloop()

builtGUI(userData)      
