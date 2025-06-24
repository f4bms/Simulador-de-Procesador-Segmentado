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
from HazardProcessor import HazardProcessor

from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtGui import QAction


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("sim.ui", self)
        
        # Configuración inicial
        self.interval = 1.0
        self.procesador = Procesador(intv=self.interval)
        self.procesador2 = Procesador(intv=self.interval)
        
        # Configurar menú
        self.setup_menu()
        
        # Conectar botones
        self.exeCompleteButton.clicked.connect(self.execute_complete)
        self.exeTimerButton.clicked.connect(self.execute_timed)
        self.exeStepsButton.clicked.connect(self.start_step_mode)
        self.stepButton.clicked.connect(self.execute_step)
        self.memoryButton.clicked.connect(self.show_memory)

        self.proce1Combo.currentIndexChanged.connect(self.update_processor_config)
        self.proce2Combo.currentIndexChanged.connect(self.update_processor_config)
        
        # Configurar selector de tiempo
        self.timeSelector.setValue(1.0)
        self.timeSelector.valueChanged.connect(self.update_cycle_time)
        
        # Timer para actualización de la interfaz
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_ui)
        self.update_timer.start(100)
        
        self.update_processor_config()
        self.update_ui()

    def update_processor_config(self):

        index1 = self.proce1Combo.currentIndex()
        if index1 == 0:
            self.procesador.enable_branch_prediction(enabled=False)
        elif index1 == 1:
            self.procesador.enable_hazard_unit()
            self.procesador.enable_branch_prediction(enabled=False)
        elif index1 == 2:
            self.procesador.enable_branch_prediction(enabled=True, prediction_mode="always_not_taken")
        elif index1 == 3:
            self.procesador.enable_hazard_unit()
            self.procesador.enable_branch_prediction(enabled=True, prediction_mode="always_not_taken")

        index2 = self.proce2Combo.currentIndex()
        if index2 == 0:
            self.procesador2.enable_branch_prediction(enabled=False)
        elif index2 == 1:
            self.procesador2.enable_hazard_unit()
            self.procesador2.enable_branch_prediction(enabled=False)
        elif index2 == 2:
            self.procesador2.enable_branch_prediction(enabled=True, prediction_mode="always_not_taken")
        elif index2 == 3:
            self.procesador2.enable_hazard_unit()
            self.procesador2.enable_branch_prediction(enabled=True, prediction_mode="always_not_taken")

    def setup_menu(self):
        """Configura la barra de menú con opciones de archivo"""
        
        menubar = self.menuBar()
        
        # Menú Archivo
        file_menu = menubar.addMenu("&Archivo")
        
        # Acción para cargar instrucciones
        load_action = QAction("&Cargar instrucciones", self)
        load_action.setShortcut("Ctrl+O")
        load_action.triggered.connect(self.load_instructions_from_file)
        file_menu.addAction(load_action)
        
        # Acción para salir
        exit_action = QAction("&Salir", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)


    def load_instructions_from_file(self):
        """Abre un diálogo para seleccionar y cargar un archivo de instrucciones"""
        # Versión corregida para PyQt6
        file_name, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption="Cargar archivo de instrucciones",
            directory="",
            filter="Archivos de texto (*.txt);;Assembly RISCV (*.s);;Todos los archivos (*)",
            initialFilter="Assembly RISCV (*.s)"
        )
        
        if file_name:
            try:
                # Limpiar instrucciones existentes
                self.procesador.intrMem.memory.clear()
                self.procesador2.intrMem.memory.clear()
                self.procesador.pc = 0
                self.procesador2.pc = 0
                self.procesador.cycles = 0
                self.procesador2.cycles = 0
                self.procesador.instrRetired = 0
                self.procesador2.instrRetired = 0
                
                # Leer y cargar instrucciones
                with open(file_name, 'r') as file:
                    for line in file:
                        line = line.strip()
                        if line and not line.startswith('#'):  # Ignorar líneas vacías y comentarios
                            self.parse_and_load_instruction(line)
                
                QMessageBox.information(
                    self,
                    "Carga exitosa",
                    f"Instrucciones cargadas correctamente desde:\n{file_name}"
                )
                self.update_ui()
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error al cargar",
                    f"No se pudo cargar el archivo:\n{str(e)}"
                )

    def parse_and_load_instruction(self, line):
        """Convierte una línea de texto en una instrucción y la carga al procesador"""
        try:
            # Eliminar comentarios al final de la línea
            line = line.split('#')[0].strip()
            if not line:
                return
                
            parts = line.split()
            instr_type = parts[0].upper()
            
            if instr_type == "LW":
                # Formato: LW rd, offset(rs1)
                rd = self.parse_register(parts[1].strip(','))
                offset, rs1 = self.parse_memory_operand(parts[2])
                self.procesador.loadInstr(LW(rd, rs1, offset, self.procesador))
                self.procesador2.loadInstr(LW(rd, rs1, offset, self.procesador))
                
            elif instr_type == "SW":
                # Formato: SW rs2, offset(rs1)
                rs2 = self.parse_register(parts[1].strip(','))
                offset, rs1 = self.parse_memory_operand(parts[2])
                self.procesador.loadInstr(SW(rs2, rs1, offset, self.procesador))
                self.procesador2.loadInstr(SW(rs2, rs1, offset, self.procesador))
                
            elif instr_type == "ADD":
                # Formato: ADD rd, rs1, rs2
                rd = self.parse_register(parts[1].strip(','))
                rs1 = self.parse_register(parts[2].strip(','))
                rs2 = self.parse_register(parts[3])
                self.procesador.loadInstr(ADD(rd, rs1, rs2, self.procesador))
                self.procesador2.loadInstr(ADD(rd, rs1, rs2, self.procesador))
                
            elif instr_type == "ADDI":
                # Formato: ADDI rd, rs1, imm
                rd = self.parse_register(parts[1].strip(','))
                rs1 = self.parse_register(parts[2].strip(','))
                imm = self.parse_immediate(parts[3])
                self.procesador.loadInstr(ADDI(rd, rs1, imm, self.procesador))
                self.procesador2.loadInstr(ADDI(rd, rs1, imm, self.procesador))
                
            elif instr_type == "SUB":
                # Formato: SUB rd, rs1, rs2
                rd = self.parse_register(parts[1].strip(','))
                rs1 = self.parse_register(parts[2].strip(','))
                rs2 = self.parse_register(parts[3])
                self.procesador.loadInstr(SUB(rd, rs1, rs2, self.procesador))
                self.procesador2.loadInstr(SUB(rd, rs1, rs2, self.procesador))
                
            elif instr_type == "AND":
                # Formato: AND rd, rs1, rs2
                rd = self.parse_register(parts[1].strip(','))
                rs1 = self.parse_register(parts[2].strip(','))
                rs2 = self.parse_register(parts[3])
                self.procesador.loadInstr(AND(rd, rs1, rs2, self.procesador))
                self.procesador2.loadInstr(AND(rd, rs1, rs2, self.procesador))
                
            elif instr_type == "ANDI":
                # Formato: ANDI rd, rs1, imm
                rd = self.parse_register(parts[1].strip(','))
                rs1 = self.parse_register(parts[2].strip(','))
                imm = self.parse_immediate(parts[3])
                self.procesador.loadInstr(ANDI(rd, rs1, imm, self.procesador))
                self.procesador2.loadInstr(ANDI(rd, rs1, imm, self.procesador))
                
            elif instr_type == "OR":
                # Formato: OR rd, rs1, rs2
                rd = self.parse_register(parts[1].strip(','))
                rs1 = self.parse_register(parts[2].strip(','))
                rs2 = self.parse_register(parts[3])
                self.procesador.loadInstr(OR(rd, rs1, rs2, self.procesador))
                self.procesador2.loadInstr(OR(rd, rs1, rs2, self.procesador))
                
            elif instr_type == "XOR":
                # Formato: XOR rd, rs1, rs2
                rd = self.parse_register(parts[1].strip(','))
                rs1 = self.parse_register(parts[2].strip(','))
                rs2 = self.parse_register(parts[3])
                self.procesador.loadInstr(XOR(rd, rs1, rs2, self.procesador))
                self.procesador2.loadInstr(XOR(rd, rs1, rs2, self.procesador))
                
            elif instr_type == "BEQ":
                # Formato: BEQ rs1, rs2, offset
                rs1 = self.parse_register(parts[1].strip(','))
                rs2 = self.parse_register(parts[2].strip(','))
                offset = self.parse_immediate(parts[3])
                self.procesador.loadInstr(BEQ(rs1, rs2, offset, self.procesador))
                self.procesador2.loadInstr(BEQ(rs1, rs2, offset, self.procesador))
                
            else:
                raise ValueError(f"Tipo de instrucción no reconocido: {instr_type}")
                
        except Exception as e:
            raise ValueError(f"Error al analizar línea '{line}': {str(e)}")

    def parse_register(self, reg_str):
        """Extrae el número de registro de una cadena como 'x1' o '1'"""
        if reg_str.startswith('x'):
            return int(reg_str[1:])
        return int(reg_str)

    def parse_immediate(self, imm_str):
        """Analiza valores inmediatos en decimal, hex (0x) o binario (0b)"""
        if imm_str.startswith('0x'):
            return int(imm_str[2:], 16)
        elif imm_str.startswith('0b'):
            return int(imm_str[2:], 2)
        return int(imm_str)

    def parse_memory_operand(self, mem_str):
        """Analiza operandos de memoria como 'offset(rs1)'"""
        if '(' in mem_str:
            offset_part, reg_part = mem_str.split('(')
            offset = self.parse_immediate(offset_part)
            rs1 = self.parse_register(reg_part.strip(')'))
            return offset, rs1
        else:
            # Asume offset 0 si no se especifica
            return 0, self.parse_register(mem_str)
        
    def update_cycle_time(self, value):
        """Actualiza el tiempo por ciclo en modo temporizado"""
        self.interval = value
        self.procesador.cycle_time = value
        self.procesador2.cycle_time = value

    def execute_complete(self):
        """Ejecuta todas las instrucciones de una vez"""
        self.execution_started = True
        self.procesador.set_execution_mode("complete")
        self.procesador2.set_execution_mode("complete")
        self.procesador.start_execution()
        self.procesador2.start_execution()
        self.update_ui()

    def execute_timed(self):
        """Ejecuta las instrucciones con temporización"""
        self.execution_started = True
        self.procesador.set_execution_mode("timed", self.interval)
        self.procesador2.set_execution_mode("timed", self.interval)
        self.procesador.start_execution()
        self.procesador2.start_execution()
        self.update_ui()

    def start_step_mode(self):
        """Inicia el modo paso a paso"""
        self.step_mode = True
        self.execution_started = True
        self.procesador.set_execution_mode("step")
        self.procesador2.set_execution_mode("step")
        self.procesador.start_execution()
        self.procesador2.start_execution()
        self.update_ui()

    def execute_step(self):
        """Ejecuta un paso en el modo paso a paso"""
        if self.step_mode:
            self.procesador.step()
            self.procesador2.step()
        self.update_ui()

    def show_memory(self):
        """Muestra el contenido de la memoria con texto oscuro para mejor legibilidad"""
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Memoria de Datos")
        dialog.resize(600, 700)
        
        # Configuración de colores
        text_color = "rgb(30, 30, 30)"  # Color de texto oscuro
        header_color = "rgb(47, 47, 47)" # Color del encabezado
        header_text_color = "rgb(255, 255, 255)" # Texto blanco para encabezados
        cell_color = "rgb(240, 240, 240)" # Fondo de celdas
        read_color = "rgb(200, 230, 255)" # Azul claro para lectura
        write_color = "rgb(200, 255, 200)" # Verde claro para escritura
        
        # Crear tabla
        table = QtWidgets.QTableWidget(32, 3)
        table.setHorizontalHeaderLabels(["Índice", "Dirección", "Valor (hex/dec)"])
        table.verticalHeader().setVisible(False)
        
        # Estilo de la tabla
        table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {cell_color};
                gridline-color: rgb(180, 180, 180);
            }}
            QTableWidget QTableCornerButton::section {{
                background-color: {header_color};
            }}
            QHeaderView::section {{
                background-color: {header_color};
                color: {header_text_color};
                padding: 5px;
                font: bold 10pt 'Kristen ITC';
                border: none;
            }}
            QTableWidget::item {{
                color: {text_color};
                font: 10pt 'Consolas';
            }}
        """)
        
        # Llenar tabla con datos
        for i in range(32):
            address = i * 4  # Asumiendo direccionamiento por palabra de 4 bytes
            value = self.procesador.dataMem.memory[i]
            
            # Índice
            idx_item = QtWidgets.QTableWidgetItem(str(i))
            idx_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            
            # Dirección
            addr_item = QtWidgets.QTableWidgetItem(f"0x{address:08X}")
            addr_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            
            # Valor
            if value is not None:
                val_text = f"0x{value:08X}\n({value})"
                val_item = QtWidgets.QTableWidgetItem(val_text)
                
                # Resaltar accesos recientes
                if hasattr(self.procesador.dataMem, 'last_accessed'):
                    if i == self.procesador.dataMem.last_accessed:
                        bg_color = write_color if getattr(self.procesador.dataMem, 'was_write', False) else read_color
                        val_item.setBackground(QtGui.QColor(bg_color))
            else:
                val_item = QtWidgets.QTableWidgetItem("None")
                val_item.setForeground(QtGui.QColor("rgb(150, 150, 150)"))  # Gris para valores None
            
            val_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            
            # Asegurar color de texto oscuro
            for item in [idx_item, addr_item, val_item]:
                item.setForeground(QtGui.QColor(text_color))
            
            table.setItem(i, 0, idx_item)
            table.setItem(i, 1, addr_item)
            table.setItem(i, 2, val_item)
        
        # Ajustar columnas
        table.resizeColumnsToContents()
        
        # Configurar selección de filas completas
        table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        
        # Botón de cierre
        close_btn = QtWidgets.QPushButton("Cerrar")
        close_btn.setStyleSheet(f"""
            QPushButton {{
                font: 12pt 'Kristen ITC';
                padding: 8px;
                background-color: {header_color};
                color: {header_text_color};
                min-width: 100px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: rgb(70, 70, 70);
            }}
        """)
        close_btn.clicked.connect(dialog.close)
        
        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(table)
        layout.addWidget(close_btn, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        
        dialog.setLayout(layout)
        dialog.exec()

    def show_statistics(self):
        """Muestra una ventana con las estadísticas de ambos procesadores"""
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Estadísticas de Ejecución")
        dialog.resize(800, 600)

        # Configurar colores
        text_color = "rgb(30, 30, 30)"
        header_color = "rgb(47, 47, 47)"
        header_text_color = "rgb(255, 255, 255)"
        cell_color = "rgb(240, 240, 240)"

        # Crear tabla de estadísticas
        table = QtWidgets.QTableWidget(10, 3)
        table.setHorizontalHeaderLabels(["Métrica", "Procesador 1", "Procesador 2"])
        table.verticalHeader().setVisible(False)

        # Estilo de la tabla
        table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {cell_color};
                gridline-color: rgb(180, 180, 180);
            }}
            QTableWidget QTableCornerButton::section {{
                background-color: {header_color};
            }}
            QHeaderView::section {{
                background-color: {header_color};
                color: {header_text_color};
                padding: 5px;
                font: bold 10pt 'Kristen ITC';
                border: none;
            }}
            QTableWidget::item {{
                color: {text_color};
                font: 10pt 'Consolas';
            }}
        """)

        # Datos de las métricas
        metrics = [
            ("Ciclos totales", self.procesador.cycles, self.procesador2.cycles),
            ("Instrucciones retiradas", self.procesador.instrRetired, self.procesador2.instrRetired),
            ("Tiempo de ejecución (s)", f"{self.procesador.time:.2f}", f"{self.procesador2.time:.2f}"),
            ("CPI (Ciclos por instrucción)",
             f"{self.procesador.cycles / max(1, self.procesador.instrRetired):.2f}",
             f"{self.procesador2.cycles / max(1, self.procesador2.instrRetired):.2f}"),
            ("IPC (Instrucciones por ciclo)",
             f"{self.procesador.instrRetired / max(1, self.procesador.cycles):.2f}",
             f"{self.procesador2.instrRetired / max(1, self.procesador2.cycles):.2f}"),
            ("Stalls",
             getattr(self.procesador.hazard_unit, 'stall_count', 0) if self.procesador.hazard_unit else 0,
             getattr(self.procesador2.hazard_unit, 'stall_count', 0) if self.procesador2.hazard_unit else 0),
            ("Flushes",
             getattr(self.procesador.hazard_unit, 'flush_count', 0) if self.procesador.hazard_unit else 0,
             getattr(self.procesador2.hazard_unit, 'flush_count', 0) if self.procesador2.hazard_unit else 0),
            ("Forwards",
             getattr(self.procesador.hazard_unit, 'forward_count', 0) if self.procesador.hazard_unit else 0,
             getattr(self.procesador2.hazard_unit, 'forward_count', 0) if self.procesador2.hazard_unit else 0),
            ("Mispredicciones de saltos",
             self.procesador.mispredictions if self.procesador.branch_prediction else "N/A",
             self.procesador2.mispredictions if self.procesador2.branch_prediction else "N/A"),
            ("Tasa de error en predicción (%)",
             f"{self.procesador.get_branch_stats():.2f}" if self.procesador.branch_prediction else "N/A",
             f"{self.procesador2.get_branch_stats():.2f}" if self.procesador2.branch_prediction else "N/A")
        ]

        # Llenar la tabla con los datos
        for row, (metric, p1_val, p2_val) in enumerate(metrics):
            metric_item = QtWidgets.QTableWidgetItem(metric)
            p1_item = QtWidgets.QTableWidgetItem(str(p1_val))
            p2_item = QtWidgets.QTableWidgetItem(str(p2_val))

            # Centrar el texto y asegurar color oscuro
            for item in [metric_item, p1_item, p2_item]:
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                item.setForeground(QtGui.QColor(text_color))

            table.setItem(row, 0, metric_item)
            table.setItem(row, 1, p1_item)
            table.setItem(row, 2, p2_item)

        # Ajustar columnas
        table.resizeColumnsToContents()

        # Botón de cierre
        close_btn = QtWidgets.QPushButton("Cerrar")
        close_btn.setStyleSheet(f"""
            QPushButton {{
                font: 12pt 'Kristen ITC';
                padding: 8px;
                background-color: {header_color};
                color: {header_text_color};
                min-width: 100px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: rgb(70, 70, 70);
            }}
        """)
        close_btn.clicked.connect(dialog.close)

        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(table)
        layout.addWidget(close_btn, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        dialog.setLayout(layout)
        dialog.exec()

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

        # Verificar si ambos procesadores han terminado
        if (not self.procesador.running and not self.procesador2.running and
                hasattr(self, 'execution_started') and self.execution_started):
            self.execution_started = False
            self.show_statistics()

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
            try:
                item_text = str(instr)
            except:
                item_text = f"Instruccion: {i}"
            model.setItem(i, 0, QtGui.QStandardItem(item_text))
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