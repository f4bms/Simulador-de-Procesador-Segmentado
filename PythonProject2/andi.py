class ANDI:
    def __init__(self, rd, rs1, imm, proce):
        self.rd = rd
        self.rs1 = rs1
        self.imm = imm
        self.proce = proce
        self.steps = [self.step1, self.step2, self.step3]

    def __str__(self):
        return f"ANDI x{self.rd}, x{self.rs1}, {self.imm}"

    def __repr__(self):
        return str(self)

    def step1(self):
        print("empezando andi")
        self.op1 = self.proce.regFile.read(self.rs1)
        print(f"ANDI: [ID] op1 = {self.op1}, imm = {self.imm}")

    def step2(self):
        self.res = self.proce.alu.OP(self.op1, self.imm, 2)  # 2 = AND
        print(f"ANDI: [EX] res = {self.res}")

    def step3(self):
        self.proce.regFile.write(self.rd, self.res)
        print(f"ANDI: [WB] x{self.rd} <- {self.res}\nANDI terminada")

    def execute(self):
        if self.steps:
            fase = self.steps.pop(0)
            fase()
