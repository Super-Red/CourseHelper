from tkinter import *
from threading import Thread
import time

def print_hello(stop):
    while(not stop[0]):
        print("hello")
        time.sleep(1)

def start_thread():
    global mythread, stop_sign
    stop_sign[0]=False
    btn1['state']=DISABLED
    btn2['state']=NORMAL
    mythread=Thread(target=print_hello, args=(stop_sign,))
    mythread.start()

def stop_thread():
    global stop_sign
    stop_sign[0]=True
    btn1['state']=NORMAL
    btn2['state']=DISABLED
    mythread.join()




root=Tk()
frm1=Frame(root)
frm1.pack()

btn1=Button(frm1, text="start", command=start_thread)
btn1.pack()
btn2=Button(frm1, text="stop", command=stop_thread, state=DISABLED)
btn2.pack()

mythread=None
stop_sign=[False,]


root.mainloop()
