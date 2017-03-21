from tkinter import *

root = Tk()

s1 = Scale(root, from_=0, to=33, tickinterval=5, resolution=3, length=200)
s1.pack()

s2 = Scale(root, from_=0, to=99, length=600, orient=HORIZONTAL)
s2.pack()


def show():
    print(s1.get(),s2.get())

Button(root, text='输出', command=show).pack()

mainloop()
