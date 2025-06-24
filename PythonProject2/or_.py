class OR:
    def __init__(self, rd, rs1, rs2, proce):
        self.rd = rd
        self.rs1 = rs1
        self.rs2 = rs2
        self.proce = proce
        self.steps = [self.step1, self.step2, self.step3]

    def step1(self):
        print("empezando or")
        self.op1 = self.proce.regFile.read(self.rs1)
        self.op2 = self.proce.regFile.read(self.rs2)
        print(f"OR: [ID] op1 = {self.op1}, op2 = {self.op2}")

    def step2(self):
        self.res = self.proce.alu.OP(self.op1, self.op2, 3)
        print(f"OR: [EX] res = {self.res}")

    def step3(self):
        self.proce.regFile.write(self.rd, self.res)
        print(f"OR: [WB] x{self.rd} <- {self.res}\nOR terminada")

    def execute(self):
        if self.steps:
            fase = self.steps.pop(0)
            fase()
