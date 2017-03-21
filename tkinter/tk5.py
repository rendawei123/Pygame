from tkinter import *

root = Tk()

girls = ['王昭君', '西施', '杨玉环', '貂蝉']
v = []

for each in girls:
    v.append(IntVar)
    c = Checkbutton(root, text=each, variable=v[-1])
    c.pack(anchor=W)

mainloop()