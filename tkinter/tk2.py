from tkinter import *

root = Tk()

photo = PhotoImage(file='/Users/David/Desktop/practice/蛋蛋的忧伤.gif')
the_label = Label(root,
                  text='蛋蛋的忧伤',
                  justify=LEFT,
                  image=photo,
                  compound=CENTER,
                  font=('华文黑体', 40),
                  fg='blue')
the_label.pack()


mainloop()