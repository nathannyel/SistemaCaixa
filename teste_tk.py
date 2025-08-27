import tkinter as tk

root = tk.Tk()
root.title("Teste Tkinter")
root.geometry("300x200")

label = tk.Label(root, text="Se você vê isso, Tkinter funciona!")
label.pack(pady=50)

root.mainloop()
