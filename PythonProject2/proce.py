import threading
import time

from intsrMem import *
from reg import *
from regFile import *
from alu import *
from dataMem import *

class Procesador:
    def __init__(self, intv = 1):
        self.intv = intv
        self.intrMem = instrMemory()
        self.regFile = regFile()
        self.alu = ALU()
        self.dataMem = dataMemory()
        self.instr_reg = Registr()
        self.regRegFile = Registr()
        self.alu_reg = Registr()
        self.reg_data = Registr()

        #para lo de los cuadritos de abajo:
        self.cycles = 0
        self.pc = 0
        self. instrRetired = 0
        self.pipel_stage = ["", "", "", "", ""]
        self.time = 1

    def loadInstr(self, instr):
        self.intrMem.memory.append(instr)

    def execute(self):
        start = True
        timer = time.time()
        while start:
            self.cycles += 1
            start = False


            #wb
            if self.reg_data.instr is not None:
                start = True
                self.reg_data.instr.execute()
                self.pipel_stage[4] = "WB"
                self.reg_data.clear()
                self.instrRetired +=1
            else:
                self.pipel_stage[4] = ""

            #mem
            if self.alu_reg.instr is not None:
                start = True
                self.alu_reg.instr.execute()
                self.pipel_stage[3] = "MEM"
                self.reg_data.instr = self.alu_reg.instr
                self.alu_reg.clear()
            else:
                self.pipel_stage[3] = ""

            #EX
            if self.regRegFile.instr is not None:
                start = True
                self.regRegFile.instr.execute()
                self.pipel_stage[2] = "EX"
                self.alu_reg.instr = self.regRegFile.instr
                self.regRegFile.clear()

            else:
                self.pipel_stage[2] = ""

            #ID
            if self.instr_reg.instr is not None:
                start = True
                self.instr_reg.instr.execute()
                self.pipel_stage[1] = f"Instr {self.pc-1}"
                self.regRegFile.instr= self.instr_reg.instr
                self.instr_reg.clear()
            else:
                self.pipel_stage[1] = ""

            #IF
            if self.pc < len(self.intrMem.memory):
                start = True
                self.pipel_stage[0] = f"Instr {self.pc}"
                self.instr_reg.instr = self.intrMem.memory[self.pc]
                self.pc +=1

            else:
                self.pipel_stage[0] = ""

            completedTime = self.time
            if completedTime > 0:
                cpi = self.cycles / max(1, self.instrRetired)
                ipc = self.instrRetired / max(1, self.cycles)
                clock_rate = self.cycles / (completedTime * 1e9)
            else:
                cpi = ipc = clock_rate = 0

            #todo esto meter a la parte grafica




    








