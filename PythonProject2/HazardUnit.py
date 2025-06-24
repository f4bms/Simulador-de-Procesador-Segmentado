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
from NOP import *

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

        self.stall = False  # resetear cada ciclo

        # Riesgo RAW entre ID y EX
        if id_stage and ex_stage and hasattr(id_stage, 'rs1') and hasattr(ex_stage, 'rd'):
            # Check rs1
            if id_stage.rs1 == ex_stage.rd and ex_stage.modifies_rd():
                if hasattr(ex_stage, 'is_load') and ex_stage.is_load():
                    self.stall = True
                    self.stall_count += 1

            # Check rs2 si existe
            if hasattr(id_stage, 'rs2') and id_stage.rs2 == ex_stage.rd and ex_stage.modifies_rd():
                if hasattr(ex_stage, 'is_load') and ex_stage.is_load():
                    self.stall = True
                    self.stall_count += 1

        # También puedes extender chequeo con MEM stage si quieres

    def check_control_hazards(self):
        """Detecta y maneja riesgos de control (branch)"""
        ex_stage = self.processor.alu_reg.instr if self.processor.alu_reg.instr else None
        if ex_stage and hasattr(ex_stage, 'is_branch') and ex_stage.is_branch():
            self.flush = True
            self.flush_count += 1

    def resolve_hazards(self):
        if self.stall:
            print("[STALL] Insertando burbuja por hazard de carga")

            # Empujar pipeline hacia adelante
            self.processor.reg_data.instr = self.processor.alu_reg.instr
            self.processor.alu_reg.instr = self.processor.regRegFile.instr
            self.processor.regRegFile.instr = NOP(self.processor)  # Inserta burbuja en EX

            # Congelar IF y retroceder PC para no avanzar
            self.processor.pc -= 1

        if self.flush:
            print("[FLUSH] Flush tras branch")
            self.processor.instr_reg.clear()

        # Resetear flags para siguiente ciclo
        self.stall = False
        self.flush = False
        self.forward_EX = False
        self.forward_MEM = False