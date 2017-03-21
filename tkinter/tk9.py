from tkinter import *

master = Tk()

frame = Frame(master)
frame.pack(padx=10, pady=10)

v1 = StringVar()
v2 = StringVar()
v3 = StringVar()


def test(content):
    return content.isdigit()

testCMD = master.register(test)

e1 = Entry(frame, textvariable=v1, width=10, validate='key', validatecommand=(testCMD, '%P'))\
    .grid(row=0, column=0)
e2 = Entry(frame, textvariable=v2, width=10, validate='key', validatecommand=(testCMD, '%P'))\
    .grid(row=0, column=2)
e3 = Entry(frame, textvariable=v3, width=10,state='readonly').grid(row=0, column=4)

Label(frame, text='+').grid(row=0, column=1)
Label(frame, text='=').grid(row=0, column=3)


def cale():
    result = int(v1.get()) + int(v2.get())
    v3.set(str(result))

Button(frame, text='计算', command=cale).grid(row=1, column=2, pady=5)

mainloop()
