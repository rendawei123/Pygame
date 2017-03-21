from tkinter import *

root = Tk()
text_label = Label(root, text='未满十八周岁者\n禁止观看!', justify=LEFT, padx=10)
text_label.pack(side=LEFT)

photo = PhotoImage(file='/Users/David/Desktop/practice/123.gif')
image_label = Label(root, image=photo)
image_label.pack(side=RIGHT)

mainloop()
