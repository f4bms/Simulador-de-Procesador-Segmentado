import threading
import time
from intsrMem import *
from reg import *
from regFile import *
from alu import *
from dataMem import *
from HazardUnit import *

class Procesador:
    def __init__(self, intv=1, enable_hazards=True):
        self.intv = intv
        self.intrMem = instrMemory()
        self.regFile = regFile()
        self.alu = ALU()
        self.dataMem = dataMemory()
        self.instr_reg = Registr()
        self.regRegFile = Registr()
        self.alu_reg = Registr()
        self.reg_data = Registr()
        self.enable_hazards = enable_hazards
        self.hazard_unit = HazardUnit(self) if enable_hazards else None

        # Para lo de los cuadritos de abajo:
        self.cycles = 0
        self.pc = 0
        self.instrRetired = 0
        self.pipel_stage = ["", "", "", "", ""]
        self.time = 1
        self.metrics = {
            'stalls': 0,
            'flushes': 0,
            'forwards': 0,
            'cpi': 0.0,
            'ipc': 0.0
        }

    def loadInstr(self, instr):
        self.intrMem.memory.append(instr)

    def apply_forwarding(self):
        """Aplica forwarding de datos cuando es necesario"""
        if not self.enable_hazards or not self.hazard_unit:
            return
            
        id_stage = self.regRegFile.instr if self.regRegFile.instr else None
        ex_stage = self.alu_reg.instr if self.alu_reg.instr else None
        mem_stage = self.reg_data.instr if self.reg_data.instr else None

        if self.hazard_unit.forward_EX and ex_stage and id_stage:
            if hasattr(id_stage, 'rs1') and hasattr(ex_stage, 'rd') and id_stage.rs1 == ex_stage.rd:
                id_stage.op1 = ex_stage.result if hasattr(ex_stage, 'result') else ex_stage.proce.alu_reg.data
            
            if hasattr(id_stage, 'rs2') and hasattr(ex_stage, 'rd') and id_stage.rs2 == ex_stage.rd:
                id_stage.op2 = ex_stage.result if hasattr(ex_stage, 'result') else ex_stage.proce.alu_reg.data

        if self.hazard_unit.forward_MEM and mem_stage and id_stage:
            if hasattr(id_stage, 'rs1') and hasattr(mem_stage, 'rd') and id_stage.rs1 == mem_stage.rd:
                id_stage.op1 = mem_stage.result if hasattr(mem_stage, 'result') else mem_stage.proce.reg_data.data
            
            if hasattr(id_stage, 'rs2') and hasattr(mem_stage, 'rd') and id_stage.rs2 == mem_stage.rd:
                id_stage.op2 = mem_stage.result if hasattr(mem_stage, 'result') else mem_stage.proce.reg_data.data

    def execute(self):
        start = True
        timer = time.time()
        while start:
            self.cycles += 1
            start = False

            # WB
            if self.reg_data.instr is not None:
                start = True
                self.reg_data.instr.execute()
                self.pipel_stage[4] = "WB"
                self.reg_data.clear()
                self.instrRetired += 1
            else:
                self.pipel_stage[4] = ""

            # MEM
            if self.alu_reg.instr is not None:
                start = True
                self.alu_reg.instr.execute()
                self.pipel_stage[3] = "MEM"
                self.reg_data.instr = self.alu_reg.instr
                self.alu_reg.clear()
            else:
                self.pipel_stage[3] = ""

            # EX
            if self.regRegFile.instr is not None:
                start = True
                # Aplicar forwarding antes de ejecutar
                if self.enable_hazards and self.hazard_unit:
                    self.apply_forwarding()
                
                self.regRegFile.instr.execute()
                self.pipel_stage[2] = "EX"
                self.alu_reg.instr = self.regRegFile.instr
                self.regRegFile.clear()
            else:
                self.pipel_stage[2] = ""

            # ID
            if self.instr_reg.instr is not None:
                start = True
                self.instr_reg.instr.execute()
                self.pipel_stage[1] = f"Instr {self.pc-1}"
                self.regRegFile.instr = self.instr_reg.instr
                self.instr_reg.clear()
            else:
                self.pipel_stage[1] = ""

            # IF
            if self.pc < len(self.intrMem.memory):
                start = True
                self.pipel_stage[0] = f"Instr {self.pc}"
                self.instr_reg.instr = self.intrMem.memory[self.pc]
                self.pc += 1
            else:
                self.pipel_stage[0] = ""

            # Verificar y manejar hazards
            if self.enable_hazards and self.hazard_unit:
                self.hazard_unit.check_hazards()
                self.hazard_unit.resolve_hazards()
                
                # Actualizar métricas
                self.metrics['stalls'] = self.hazard_unit.stall_count
                self.metrics['flushes'] = self.hazard_unit.flush_count
                self.metrics['forwards'] = self.hazard_unit.forward_count

            completedTime = self.time
            if completedTime > 0:
                self.metrics['cpi'] = self.cycles / max(1, self.instrRetired)
                self.metrics['ipc'] = self.instrRetired / max(1, self.cycles)
                clock_rate = self.cycles / (completedTime * 1e9)
            else:
                self.metrics['cpi'] = self.metrics['ipc'] = 0.0

            # Actualizar GUI
            self.update_gui()

    def update_gui(self):
        """Actualiza la interfaz gráfica con la información del pipeline"""
        # Esta función debería ser implementada para actualizar la UI
        pass


    








