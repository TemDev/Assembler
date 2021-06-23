import instruction as syntax  # Needed to access the HEXTOFUNCTIONDICT dictionary
from tkinter import *


class Interpreter:
    def __init__(self, master, runFreq, args):
        self.master = master
        self.runFreq = runFreq
        self.args = args
        self.freq = 1

    def execute(self, stepFlag):
        if self.args["RAM"][int(self.args["PC"],
                                16)] in syntax.inverse:  # Checking if the opcode exists in the dictionary before calling the method
            if not self.args["halt"] and not self.args[
                "stop"]:  # Checking if this opcode can be executed in the first place
                function = syntax.inverse[self.args["RAM"][int(self.args["PC"],
                                                               16)]]  # (self.args) #Calls the respective method for the opcode that the PC is pointing at, passing the dictionary in as a parameter,16(conversion of base) in this reference mean HEX,self.args["RAM"] is thhe whole ram block 256
                methodToCall = getattr(syntax, function)
                methodToCall(self.args)
                self.updateArgs(self.args)  # Returning updated arguments after the execution
                if not stepFlag:  # Checking if we can schedule the next call to execute
                    self.master.after(self.runFreq, lambda: self.execute(stepFlag))
            elif self.args["halt"]:  # In the event that martin has an error on his side or code has finished
                if self.args["errorMsg"] == "Executing...":  # Means code has finished
                    self.args["errorMsg"] = "Execution successful."
                self.displayError(self.args[
                                      "errorMsg"])  # If above was not met, the error message will not be modified, and so martin's error message will be shown.
            elif self.args["stop"]:  # If we couldn't execute it, means stop flag was set
                self.args["errorMsg"] = "User initiated stop."
                self.displayError(self.args["errorMsg"])
        else:  # Undefined opcode case
            self.args["halt"] = True  # Setting the halt flag as we have got to an invalid opcode
            self.args["errorMsg"] = f"Opcode {self.args['RAM'][int(self.args['PC'], 16)]} is undefined."
            self.displayError(self.args["errorMsg"])

        return self.args  # We need to return the dictionary in any case

    def updateArgs(self, args):  # Stub function which will be overwritten by Adi's updateArgs method
        print(self.args)

    def displayError(self, errorMsg):  # Stub function which will be overwritten by Adi's displayError method
        print(self.args["errorMsg"])

    def stop(self):  # Method to be called in the event that the stop button is pressed
        self.args["stop"] = True

    def start(self):  # Method to be called in the event that run is pressed after a user stop.
        self.args["stop"] = False
        self.args["errorMsg"] = "Executing..."
        self.displayError(self.args["errorMsg"])
        self.args["Freq"] = self.freq

    def reinitArgs(self, args):  # Needs to reinitialise the args dictionary. Can reuse RAM, master, runFreq.
        # Called whenever assemble is pressed as we need to somehow keep the initial state of RAM before it was modifed
        self.args = args
        self.args["Freq"] = self.freq

    def changeFreq(self, newFreq):
        self.runFreq = newFreq
        self.args["errorMsg"] = f"Execution frequency has been set to {newFreq}ms between instructions."
        self.displayError(self.args["errorMsg"])

    def set_freq(self, freq):
        self.runFreq = int(0.5 ** (freq - 1) * 1000)
        self.freq = 2 ** (freq - 1)


if __name__ == "__main__":
    root = Tk()
    args = {
        "RAM": ["00" for i in range(256)],
        "ACC": "00",
        "PC": "00",
        "IX": "00",
        "ZMP": False,
        "halt": False,
        "errorMsg": None
    }
    args["RAM"][0] = "0A"
    args["RAM"][1] = "64"
    args["RAM"][2] = "2B"

    inter = Interpreter(root, 1, args)
    inter.execute(True)

    root.mainloop()

"""PLAN:

class Interpreter:
    constructor(RAM, symbolTable):
        self.RAM = RAM
        self.symbolTable = symbolTable
        self.PC = 0
        self.registers = {
            "EE": 0, #ACC
            "FF": 0  #IX
        }
        self.haltFlag = False

    executeMethod():
        self.RAM, self.PC, self.registers, self.haltFlag = HEXTOFUNCTIONDICT[self.RAM[self.PC]](self.PC, self.RAM, self.registers) #We call the syntax.py methods, which return RAM, PC and registers
        return self.RAM, self.PC, self.registers, self.haltFlag #This gets returned to whatever called it so it can be displayed




#Not sure where this method would go so here's a rough plan of what I'm thinking

Put this in main

interpreter = Interpreter(RAM, symbolTable) #Creating interpreter object here
haltFlag = False


interpretMethod(stepFlag):
    RAM, PC, registers, haltFlag = interpreter.executeMethod()
    if not(stepFlag): #We can by default have some step flag which indicates if we are stepping or not
        #SCHEDULE CALL HERE

"""
