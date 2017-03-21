from tkinter import *


def callback():
    var.set('吹吧你，我才不信呢！')

root = Tk()

frame1 = Frame(root)
frame2 = Frame(root)

var = StringVar()
var.set('未满十八周岁者禁止观看！')

text_label = Label(frame1,
                   textvariable=var,
                   justify=LEFT,
                   padx=10)
text_label.pack(side=LEFT)

photo = PhotoImage(file='/Users/David/Desktop/practice/123.gif')
image_label = Label(frame1, image=photo)
image_label.pack(side=RIGHT)

the_button = Button(frame2, text='我已满十八周岁', command=callback)
the_button.pack()

frame1.pack(padx=10, pady=10)
frame2.pack(padx=10, pady=10)

mainloop()
