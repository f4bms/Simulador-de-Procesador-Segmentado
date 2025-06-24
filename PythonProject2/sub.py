class SUB:
    def __init__(self, rd, rs1, rs2, proce):
        self.rd, self.rs1, self.rs2 = rd, rs1, rs2
        self.proce = proce
        self.steps = [self.id, self.ex, self.wb]
        self.result = None  # Para forwarding
        self.op1 = None
        self.op2 = None

    def id(self):
        print("empezando sub")
        self.op1 = self.proce.regFile.reg[self.rs1]
        self.op2 = self.proce.regFile.reg[self.rs2]
        print(f"[ID] op1={self.op1} op2={self.op2}")

    def ex(self):
        self.result = self.proce.alu.OP(self.op1, self.op2, 1)  # 1 = resta
        print(f"[EX] result={self.result}")

    def wb(self):
        self.proce.regFile.reg[self.rd] = self.result
        print(f"[WB] x{self.rd} <- {self.result}\nSUB terminada")

    def execute(self):
        if self.steps:
            self.steps.pop(0)()
            if not self.steps:
                print("SUB terminada")

    # Métodos para hazard unit
    def uses_rs(self):
        return True

    def uses_rt(self):
        return True

    def modifies_rd(self):
        return True