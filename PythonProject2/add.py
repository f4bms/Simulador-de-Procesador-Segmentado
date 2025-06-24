class ADD:
    def __init__(self, rd, rs1, rs2, proce):
        self.op2 = None
        self.op1 = None
        self.rd, self.rs1, self.rs2 = rd, rs1, rs2
        self.proce = proce
        self.steps = [self.id, self.ex, self.wb]
        self.result = None  # Para forwarding

    def __str__(self):
        return f"ADD x{self.rd}, x{self.rs1}, x{self.rs2}"

    def __repr__(self):
        return str(self)

    def id(self):
        print("empezando add")
        self.op1 = self.proce.regFile.read(self.rs1)
        self.op2 = self.proce.regFile.read(self.rs2)
        print(f"ADD:[ID] op1={self.op1} op2={self.op2}")

    def ex(self):
        self.result = self.proce.alu.OP(self.op1, self.op2, 0)
        print(f"ADD:[EX] res={self.result}")

    def wb(self):
        self.proce.regFile.write(self.rd, self.result)
        print(f"ADD:[WB] x{self.rd} <- {self.result}\nADD terminada")

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
