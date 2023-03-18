import tkinter as tk
from tkinter import filedialog, Text
import os
import matplotlib.pyplot as pp
import numpy as np

root = tk.Tk()

canvas = tk.Canvas(root, height=3000, width=3000, bg="#263d42")
canvas.pack()

frame = tk.Frame(root)
frame.place(relwidth=0.8, relheight=0.8, rely=0.1, relx=0.1)

data = np.loadtxt(fname='test.txt', delimiter=',')
print(data)
root.mainloop()

