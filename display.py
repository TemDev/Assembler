try:
    from Tkinter import *
except:
    from tkinter import *

import copy


def denHex(x):
    # Converts a denary integer into a formatted hexadecimal string
    l = hex(x)[2:].upper()
    if len(l) == 1:
        l = "0" + l
    return l


class Display:
    # This is a display widget

    def __init__(self, master, r, c):
        self.master = master
        self.font = ("consolas", 12)
        self.frame = Frame(self.master, bg="white")
        self.frame.grid(row=r, column=c)
        self.ramFrame = Frame(self.frame, borderwidth=5, relief="groove", bg="white")
        self.ramFrame.grid(row=1, column=0)
        self.regFrame = Frame(self.frame, borderwidth=5, relief="groove", bg="white")
        self.regFrame.grid(row=0, column=0, sticky=W)
        self.ram = [denHex(0) for i in range(256)]  # a list of integers
        self.textArray = []  # a list of label objects
        self.convFunc = lambda x: x
        self.lineNums = []  # a list containing line number labels in display
        self.nSys = ["Hex"]
        self.registers = {
            "PC": "00",
            "ACC": "00",
            "IX": "00",
            "ZMP": False,
            "halt": False,
            "Freq": 1
        }
        self.regArray = {}
        j = 0
        for reg in self.registers:
            if reg == "ZMP" or reg == "halt":
                if self.registers[reg]:
                    t = "TRUE"
                else:
                    t = "FALSE"
                self.regArray[reg + str("-label")] = Label(self.regFrame, text=reg, font=self.font, width=5, bg="white")
                self.regArray[reg + str("-label")].grid(row=0, column=j, padx=30)
                self.regArray[reg] = Label(self.regFrame, text=t, font=self.font, bg="white")
                self.regArray[reg].grid(row=1, column=j)
            else:
                self.regArray[reg + str("-label")] = Label(self.regFrame, text=reg, font=self.font, width=5, bg="white")
                self.regArray[reg + str("-label")].grid(row=0, column=j)
                self.regArray[reg] = Label(self.regFrame, text=self.convFunc(self.registers[reg]), font=self.font,
                                           bg="white")
                self.regArray[reg].grid(row=1, column=j)
            j += 1
        self.regArray["PC-label"]["bg"] = "cyan"

        self.hgList = ["white" for i in range(256)]

        # Loop to initialise the textArray
        j = 0
        for i in range(256):
            if i % 16 == 0:
                self.lineNums.append(Label(self.ramFrame, text=denHex(i), font=self.font, fg="blue", bg="white"))
                self.lineNums[j].grid(row=j, column=0)
                j += 1
            self.textArray.append(
                Label(self.ramFrame, text=self.convFunc(self.ram[i]), font=self.font, width=4, bg="white"))
            self.textArray[i].grid(row=j - 1, column=i % 16 + 1)

    def update(self):
        for reg in self.registers:
            if reg == "ZMP" or reg == "halt":
                if self.registers[reg]:
                    t = "TRUE"
                else:
                    t = "FALSE"
                self.regArray[reg]["text"] = t
            else:
                self.regArray[reg]["text"] = self.convFunc(self.registers[reg])

        for i, data in enumerate(self.ram):
            self.textArray[i]["text"] = self.convFunc(data)
        for i, each in enumerate(self.lineNums):
            each["text"] = self.convFunc(denHex(i * 16))

    def numSys(self, numSys):
        if numSys == "Hex":
            self.convFunc = lambda x: x
            self.nSys[0] = "Hex"
        elif numSys == "Dec":
            self.convFunc = lambda x: "{:03d}".format(int(x, 16))
            self.nSys[0] = "Dec"
        self.update()

        pass

    def remove_hg(self, ind):
        self.textArray[ind]["bg"] = self.hgList[ind]
        pass

    def add_hg(self, ind, clr):
        self.textArray[ind]["bg"] = clr
        pass

    def updateArgs(self, args, assem=None):
        if assem != None:
            for i, val in enumerate(assem):
                if val == "OPCODE":
                    self.hgList[i] = "light Blue"
                    self.remove_hg(i)
                elif val == "DB":
                    self.hgList[i] = "orchid1"
                    self.remove_hg(i)
                else:
                    self.hgList[i] = "white"
                    self.remove_hg(i)

        arggs = copy.deepcopy(args)
        self.remove_hg(int(self.registers["PC"], 16))
        for reg in self.registers:
            self.registers[reg] = arggs[reg]
        self.add_hg(int(self.registers["PC"], 16), "cyan")
        self.ram = arggs["RAM"]
        self.update()

        pass


def test(x, args):
    n = int(args["PC"], 16)
    n = (n - 1) % 256
    args["PC"] = denHex(n)
    print(denHex(n))
    k = ["none" for i in range(256)]
    k[0] = "OPCODE"
    k[1] = "DB"
    x.updateArgs(args, k)


if __name__ == "__main__":
    root = Tk()
    d = Display(root, 0, 0)
    dic = {
        "PC": "13",
        "IX": "13",
        "ACC": "23",
        "ZMP": False,
        "halt": False,
        "RAM": ["01" for _ in range(256)]
    }
    d.updateArgs(dic)
    testBtn = Button(root, text="test", command=lambda: test(d, dic))
    testBtn.grid(row=0, column=1)

    root.mainloop()
