class LW:
    def __init__(self, rd, imm, rs1, proce):
        self.rd = rd
        self.imm = imm
        self.rs1 = rs1
        self.proce = proce
        self.steps = [self.step1, self.step2, self.step3, self.step4]
        self.result = None  # Para forwarding
        self.addr = None

    def step1(self):
        print("empezando lw")
        self.op1 = self.proce.regFile.reg[self.rs1]
        print(f"LW:[ID] base={self.op1}, imm={self.imm}")

    def step2(self):
        self.addr = self.proce.alu.OP(self.op1, self.imm, 0)
        print(f"LW:[EX] dirección={self.addr}")

    def step3(self):
        self.result = self.proce.dataMem.memory[self.addr]
        print(f"LW:[MEM] dato={self.result}")

    def step4(self):
        self.proce.regFile.reg[self.rd] = self.result
        print(f"LW:[WB] x{self.rd} <- {self.result}\nLW terminada")

    def execute(self):
        if self.steps:
            fase = self.steps.pop(0)
            fase()
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