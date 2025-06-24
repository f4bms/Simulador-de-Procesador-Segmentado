class ADD:
    def __init__(self, rd, rs1, rs2, proce):
        self.rd, self.rs1, self.rs2 = rd, rs1, rs2
        self.proce = proce
        self.steps = [self.id, self.ex, self.wb]
        self.result = None  # Para forwarding
        self.op1 = None
        self.op2 = None

    def id(self):
        print("empezando add")

        self.op1 = self.proce.regFile.reg[self.rs1]
        self.op2 = self.proce.regFile.reg[self.rs2]
        print(f"ADD:[ID] op1={self.op1} op2={self.op2}")

    def ex(self):
        self.res = self.proce.alu.OP(self.op1, self.op2, 0)
        print(f"ADD:[EX] res={self.res}")

    def wb(self):
        self.proce.regFile.reg[self.rd] = self.res
        print(f"ADD:[WB] x{self.rd} <- {self.res}\nADD terminada")

    def execute(self):
        if self.steps:
            self.steps.pop(0)()

    # Métodos para hazard unit
    def uses_rs(self):
        return True

    def uses_rt(self):
        return True

    def modifies_rd(self):
        return True
