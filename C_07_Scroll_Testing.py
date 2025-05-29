import tkinter as tk
from tkinter.scrolledtext import ScrolledText

root = tk.Tk()

text = ScrolledText(root, state='disable')
text.pack(fill='both', expand=True)

frame = tk.Frame(text)
text.window_create('1.0', window=frame)

for number in range(30):
    l = tk.Label(frame, text='Input:', bg='red')
    l.grid(row=number, column=0, sticky='we')
    l = tk.Label(frame, text=number, bg='green')
    l.grid(row=number, column=1, sticky='we')

root.mainloop() 