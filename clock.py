# Minimiohjelma-esimerkki
import tkinter as tk

root = tk.Tk()
root.geometry("400x300")

btn = tk.Button(root, text="Testaa", font=("Arial", 20), width=15, height=3)
btn.pack(pady=100)

def on_enter(event):
    root.config(cursor="hand1")   # tai "fleur", "pirate" jne.

def on_leave(event):
    root.config(cursor="")

btn.bind("<Enter>", on_enter)
btn.bind("<Leave>", on_leave)

root.mainloop()