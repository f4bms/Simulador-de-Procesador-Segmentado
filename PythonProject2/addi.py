class ADDI:
    def __init__(self, rd, rs1, imm, proce):
        self.rd = rd
        self.rs1 = rs1
        self.imm = imm
        self.proce = proce

        self.steps = [self.step1, self.step2, self.step3]

        self.result = None  # Para forwarding

    def step1(self):
        print("empezando addi")
        self.op1 = self.proce.regFile.reg[self.rs1]
        print(f"ADDI: [ID] op1={self.op1}, imm={self.imm}")

    def step2(self):
        self.result = self.proce.alu.OP(self.op1, self.imm, 0)
        print(f"ADDI:[EX] res={self.result}")

    def step3(self):
        self.proce.regFile.reg[self.rd] = self.result
        print(f"ADDI:[WB] x{self.rd} <- {self.result}\nADDI terminada")

    def execute(self):
        if self.steps:
            fase =self.steps.pop(0)
            fase()
            if not self.steps:
                print("ADDI terminada")

    # Métodos para hazard unit
    def uses_rs(self):
        return True

    def uses_rt(self):
        return False

    def modifies_rd(self):
        return True