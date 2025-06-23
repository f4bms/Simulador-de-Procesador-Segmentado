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
from PyQt6.QtCore import QTimer


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("sim.ui", self)
        
        # Configuración inicial
        self.interval = 1.0
        self.procesador = Procesador(intv=self.interval)
        self.procesador.regFile.reg[5] = 0b1100
        
        # Cargar instrucciones de ejemplo
        self.load_sample_instructions()
        
        # Conectar botones
        self.exeCompleteButton.clicked.connect(self.execute_complete)
        self.exeTimerButton.clicked.connect(self.execute_timed)
        self.exeStepsButton.clicked.connect(self.start_step_mode)
        self.stepButton.clicked.connect(self.execute_step)
        self.pushButton.clicked.connect(self.show_memory)
        
        # Configurar selector de tiempo
        self.timeSelector.setValue(1.0)
        self.timeSelector.valueChanged.connect(self.update_cycle_time)
        
        # Timer para actualización de la interfaz
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_ui)
        self.update_timer.start(100)  # Actualizar cada 100ms
        
        # Estado inicial
        self.step_mode = False
        self.update_ui()

    def load_sample_instructions(self):
        """Carga instrucciones de ejemplo en el procesador"""
        self.procesador.loadInstr(ANDI(6, 5, 0b1010, self.procesador))
        # Agregar más instrucciones de ejemplo si es necesario
        # self.procesador.loadInstr(ADD(7, 6, 5, self.procesador))
        # self.procesador.loadInstr(SW(7, 0, 10, self.procesador))

    def update_cycle_time(self, value):
        """Actualiza el tiempo por ciclo en modo temporizado"""
        self.interval = value
        self.procesador.cycle_time = value

    def execute_complete(self):
        """Ejecuta todas las instrucciones de una vez"""
        self.procesador.set_execution_mode("complete")
        self.procesador.start_execution()
        self.update_ui()

    def execute_timed(self):
        """Ejecuta las instrucciones con temporización"""
        self.procesador.set_execution_mode("timed", self.interval)
        self.procesador.start_execution()
        self.update_ui()

    def start_step_mode(self):
        """Inicia el modo paso a paso"""
        self.step_mode = True
        self.procesador.set_execution_mode("step")
        self.procesador.start_execution()
        self.update_ui()

    def execute_step(self):
        """Ejecuta un paso en el modo paso a paso"""
        if self.step_mode:
            self.procesador.step()
        self.update_ui()

    def show_memory(self):
        """Muestra el contenido de la memoria"""
        # Implementar lógica para mostrar la memoria
        pass

    def update_ui(self):
        """Actualiza todos los elementos de la interfaz de usuario"""
        # Actualizar estadísticas
        self.cycleValueLabel.setText(str(self.procesador.cycles))
        self.timeValueLabel.setText(f"{self.procesador.time:.2f}")
        self.pcValueLabel.setText(str(self.procesador.pc))
        
        # Actualizar pipeline
        self.update_pipeline_display()
        
        # Actualizar registros y memoria
        self.update_registers_table()
        self.update_instructions_table()
        
        # Actualizar componentes activos
        self.update_active_components()

    def update_pipeline_display(self):
        """Actualiza la visualización gráfica de las etapas del pipeline"""
        # Colores para los estados
        executing_color = "rgb(0, 255, 0)"  # Verde para etapa activa
        stalled_color = "rgb(255, 0, 0)"    # Rojo para etapa detenida
        normal_color = "rgb(255, 255, 255)" # Blanco para etapa inactiva
        
        # Obtener las etapas del pipeline del procesador
        pipeline_stages = getattr(self.procesador, "pipel_stage", ["", "", "", "", ""])
        
        # Mapeo de labels para cada etapa del pipeline
        stage_labels = [
            self.white1Label,  # IF
            self.white2Label,  # ID
            self.white3Label,  # EX
            self.white4Label,  # MEM
            self.white5Label   # WB
        ]
        
        # Actualizar cada label según el estado de la etapa
        for i, (stage, label) in enumerate(zip(pipeline_stages, stage_labels)):
            if stage:  # Si hay instrucción en esta etapa
                # Verificar si hay riesgo/stall (podrías agregar esta lógica en tu procesador)
                is_stalled = getattr(self.procesador, f"stage_{i}_stalled", False)
                
                if is_stalled:
                    label.setStyleSheet(f"background-color: {stalled_color};")
                else:
                    label.setStyleSheet(f"background-color: {executing_color};")
                
                # Opcional: Mostrar nombre de la instrucción (necesitarías labels adicionales)
                # self.update_stage_text(i, stage)
            else:
                label.setStyleSheet(f"background-color: {normal_color};")

    def update_registers_table(self):
        """Actualiza la tabla de registros"""
        model = QtGui.QStandardItemModel(32, 2)
        model.setHorizontalHeaderLabels(["Registro", "Valor"])
        
        for i in range(32):
            reg_item = QtGui.QStandardItem(f"x{i}")
            val_item = QtGui.QStandardItem(str(self.procesador.regFile.reg[i]))
            model.setItem(i, 0, reg_item)
            model.setItem(i, 1, val_item)
        
        self.tableView.setModel(model)
        self.tableView.resizeColumnsToContents()

    def update_instructions_table(self):
        """Actualiza la tabla de instrucciones"""
        model = QtGui.QStandardItemModel(len(self.procesador.intrMem.memory), 1)
        model.setHorizontalHeaderLabels(["Instrucción"])
        
        for i, instr in enumerate(self.procesador.intrMem.memory):
            item = QtGui.QStandardItem(str(instr))
            model.setItem(i, 0, item)
        
        self.tableView_2.setModel(model)
        self.tableView_2.resizeColumnsToContents()

    def update_active_components(self):
        """Resalta los componentes activos en el pipeline"""
        # Definir colores
        active_color = "rgb(255, 255, 0)"  # Amarillo para activo
        inactive_color = "rgb(0, 0, 0)"     # Negro para inactivo
        
        # Memoria de Instrucciones
        mem_i_active = getattr(self.procesador.intrMem, "active", False)
        self.activeMemILabel.setStyleSheet(
            f"background-color: {active_color if mem_i_active else inactive_color};"
        )
        
        # Archivo de Registros
        reg_file_active = getattr(self.procesador.regFile, "active", False)
        self.activeRegFileLabel.setStyleSheet(
            f"background-color: {active_color if reg_file_active else inactive_color};"
        )
        
        # ALU
        alu_active = getattr(self.procesador.alu, "active", False)
        self.activeALULabel.setStyleSheet(
            f"background-color: {active_color if alu_active else inactive_color};"
        )
        
        # Memoria de Datos
        mem_d_active = getattr(self.procesador.dataMem, "active", False)
        self.activeMemDLabel.setStyleSheet(
            f"background-color: {active_color if mem_d_active else inactive_color};"
        )


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())