import threading
import time

from intsrMem import *
from reg import *
from regFile import *
from alu import *
from dataMem import *
from HazardUnit import *

class Procesador:
    def __init__(self, intv = 1, enable_hazards = False):
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
        self.hazard_unit = HazardUnit(self) if True else None

        #para lo de los cuadritos de abajo:
        self.cycles = 0
        self.pc = 0
        self. instrRetired = 0
        self.pipel_stage = ["", "", "", "", ""]
        self.time = 0
        self.metrics = {
            'stalls': 0,
            'flushes': 0,
            'forwards': 0,
            'cpi': 0.0,
            'ipc': 0.0
        }

        #Modos de ejecución
        self.running = False
        self.execution_mode = "complete"
        self.cycle_time = 1.0
        self.step_event = threading.Event()
        self.stop_event = threading.Event()

        #Predicción de saltos
        self.branch_prediction = False
        self.branch_prediction_mode = "always_not_taken"
        self.branch_history = {} #Para prediccion dinamica
        self.mispredictions = 0
        self.branch_total = 0

    def enable_hazard_unit(self, enabled = True):
        self.hazard_unit = HazardUnit(self) if enabled else None

    def enable_branch_prediction(self, enabled = True, prediction_mode = "always_taken"):
        self.branch_prediction = enabled
        self.branch_prediction_mode = prediction_mode
    
    def get_branch_stats(self):
        if self.branch_total == 0:
            return 0.0
        return (self.mispredictions / self.branch_total) * 100

    def loadInstr(self, instr):
        self.intrMem.memory.append(instr)
    
    def set_execution_mode(self, mode, cycle_time=1.0):
        valid_modes = ["complete", "step", "timed"]
        if mode not in valid_modes:
            raise ValueError(f"Modo inválido. Debe ser uno de {valid_modes}")
        self.execution_mode = mode
        self.cycle_time = cycle_time

    def start_execution(self):
        self.running = True
        self.start_exe_time = time.time()
        self.stop_event.clear()

        if self.execution_mode == "complete":
            self.execute_complete()
        elif self.execution_mode == "step":
            self.step_event.clear()
        elif self.execution_mode == "timed":
            threading.Thread(target=self.execute_timed, daemon=True).start()
    
    def stop_execution(self):
        self.running = False
        self.stop_event.set()
    
    def step(self):
        if self.execution_mode == "step" and self.running:
            self.step_event.set()
    
    def execute_complete(self):
        while self.running and not self.stop_event.is_set():
            start_time = time.time()
            self.execute()
            elapsed = time.time() - start_time
            latency = max(0, 0.02 - elapsed)
            time.sleep(latency)
    
    def execute_timed(self):
        while self.running and not self.stop_event.is_set():
            start_time = time.time()
            self.execute()

            elapsed = time.time() - start_time
            sleep_time = max(0, self.cycle_time - elapsed)
            time.sleep(sleep_time)

    def execute(self, complete=False):
        while True:
            if not complete and self.execution_mode == "step":
                self.step_event.wait()
                self.step_event.clear()
            
            self.cycles += 1
            start = False

            self.time = time.time() - self.start_exe_time

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
            if self.enable_hazards and self.hazard_unit and self.hazard_unit.stall:
                print("[STALL] Congelando IF y PC")
                # No avanzar PC ni actualizar instr_reg
            if self.pc < len(self.intrMem.memory):
                start = True
                self.pipel_stage[0] = f"Instr {self.pc}"
                self.instr_reg.instr = self.intrMem.read(self.pc)
                self.pc +=1

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
                cpi = self.cycles / max(1, self.instrRetired)
                ipc = self.instrRetired / max(1, self.cycles)
                clock_rate = self.cycles / (completedTime * 1e9)
            else:
                cpi = ipc = clock_rate = 0

            if (self.pc >= len(self.intrMem.memory) and
                    self.instr_reg.instr is None and
                    self.regRegFile.instr is None and
                    self.alu_reg.instr is None and
                    self.reg_data.instr is None):
                self.stop_execution()
                break

            self.intrMem.clear_active()
            self.regFile.clear_active()
            self.alu.clear_active()
            self.dataMem.clear_active()

            if not complete or not start or self.stop_event.is_set():
                break