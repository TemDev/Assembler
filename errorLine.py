try:
    from Tkinter import *
except:
    from tkinter import *


class ErrorBar:
    def __init__(self, master, r, c):
        self.master = master
        self.frame = Frame(master, relief="groove", bd=3)
        self.frame.grid(row=r, column=c, sticky=W, pady=10)
        self.fontSize = 12
        self.font = ("Consolas", self.fontSize)
        self.text = "Don't worry my friend, you have no errors....... yet"
        self.textBar = Label(self.frame,
                             text=self.text,
                             font=self.font,
                             fg="black",
                             width=50,
                             justify=LEFT,
                             wraplength=600,
                             bg="white",
                             anchor=W,
                             relief="groove"
                             )
        self.textBar.grid(row=0, column=0, sticky=W)

    def update(self, errMsg, *args):
        self.textBar.configure(text=errMsg)
        self.master.update()


if __name__ == "__main__":
    root = Tk()
    bar = ErrorBar(root, 0, 0)

    root.mainloop()
