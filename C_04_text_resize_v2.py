import tkinter as tk
import tkinter.font as font

def resize_text(event, width):
    if width > 0: # Avoid issues when width is not yet determined
        font_size = int(width / 5)  # Adjust the divisor as needed
        new_font = font.Font(family="Helvetica", size=font_size, weight="bold")
        button.config(font=new_font)

root = tk.Tk()

button = tk.Button(root, text="Resize Me", padx=10, pady=10)
button.pack(fill="both", expand=True)

root.bind("<Configure>", resize_text)

root.mainloop()