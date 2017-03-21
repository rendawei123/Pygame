from tkinter import *

master = Tk()

theLB = Listbox(master)
theLB.pack()

for item in ['鸡蛋', '鸭蛋', '鹅蛋', '李狗蛋']:
    theLB.insert(END, item)

Button(master, text='删除', command=lambda x=theLB: x.delete(ACTIVE)).pack()

mainloop()
