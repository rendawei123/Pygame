from tkinter import *

root = Tk()

group = LabelFrame(root, text='你认为最漂亮的是：')
group.pack(padx=10, pady=10)

girls = (('王昭君', 1), ('西施', 2), ('貂蝉', 3), ('杨玉环', 4), ('李师师', 5), ('佟湘玉', 6))
v = IntVar()
v.set(1)

for each, num in girls:
    b = Radiobutton(group, text=each, variable=v, value=num)
    b.pack(anchor=W)

mainloop()
