from tkinter import *

def foo():
    global var_list
    for v in var_list:
        if (v.get()>0):print(var_list.index(v),end=',')
    print()



def onclick_cb(n):
    global value_list
    print(n)
    if n in value_list:
        value_list.remove(n)
    else:
        value_list.add(n)
    print(value_list)

root=Tk()
root.geometry("+600+400")
frm1=Frame(root)
frm1.pack(side=LEFT)
cb_list=[]
value_list=set()
for i in range(10):
    Checkbutton(frm1, text=str(i), command=lambda s=i: onclick_cb(s)).pack()



frm2=Frame(root)
frm2.pack(side=LEFT)
var_list=[]
for i in range(10):
    v=IntVar()
    var_list.append(v)
    Checkbutton(frm2, text=str(i), variable=v).pack()
Button(frm2, text='test',command=foo).pack()

frm3=Frame(root)
frm3.pack(side=LEFT)
btn_list=[]
for i in range(15):
    t=Button(frm3,text=str(i))
    btn_list.append(t)
    t.pack()

root.mainloop()
