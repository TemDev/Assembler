try:
    from Tkinter import *
except:
    from tkinter import *


class outBar:
    def __init__(self, master, r, c):
        self.master = master
        self.frame = Frame(master, borderwidth=5, relief="groove", bg="white")
        self.frame.grid(row=r, column=c, sticky=W)
        self.fontSize = 12
        self.font = ("Consolas", self.fontSize)
        self.text = ""
        self.textBar2 = Label(self.frame,
                              text="Output: ",
                              font=self.font,
                              width=8,
                              bg="white")
        self.textBar2.grid(row=0, column=0)

        self.textBar = Label(self.frame,
                             text=self.text,
                             font=self.font,
                             fg="black",
                             width=20,
                             justify=LEFT,
                             bg="white"
                             )
        self.textBar.grid(row=0, column=1)
        '''
        self.clearButton = Button(self.frame,
                            text = "Clear",
                            font = self.font,
                            command = self.clearBar,
                            width = 7)
        self.clearButton.grid(row = 0,column = 2)
        '''

    def out(self, text):
        self.text = self.text + text
        self.textBar.configure(text=self.text)

    def clearBar(self):
        self.textBar.configure(text="")
        self.text = ""


if __name__ == "__main__":
    root = Tk()
    outBar = outBar(root, 0, 0)
    # outBar.out("xxxx")

    root.mainloop()
