class ADDI:
    def __init__(self, rd, rs1, imm, proce):
        self.rd = rd
        self.rs1 = rs1
        self.imm = imm
        self.proce = proce

        self.steps = [self.step1, self.step2, self.step3]

        self.result = None  # Para forwarding

    def __str__(self):
        return f"ADDI x{self.rd}, x{self.rs1}, {self.imm}"

    def __repr__(self):
        return str(self)

    def step1(self):
        print("empezando addi")
        self.proce.regRegFile.data = self.proce.regFile.read(self.rs1)
        print("ADDI: ", self.proce.regRegFile.data)

    def step2(self):
        self.result = self.proce.alu.OP(self.proce.regRegFile.data, self.imm, 0)
        print(f"ADDI:[EX] res={self.result}")

    def step3(self):
        self.proce.regFile.write(self.rd, self.result)
        print(f"ADDI:[WB] x{self.rd} <- {self.result}")

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