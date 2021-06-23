try:
    from Tkinter import *
    from Tkinter import FileDialog
    from Tkinter import MessageBox
except:
    from tkinter import *
    from tkinter import filedialog
    from tkinter import messagebox
from collections import OrderedDict
from instruction import inverse, SPECIALOPERANDS
import os


class ToolBar:
    def __init__(self, master):
        self.master = master
        self.toolbar = Menu(self.master)
        self.bars = OrderedDict()
        self.verStr = "None"

        # create all the label for the code
        self.bars["File"] = Menu(self.toolbar, tearoff=False)
        self.bars["Tools"] = Menu(self.toolbar, tearoff=False)
        self.bars["View"] = Menu(self.toolbar, tearoff=False)
        self.bars["About"] = Menu(self.toolbar, tearoff=False)
        self.bars["Exit"] = Menu(self.toolbar, tearoff=False)  # implement exit button into the menu bar

        self.numSys = Menu(self.bars["View"], tearoff=False)
        self.bars["View"].add_cascade(label="NumberSystem", menu=self.numSys)
        self.numSys.add_command(label="Decimal", command=lambda: self.set_numSys("Dec"))
        self.numSys.add_command(label="Hexadecimal", command=lambda: self.set_numSys("Hex"))

        for each in self.bars:
            self.toolbar.add_cascade(label=each, menu=self.bars[each])
        self.master.config(menu=self.toolbar)

        self.bars["File"].add_command(label="Save", command=lambda: self.pop_save())  # Focus here link to pop save
        self.bars["View"].add_command(label="Opcodes and Instructions", command=lambda: self.pop_opcode())
        self.bars["File"].add_command(label="Load", command=lambda: self.pop_load())  # this one link to pop load
        self.bars["Tools"].add_command(label="Symbol Table", command=lambda: self.pop_symbol())
        self.freq = Menu(self.bars["Tools"], tearoff=False)
        self.bars["Tools"].add_cascade(label="Frequency", menu=self.freq)
        self.bars["Exit"].add_command(label="Exit", command=lambda: self.exit())  # exit the programme
        # this set the frequency of the assembler
        self.freq.add_command(label="1 HZ", command=lambda: self.set_freq(1))
        self.freq.add_command(label="2 HZ", command=lambda: self.set_freq(2))
        self.freq.add_command(label="4 HZ", command=lambda: self.set_freq(3))
        self.freq.add_command(label="8 HZ", command=lambda: self.set_freq(4))
        self.freq.add_command(label="16 HZ", command=lambda: self.set_freq(5))
        self.freq.add_command(label="32 HZ", command=lambda: self.set_freq(6))

        self.bars["About"].add_command(label="Info", command=self.pop_info)

        self.sym = {}

    def get_text(self):
        text = ""
        return text

    def exit(self):
        self.master.destroy()

    def setFile(self, value):  # called from CurSelect
        self.fileNameText.delete(1.0, END)  # Delete the old file
        self.fileNameText.insert(END, value)  # insert the new file

    def CurSelect(self, event):  # called from pop saved
        try:
            self.value = self.savedFileDisplay.get(self.savedFileDisplay.curselection())
            self.setFile(self.value)
        except:
            print("")

    def writeFile(self, fileName):
        self.text = self.get_text()
        self.f = open(fileName, "w")
        self.f.write(self.text)
        self.f.close()

    def checkFormat(self, fileName):
        self.invalidChar = ["/", ":", "|", "?", "*", ">", "<"]
        self.validFlag = True
        i = 0
        while i <= len(self.invalidChar) - 1 and self.validFlag == True:
            if self.invalidChar[i] in fileName:
                messagebox.showerror("Invalid filename", "You can't have /,:,|,?,*,>,< in the name")
                self.validFlag = False
            i += 1

        if self.validFlag == True and fileName[-4:] == ".txt":
            self.writeFile(fileName)

        elif self.validFlag == True:
            self.writeFile(fileName + ".txt")

    def pop_save(self):
        # change path
        path = os.path.abspath("")
        dir_path = os.path.dirname(os.path.realpath(__file__)) + "/Files"
        os.chdir(dir_path)
        path = os.path.abspath("./")

        # start of file dialog design Window
        self.existingFile = []
        for fileName in os.listdir(path):  # load existing file into the list
            self.existingFile.append(fileName)

        self.file = filedialog.asksaveasfilename(initialdir=path, title="Select file",
                                                 filetypes=(("text file", "*.txt"), ("all files", "*.*")))
        self.file = self.file.replace("/", "\\")
        self.file = self.file.replace(path + "\\", "")

        if self.file + ".txt" not in self.existingFile:
            self.checkFormat(self.file)
        else:
            messagebox.showerror("Existing file", "There is an existing file with same name in the directory")

    def pop_load(self):
        path = os.path.abspath("")
        dir_path = os.path.dirname(os.path.realpath(__file__)) + "/Files"
        os.chdir(dir_path)
        path = os.path.abspath("./")

        self.file = filedialog.askopenfilename(initialdir=path, title="Select file",
                                               filetypes=(("text file", "*.txt"), ("all files", "*.*")))
        self.load(self.file)

    def load(self, fileName):
        path = os.path.abspath("")
        dir_path = os.path.dirname(os.path.realpath(__file__)) + "/Files"
        os.chdir(dir_path)
        path = os.path.abspath("./")

        self.fileName = fileName
        self.f = open(self.fileName, "r")
        self.fileContent = self.f.read()
        self.writeText(self.fileContent)
        self.reset()

    def writeText(self, text):
        self.text = text

    def reset(self):

        pass

    def set_freq(self, freq):

        pass

    def update_sym(self, sym):
        self.sym = sym

    def conv(self, x):
        pass

    def pop_opcode(self):  # displays supported opcodes and instructions - 2.0i
        top = Toplevel()
        top.title("Opcodes & Instructions")
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        top.columnconfigure(1, weight=1)
        opcode = Label(top, text="Opcodes", font=("Consolas", 20), bd=1, relief="solid", anchor=CENTER,
                       justify=CENTER)
        opcode.grid(row=0, column=0, sticky=N + S)
        instruction = Label(top, text="Instructions", font=("Consolas", 20), bd=1, relief="solid", anchor=CENTER,
                            justify=CENTER)
        instruction.grid(row=0, column=1, sticky=N + S)
        row = 1
        for keys, values in inverse.items():
            opcodeLab = Label(top, text=keys, bd=1, relief="solid", font=("Consolas", 18), anchor=CENTER,
                              justify=CENTER)
            opcodeLab.grid(row=row, column=0, sticky=N + E + S + W)
            istructLab = Label(top, text=values, bd=1, relief="solid", font=("Consolas", 18), anchor=CENTER,
                               justify=CENTER)
            istructLab.grid(row=row, column=1, sticky=N + E + S + W)
            row += 1
        specialValues = list(SPECIALOPERANDS.keys())
        specialKeys = list(SPECIALOPERANDS.values())
        for i in range(len(SPECIALOPERANDS)):
            opcodeLab = Label(top, text=specialKeys[i], bd=1, relief="solid", font=("Consolas", 18), anchor=CENTER,
                              justify=CENTER)
            opcodeLab.grid(row=row, column=0, sticky=N + E + S + W)
            istructLab = Label(top, text=specialValues[i], bd=1, relief="solid", font=("Consolas", 18), anchor=CENTER,
                               justify=CENTER)
            istructLab.grid(row=row, column=1, sticky=N + E + S + W)
            row += 1

    def pop_symbol(self):  # passing in a func from display in main
        keyList = list(self.sym.keys())
        valList = list(self.sym.values())
        if self.nSys[0] == "Hex":
            self.conv = lambda x: x
        elif self.nSys[0] == "Dec":
            self.conv = lambda x: "{:03d}".format(int(x, 16))

        top = Toplevel()
        top.title("Symbol Table")
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        top.columnconfigure(1, weight=1)
        labName = Label(top, text="Label Names", font=("Consolas", 23), bd=1, relief="solid", anchor=CENTER,
                        justify=CENTER)
        labName.grid(row=0, column=0, sticky=N + S)
        address = Label(top, text="Addresses", font=("Consolas", 23), bd=1, relief="solid", anchor=CENTER,
                        justify=CENTER)
        address.grid(row=0, column=1, sticky=N + S)
        r = 1
        for i in range(len(keyList)):
            keyLab = Label(top, text=keyList[i], bd=1, relief="solid", font=("Consolas", 18), anchor=CENTER,
                           justify=CENTER)
            keyLab.grid(row=r, column=0, sticky=N + E + S + W)
            valLab = Label(top, text=self.conv(valList[i]), bd=1, relief="solid", font=("Consolas", 18), anchor=CENTER,
                           justify=CENTER)
            valLab.grid(row=r, column=1, sticky=N + E + S + W)
            r += 1

        pass

    def assign_numSys(self, func):
        self.set_numSys = func
        pass

    def setVersion(self, ver):
        self.verStr = ver

    def pop_info(self):
        popup = Toplevel()
        popup.title("Credits")
        font1 = ("Times", 14, "bold")
        font2 = ("Consolas", 12, "italic")
        font3 = ("Times", 12)
        lines = [
            ("CIE Assembly Virtual Machine", font1),
            ("This program is designed to run the assembly code of CIE A-level specification", font3),
            ("and aid students in their studies of Computer Science.", font3),
            ("Original version made by The CompSciGang of Oxford International College in 2019", font3),
            ("Project led by:", font1),
            ("Nicholas Mulvey", font2),
            ("The A2 class of 2019:", font1),
            ("Adi Bozzhanov, Laveen Chandnani", font2),
            ("Tanthun Assawapitiyaporn, Martin Lee", font2),
            ("The AS class of 2020:", font1),
            ("Sittivit (Ken) Bunlungsak, Huixiang (Harry) Kong", font2),
            ("Mountain Cheng, Yat Long (Jerry) Kam", font2),
            ("Maria Davydova, Tamirlan Mamutov", font2),
            ("Illia Derevianko, Temirlan Sergazin", font2),
            ("Version: " + self.verStr, font1)
        ]
        labels = []

        for i, line in enumerate(lines):
            labels.append(Label(popup, text=line[0], font=line[1], wraplength=550))
            labels[i].grid(row=i, column=0)

        popup.mainloop()

        pass


if __name__ == "__main__":
    root = Tk()
    tb = ToolBar(root)

    root.mainloop()
