try:
    from Tkinter import *
except:
    from tkinter import *


def denHex(x):
    # Converts a denary integer into a formatted hexadecimal string
    l = hex(x)[2:].upper()
    if len(l) == 1:
        l = "0" + l
    return l


class InBar:
    def __init__(self, master, r, c):
        self.master = master
        self.frame = Frame(master, borderwidth=5, relief="groove", bg="white")
        self.frame.grid(row=r, column=c, sticky=W)
        self.fontSize = 12
        self.font = ("Consolas", self.fontSize)
        self.label = Label(self.frame, text="Input: ", font=self.font, width=8, bg="white")
        self.label.grid(row=0, column=0)
        self.strVar = StringVar()
        self.entry = Entry(self.frame, textvariable=self.strVar, width=10, justify=LEFT, font=self.font,
                           state="disabled", bg="white")
        self.entry.grid(row=0, column=1)
        self.running = False
        # self.enterButton = Button(self.frame,text="Enter",font=self.font,width=7,command=self.enterInput)
        # self.enterButton.grid(row=0,column=2)

    def setInState(self, state):
        self.running = state
        pass

    def trigger(self, args):
        self.args = args
        self.entry["state"] = "normal"
        self.label["bg"] = "orange"
        self.enterButton = Button(self.frame, text="Enter", font=self.font, width=7, command=self.enterInput)
        self.enterButton.grid(row=0, column=2)

    def enterInput(self):
        char = self.strVar.get()
        self.args["ACC"] = denHex(ord(char))
        self.args["inFlag"] = False
        self.enterButton.destroy()
        self.entry["state"] = "disabled"
        self.label["bg"] = "white"
        self.strVar.set("")
        self.execute(self.running)

    def execute(self, f):
        pass


if __name__ == "__main__":
    root = Tk()
    inBar = InBar(root, 0, 0)
