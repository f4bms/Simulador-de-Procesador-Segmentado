class ADDI:
    def __init__(self, rd, rs1, imm, proce):
        self.rd = rd
        self.rs1 = rs1
        self.imm = imm
        self.proce = proce

        self.steps = [self.step1, self.step2, self.step3]

    def __str__(self):
        return f"ADDI x{self.rd}, x{self.rs1}, {self.imm}"

    def __repr__(self):
        return str(self)

    def step1(self):
        print("empezando addi")
        self.proce.regRegFile.data = self.proce.regFile.read(self.rs1)
        print("ADDI: ", self.proce.regRegFile.data)

    def step2(self):
        if self.proce.regRegFile.data is None:
            raise ValueError(f"El registro {self.rs1} tiene un valor None y no puede sumarse.")
        self.proce.alu_reg.data = self.proce.alu.OP(self.proce.regRegFile.data, self.imm, 0)
        print("ADDI:[EX]: ", self.proce.alu_reg.data)

    def step3(self):
        self.proce.regFile.write(self.rd, self.proce.alu_reg.data)
        print(f"ADDI:[WB] x{self.rd} <- {self.proce.alu_reg.data}")

    def execute(self):
        if self.steps:
            fase =self.steps.pop(0)
            fase()
            if not self.steps:
                print("ADDI terminada")