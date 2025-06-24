from proce import *
from lw import *
from sw import *
from add import *
from addi import *
from sub import *
from beq import *
from and_ import *
from or_ import *
from xor_ import *
from andi import *

class HazardProcessor:
    def __init__(self, interval=1.0):
        self.interval = interval
        self.processor = Procesador(intv=interval, enable_hazards=True)

    def load_instructions(self):
        """Carga un programa de prueba que genera hazards"""
        instructions = [
            LW(1, 10, 0, self.processor),
            ADD(2, 1, 1, self.processor),
            SW(2, 0, 30, self.processor),
            BEQ(1, 2, 8, self.processor),
            ADDI(3, 1, 5, self.processor),
            AND(4, 1, 2, self.processor),
            OR(5, 1, 2, self.processor),
            XOR(6, 1, 2, self.processor),
            ANDI(7, 1, 0b1010, self.processor),
            SUB(8, 2, 1, self.processor)
        ]
        for instr in instructions:
            self.processor.loadInstr(instr)

    def run(self):
        """Ejecuta el procesador en un hilo separado"""
        thread = threading.Thread(target=self.processor.execute)
        thread.start()
        thread.join()
