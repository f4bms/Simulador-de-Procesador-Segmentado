class LW:
        def __init__(self, rd, imm, rs1, proce):

            self.rd = rd
            self.imm = imm
            self.rs1 = rs1
            self.proce = proce

            self.steps = [self.step1, self.step2, self.step3, self.step4]

            self.result = None  # Para forwarding
            self.addr = None
            self.op1 = None

        def step1(self):
            print("empezando lw")
            if self.rs1 >= len(self.proce.regFile.reg):
                print(f"el rs1 fuera de rango: rs1={self.rs1}")
                raise ValueError("Registro fuente fuera de rango")
            self.op1 = self.proce.regFile.reg[self.rs1]
            print(f"LW:[ID] base={self.op1}, imm={self.imm}")

        def step2(self):
            if self.op1 is None:
                print("[ERROR] op1 no definido en LW. ¿step1 falló?")
                raise ValueError("op1 no definido")
            self.addr = self.proce.alu.OP(self.op1, self.imm, 0)
            print(f"LW:[EX] dirección={self.addr}")

        def step3(self):
            if self.addr is None or self.addr >= len(self.proce.dataMem.memory):
                print(f"[ERROR] Dirección fuera de rango o indefinida: addr={self.addr}")
                raise ValueError("Dirección de memoria inválida")
            self.result = self.proce.dataMem.memory[self.addr]
            print(f"LW:[MEM] dato={self.result}")

        def step4(self):
            self.proce.regFile.reg[self.rd] = self.result
            print(f"LW:[WB] x{self.rd} <- {self.result}\nLW terminada")

        def execute(self):
            if self.steps:
                fase = self.steps.pop(0)
                try:
                    fase()
                except Exception as e:
                    print(f"[ERROR] durante {fase.__name__}: {e}")
                    self.steps.clear()
                if not self.steps:
                    print("LW terminó")

        # Métodos para hazard unit
        def uses_rs(self):
            return True

        def uses_rt(self):
            return False

        def modifies_rd(self):
            return True

        def is_load(self):
            return True