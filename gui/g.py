import tkinter as tk

window = tk.Tk()

greeting = tk.Label(text="Hello, Tkinter")

label = tk.Label(
    text="hello, mr label",
    foreground="white",
    background="black"
)

label2 = tk.Label(
    text="Hello, Tkinter",
    fg="#000000",
    bg="#AA0000",
    width=10,
    height=10
)

button = tk.Button(
    text="Click Me",
    width=25,
    height=5,
    bg="red",
    fg="white"
)

label3 = tk.Label(text="Name")
entry = tk.Entry()

greeting.pack()
label.pack()
label2.pack()
button.pack()
label3.pack()
entry.pack()

window.mainloop()