try:
    from Tkinter import *
except:
    from tkinter import *
import instruction as syntax
from toolbar import *
from interpreterControls import *
from editor import *
from display import *
from errorLine import *
from assembler import *
from outBar import *
from inBar import *
from interpreter import *

if __name__ == "__main__":
    VERSION = "2.0I"
    root = Tk()
    root.title("CIE Assembler virtual machine")
    # https://stackoverflow.com/questions/30965033/python-tkinter-application-fit-on-screen
    width, height = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry('%dx%d+0+0' % (width, height))
    root["bg"] = "white"
    root.resizable(True, True)

    asem = Assembler()
    interpreter = Interpreter(root, 1000, asem.args)
    asem.init_RAM()
    toolBar = ToolBar(root)
    editButtons = InterpreterControls(root, 0, 0)
    displayFrame = Frame(root, bg="white")
    displayFrame.grid(row=1, column=1, sticky=N)
    editor = Editor(root, 1, 0)
    inputBar = InBar(displayFrame, 2, 0)
    outBar = outBar(displayFrame, 1, 0)
    display = Display(displayFrame, 0, 0)
    errorBar = ErrorBar(displayFrame, 3, 0)

    # Connecting things together
    syntax.outStub = outBar.out
    syntax.inStub = inputBar.trigger
    editor.report = errorBar.update
    toolBar.setVersion(VERSION)
    toolBar.assign_numSys(display.numSys)
    toolBar.nSys = display.nSys
    toolBar.set_freq = interpreter.set_freq
    toolBar.reset = editButtons.reset
    inputBar.execute = interpreter.execute

    interpreter.updateArgs = display.updateArgs
    interpreter.displayError = errorBar.update
    editButtons.update_sym = toolBar.update_sym

    editButtons.assign_Functions(
        editor.lexical_analysis,
        asem.passThrough,
        display.updateArgs,
        errorBar.update,
        interpreter.reinitArgs,
        interpreter.execute,
        inputBar.setInState,
        outBar.clearBar,
        lambda: display.updateArgs({
            "RAM": ["00" for i in range(255)],
            "PC": "00",
            "ACC": "00",
            "IX": "00",
            "ZMP": False,
            "halt": False,
            "inFlag": False,
            "stop": False,
            "Freq": interpreter.freq
        },
            ["blank" for i in range(256)]
        ),
        interpreter.stop,
        interpreter.start
    )
    toolBar.get_text = editor.get_text
    toolBar.writeText = editor.insert_text

    root.mainloop()
