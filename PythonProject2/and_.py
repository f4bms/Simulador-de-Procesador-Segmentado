class AND:
    def __init__(self, rd, rs1, rs2, proce):
        self.rd = rd
        self.rs1 = rs1
        self.rs2 = rs2
        self.proce = proce
        self.steps = [self.step1, self.step2, self.step3]
        self.result = None  # Para forwarding
        self.op1 = None
        self.op2 = None

    def __str__(self):
        return f"AND x{self.rd}, x{self.rs1}, x{self.rs2}"

    def __repr__(self):
        return str(self)

    def step1(self):
        print("empezando and")
        self.op1 = self.proce.regFile.read(self.rs1)
        self.op2 = self.proce.regFile.read(self.rs2)
        print(f"AND: [ID] op1 = {self.op1}, op2 = {self.op2}")

    def step2(self):
        self.result = self.proce.alu.OP(self.op1, self.op2, 2)
        print(f"AND: [EX] res = {self.result}")

    def step3(self):
        self.proce.regFile.write(self.rd, self.result)
        print(f"AND: [WB] x{self.rd} <- {self.result}\nAND terminada")

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
