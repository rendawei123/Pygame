from tkinter import *

root = Tk()

Label(root, text='帐号').grid(row=0, column=0, padx=10)
Label(root, text='密码').grid(row=1, column=0, pady=10)

v1 = StringVar()
v2 = StringVar()

e1 = Entry(root, textvariable=v1)
e1.grid(row=0, column=1, padx=10, pady=10)
e2 = Entry(root, textvariable=v2, show='*')
e2.grid(row=1, column=1, padx=10, pady=10)


def show():
    print('帐号：%s' % e1.get())
    print('密码：%s' % e2.get())

Button(root, text='芝麻开门', width=10, command=show).grid(row=2, column=0, padx=10, pady=10)
Button(root, text='退出', width=10, command=root.quit).grid(row=2, column=1, padx=10, pady=10)

mainloop()
