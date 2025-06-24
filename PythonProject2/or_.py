class OR:
    def __init__(self, rd, rs1, rs2, proce):
        self.rd = rd
        self.rs1 = rs1
        self.rs2 = rs2
        self.proce = proce
        self.steps = [self.step1, self.step2, self.step3]
        self.result = None  # Para forwarding
        self.op1 = None
        self.op2 = None

    def step1(self):
        print("empezando or")
        self.op1 = self.proce.regFile.reg[self.rs1]
        self.op2 = self.proce.regFile.reg[self.rs2]
        print(f"OR: [ID] op1 = {self.op1}, op2 = {self.op2}")

    def step2(self):
        self.result = self.proce.alu.OP(self.op1, self.op2, 3)
        print(f"OR: [EX] res = {self.result}")

    def step3(self):
        self.proce.regFile.reg[self.rd] = self.result
        print(f"OR: [WB] x{self.rd} <- {self.result}\nOR terminada")

    def execute(self):
        if self.steps:
            fase = self.steps.pop(0)
            fase()

    # Métodos para hazard unit
    def uses_rs(self):
        return True

    def uses_rt(self):
        return True

    def modifies_rd(self):
        return True
