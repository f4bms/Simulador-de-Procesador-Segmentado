import sys
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

from PyQt6 import QtCore, QtGui, QtWidgets, uic

class DualProcessor:
    def __init__(self, interval=1.0):
        self.interval = interval
        self.proc_with_hazard = Procesador(intv=interval, enable_hazards=True)
        self.proc_without_hazard = Procesador(intv=interval, enable_hazards=False)
        
    def load_instructions(self):
        # Ejemplo de programa que causa hazards
        instructions = [
            LW(1, 0, 100, self.proc_with_hazard),
            ADD(2, 1, 1, self.proc_with_hazard),
            SW(2, 0, 104, self.proc_with_hazard),
            BEQ(1, 2, 8, self.proc_with_hazard),
            ADDI(3, 1, 5, self.proc_with_hazard),
            AND(4, 1, 2, self.proc_with_hazard),
            OR(5, 1, 2, self.proc_with_hazard),
            XOR(6, 1, 2, self.proc_with_hazard),
            ANDI(7, 1, 0b1010, self.proc_with_hazard),
            SUB(8, 2, 1, self.proc_with_hazard)
        ]
        
        # Cargar las mismas instrucciones en ambos procesadores
        for instr in instructions:
            self.proc_with_hazard.loadInstr(instr)
            
            # Crear una copia para el procesador sin hazards
            instr_class = instr.__class__
            args = []
            for attr in ['rd', 'rs1', 'rs2', 'imm']:
                if hasattr(instr, attr):
                    args.append(getattr(instr, attr))
            args.append(self.proc_without_hazard)
            new_instr = instr_class(*args)
            self.proc_without_hazard.loadInstr(new_instr)

    def run(self):
        # Ejecutar ambos procesadores en threads separados
        thread_with = threading.Thread(target=self.proc_with_hazard.execute)
        thread_without = threading.Thread(target=self.proc_without_hazard.execute)
        
        thread_with.start()
        thread_without.start()
        
        thread_with.join()
        thread_without.join()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    uic.loadUi("untitled.ui", window)

    interval = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0

    dual_proc = DualProcessor(interval)
    dual_proc.load_instructions()
    
    # Configurar la interfaz gráfica
    # (Conectar los elementos de la UI con los procesadores)
    
    window.show()
    dual_proc.run()
    sys.exit(app.exec())

#ya está: sw, lw, add, addi, sub, beq, or, and, xor, andi
