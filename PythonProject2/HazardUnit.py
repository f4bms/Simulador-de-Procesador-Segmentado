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

class HazardUnit:
    def __init__(self, processor):
        self.processor = processor
        self.stall = False
        self.flush = False
        self.forward_EX = False
        self.forward_MEM = False
        self.stall_count = 0
        self.flush_count = 0
        self.forward_count = 0

    def check_hazards(self):
        """Verifica todos los tipos de hazards en el pipeline"""
        self.check_data_hazards()
        self.check_control_hazards()

    def check_data_hazards(self):
        """Detecta y maneja riesgos de datos (RAW)"""
        # Obtener las instrucciones en cada etapa del pipeline
        if_stage = self.processor.instr_reg.instr if self.processor.instr_reg.instr else None
        id_stage = self.processor.regRegFile.instr if self.processor.regRegFile.instr else None
        ex_stage = self.processor.alu_reg.instr if self.processor.alu_reg.instr else None
        mem_stage = self.processor.reg_data.instr if self.processor.reg_data.instr else None

        # Riesgo RAW entre ID y EX
        if id_stage and ex_stage and hasattr(id_stage, 'rs1') and hasattr(ex_stage, 'rd'):
            if id_stage.rs1 == ex_stage.rd:
                if isinstance(ex_stage, LW):  # Load hazard necesita stall
                    self.stall = True
                    self.stall_count += 1
                else:  # Otras instrucciones pueden usar forwarding
                    self.forward_EX = True
                    self.forward_count += 1

            if hasattr(id_stage, 'rs2') and id_stage.rs2 == ex_stage.rd:
                if isinstance(ex_stage, LW):  # Load hazard necesita stall
                    self.stall = True
                    self.stall_count += 1
                else:  # Otras instrucciones pueden usar forwarding
                    self.forward_EX = True
                    self.forward_count += 1

        # Riesgo RAW entre ID y MEM
        if id_stage and mem_stage and hasattr(id_stage, 'rs1') and hasattr(mem_stage, 'rd'):
            if id_stage.rs1 == mem_stage.rd:
                self.forward_MEM = True
                self.forward_count += 1

            if hasattr(id_stage, 'rs2') and id_stage.rs2 == mem_stage.rd:
                self.forward_MEM = True
                self.forward_count += 1

    def check_control_hazards(self):
        """Detecta y maneja riesgos de control (branch)"""
        # Obtener la instrucción en etapa EX (branch)
        ex_stage = self.processor.alu_reg.instr if self.processor.alu_reg.instr else None
        
        # Si es una instrucción de salto (BEQ)
        if ex_stage and isinstance(ex_stage, BEQ):
            self.flush = True
            self.flush_count += 1

    def resolve_hazards(self):
        """Aplica las soluciones a los hazards detectados"""
        if self.stall:
            # Insertar burbuja en el pipeline
            self.processor.instr_reg.clear()
            self.processor.regRegFile.clear()
        
        if self.flush:
            # Flush de instrucciones después del branch
            self.processor.instr_reg.clear()
        
        # Resetear flags para el próximo ciclo
        self.stall = False
        self.flush = False
        self.forward_EX = False
        self.forward_MEM = False