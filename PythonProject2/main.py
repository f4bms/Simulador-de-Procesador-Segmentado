import sys
from proce import *
from lw import *
from PyQt6 import QtCore, QtGui, QtWidgets, uic

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    uic.loadUi("untitled.ui", window)

    interval = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0

    procesador = Procesador(intv= interval)

    # Setup: x2 = 10, memoria[14] = 99
    procesador.regFile.reg[2] = 10
    procesador.dataMem.memory[14] = 99

    procesador.loadInstr(LW(rd=1, imm=4, rs1=2, proce=procesador))
    procesador.execute()


    window.show()

    sys.exit(app.exec())