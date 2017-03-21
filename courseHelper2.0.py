
'''
Author:     Super_Red
Date:       21/3/2017
Describe:   rewrite the courseHelper to make it more readible
'''

'''
Modify the 'xuanKeParams' in line 100 before use!!!!!!!!!!!
'''

from bs4 import BeautifulSoup
import requests
import time

import threading
import json
from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO


class DataManager(object):

    def __init__(self):
        '''
        use Session in requests to story cookies
        First get the login pages to get the cookies
        Then download the checkCode and match it to make the cookies vaild
        '''
        self.session = requests.Session()
        self.session.get("http://bkxk.xmu.edu.cn/xsxk/login.html")
        self.checkCodeImage = self.getCheckCodeImage()
        self.loginStatus = False
        self.quitThreadFlag = [False, ]

    def getCheckCodeImage(self):
        timeparams = {"now" : time.asctime()[:-13] + time.asctime()[-4:] + time.asctime()[-14:-4] + "GMT 0800"}
        myRequest = self.session.get("http://bkxk.xmu.edu.cn/xsxk/getCheckCode",params=timeparams)
        checkCodeImage = Image.open(BytesIO(myRequest.content))
        # modify the checkCode to fit the tkinter window
        (width,height) = checkCodeImage.size
        checkCodeImage = checkCodeImage.resize((60,int(height*60/width)),Image.ANTIALIAS)
        return checkCodeImage

    def login(self, userData):
        r = self.session.post("http://bkxk.xmu.edu.cn/xsxk/login.html", data=userData)
        redFont = BeautifulSoup(r.text, "html.parser").findAll("font", {"color" : "red"})
        if len(redFont) == 0:
            self.loginStatus = True
            print("Login Successfully")
        else:
            self.loginStatus = False

    def getCurriculums(self):
        r = self.session.get("http://bkxk.xmu.edu.cn/xsxk/localInfo.html")
        xiaoXuanURL = "http://bkxk.xmu.edu.cn/xsxk/qxxxx.html"
        bsObj = BeautifulSoup(self.session.get(xiaoXuanURL).text, "html.parser")
        totalPages = int(bsObj.findAll("span", {"id" : "totalPageCount"})[0].text)
        curriculumList = []
        for page in range(totalPages):
            params = {  "pagination" : 20,
                        "pageNo" : (page + 1) }
            pageBSObj = BeautifulSoup(self.session.get(xiaoXuanURL, params=params).text, "html.parser")
            curriculums =[(result["id"], result.text) for result in pageBSObj.findAll("a", {"class" : "jxjd"})]
            curriculumList += curriculums
        self.curriculumList = curriculumList
        return self.curriculumList

    def getTheSelectedCourse(self, *courseButtonVarList):
        self.courseSelected = []
        for index, v in enumerate(courseButtonVarList):
            if v.get() > 0 and self.curriculumList[index] not in self.courseSelected:
                self.courseSelected.append(self.curriculumList[index])
        courseName = [course[1] for course in self.courseSelected]
        print("你已选的课是",courseName)
        self.checkTheSelectedCourses()

    def checkTheSelectedCourses(self):
        xuanKeHeader = {    "Content-Type"      :   "application/x-www-form-urlencoded",
                            "X-Requested-With"  :   "XMLHttpRequest"} 

        checkTime = 0
        while(len(self.courseSelected) > 0 and (not self.quitThreadFlag[0])):
            time.sleep(0.5)
            checkTime += 1
            for course in self.courseSelected:
                checkData = {"jxbs":'''[{"jxbid":"''' + course[0] + '''"}]''','xxlx':3}
                r = self.session.post('http://bkxk.xmu.edu.cn/xsxk/calJxbRs.html?method=getRsToZxxk', data=checkData, headers=xuanKeHeader)
                keXuanRenShu = int(json.loads(r.text)["data"][0]["kxrs"])
                yiXuanRenShu = int(json.loads(r.text)["data"][0]["yxrs"])
                print("{coursename} 第 {times} 次查询,人数：{kxrs}/{yxrs}".format(coursename=course[1], times=checkTime, kxrs=keXuanRenShu, yxrs=yiXuanRenShu))
                if keXuanRenShu < yiXuanRenShu :
                    self.applyTheAvailableCourse(course)
            print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')

    def applyTheAvailableCourse(self, course):
        # xuanKeParam is the only changable thing to modify every time!!
        xuanKeUrl = 'http://bkxk.xmu.edu.cn/xsxk/elect.html'
        xuanKeParams = {    'method'    :   'handleZxxk',
                            'jxbid'     :   course[0],
                            'xxlx'      :   '3',
                            'xklc'      :   '2015304'}
        r = self.session.get(xuanKeUrl, params=xuanKeParams)
        if(json.loads(r.text)['success']):
            self.courseSelected.remove(course)
            print("成功选上%s!!!!" % name)

