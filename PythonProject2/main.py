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

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    uic.loadUi("untitled.ui", window)

    interval = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0

    procesador = Procesador(intv= interval)

    procesador.regFile.reg[5] = 0b1100  

    procesador.loadInstr(ANDI(6, 5, 0b1010, procesador))
    procesador.execute()


    window.show()

    sys.exit(app.exec())

#ya está: sw, lw, add, addi, sub, beq, or, and, xor, andi
