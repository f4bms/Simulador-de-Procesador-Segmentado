class XOR:
    def __init__(self, rd, rs1, rs2, proce):
        self.rd = rd
        self.rs1 = rs1
        self.rs2 = rs2
        self.proce = proce
        self.steps = [self.step1, self.step2, self.step3]

    def step1(self):
        print("empezando xor")
        self.op1 = self.proce.regFile.reg[self.rs1]
        self.op2 = self.proce.regFile.reg[self.rs2]
        print(f"XOR: [ID] op1 = {self.op1}, op2 = {self.op2}")

    def step2(self):
        self.res = self.proce.alu.OP(self.op1, self.op2, 4)
        print(f"XOR: [EX] res = {self.res}")

    def step3(self):
        self.proce.regFile.reg[self.rd] = self.res
        print(f"XOR: [WB] x{self.rd} <- {self.res}\nXOR terminada")

    def execute(self):
        if self.steps:
            fase = self.steps.pop(0)
            fase()