class CourseHelper(object):

    def __init__(self, dataManager):
        self.dataManager = dataManager
        self.bulidRoot()
        self.stringVarList = [StringVar() for i in range(3)]
        self.stringVarList[0].set("17420132200463")
        self.stringVarList[1].set("215055")
        self.usernameEntry = Entry(self.root, width=15, textvariable=self.stringVarList[0])
        self.passwordEntry = Entry(self.root, width=15, textvariable=self.stringVarList[1])
        self.checkCodeEntry = Entry(self.root, width=5, textvariable=self.stringVarList[2])
        self.bulidLayout()
        self.root.mainloop()

    def bulidRoot(self):
        self.root = Tk()
        self.root.title("Course Helper")
        self.root.geometry("400x400+500+200")
        self.root.resizable(False, False)

    def bulidLayout(self):
        Label(self.root, text="学号: ",font="Monaco 15").place(x=50,y=10)
        Label(self.root, text="密码: ",font="Monaco 15").place(x=50,y=40)
        Label(self.root, text="验证码: ",font="Monaco 15").place(x=50,y=70)
        self.usernameEntry.place(x=120,y=10)
        self.passwordEntry.place(x=120,y=40)
        self.checkCodeEntry.place(x=120,y=70)
        self.passwordEntry["show"] = "*"
        self.codeImage = ImageTk.PhotoImage(self.dataManager.checkCodeImage) 
        Label(self.root, image=self.codeImage).place(x=190,y=70)
        Button(text=" 登 录   ", command=self.submitData).place(x=280,y=20)
        Button(text=" 重 置   ", command=self.resetEntry).place(x=280,y=50)

    def resetEntry(self):
        for variable in self.stringVarList:
            variable.set("")

    def submitData(self):
        userData = {}
        userData["username"] = self.stringVarList[0].get()
        userData["password"] = self.stringVarList[1].get()
        userData["checkCode"] = self.stringVarList[2].get()
        self.usernameEntry['state'] = 'readonly'
        self.passwordEntry['state'] = 'readonly'
        self.checkCodeEntry['state'] = 'readonly'
        self.dataManager.login(userData)
        if self.dataManager.loginStatus:
            # login sucessfully 
            curriculums = self.dataManager.getCurriculums()
            self.showContent(curriculums)
        else:
            Label(self.root, font="Monaco 15", text="登录失败，请重启！").place(x=100,y=200)

    def showContent(self, curriculums):
        # bind the horizontal_scroller_bar to a canvas and place the canvas to the right place
        canvas = Canvas(self.root, width=400, height=260, borderwidth=0)
        hsb = Scrollbar(self.root, orient="horizontal", command=canvas.xview)
        canvas.configure(xscrollcommand=hsb.set)
        hsb.pack(side="bottom", fill="x")
        canvas.place(x=0, y=97)
        # create a frame inside canvas to display courses
        self.displayFrame = Frame(canvas)
        canvas.create_window((4, 4), window=self.displayFrame, anchor="nw")
        # make sure that the frame can be controlled by the hsb
        self.displayFrame.bind("<Configure>", lambda event : canvas.configure(scrollregion=canvas.bbox("all")))
        self.populate(curriculums)
        self.addButtons()

    def populate(self, curriculums):
        print(curriculums)
        self.courseButtonVarList = []
        columns = len(curriculums) // 10
        remainings = len(curriculums) % 10
        for column in range(columns):
            for row in range(10):
                v = IntVar()
                self.courseButtonVarList.append(v)
                Checkbutton(self.displayFrame, text=curriculums[10*column+row][1], variable=v).grid(row=row, column=column, sticky='w')
            Label(self.displayFrame, text="{pages}-{index}".format(pages=int(column/2)+1, index=column%2+1)).grid(row=row+1, column=column, sticky='s')
        if remainings != 0:
            for row in range(remainings):
                v = IntVar()
                self.courseButtonVarList.append(v)
                Checkbutton(self.displayFrame, text=curriculums[10*columns+row][1],variable=v).grid(row=row, column=columns, sticky='w')
            Label(self.displayFrame, text="{pages}-{index}".format(pages=int(columns/2)+1, index=columns%2+1)).grid(row=10, column=columns, sticky='s')

    def addButtons(self):
        self.getButton = Button(self.root, text="  抢 课   ",command=lambda:self.startThread())
        self.getButton.place(x=100,y=356)
        self.quitButton = Button(self.root, text="  退 出   ",command=(lambda:self.exit()), state='disabled')
        self.quitButton.place(x=200,y=356)

    def startThread(self):
        self.dataManager.quitThreadFlag[0] = False
        self.getButton['state']='disabled'
        self.quitButton['state']='normal'
        self.thread1 = threading.Thread(target=self.dataManager.getTheSelectedCourse, args=(self.courseButtonVarList))
        self.thread1.start()

    def exit(self):
        self.dataManager.quitThreadFlag[0] = True
        self.getButton['state']='normal'
        self.quitButton['state']='disabled'
        time.sleep(2)
        if (not self.thread1.is_alive()):
            print("You have successfully quit the programe\nRestart it if you wanna use it again")
        else: 
            print("Something goes wrong!")
        self.thread1.join()

dataManager = DataManager()
gui = CourseHelper(dataManager)

