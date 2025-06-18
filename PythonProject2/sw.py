class SW:
    def __init__(self, rd, imm, rs1, proce):
        self.rd   = rd
        self.imm  = imm
        self.rs1  = rs1
        self.proce = proce
        self.steps = [self.step1, self.step2, self.step3]

    def step1(self):
        print("empezando sw")
        self.base = self.proce.regFile.reg[self.rs1]
        self.data = self.proce.regFile.reg[self.rd]
        print("valor base =", self.base, "dato =", self.data)

    def step2(self):
        self.addr = self.proce.alu.OP(self.base, self.imm, 0)
        print("dirección =", self.addr)

    def step3(self):
        self.proce.dataMem.memory[self.addr] = self.data
        print(f"dato escrito: Mem[{self.addr}] <- {self.data}\nSW terminada")

    def execute(self):
        if self.steps:
            fase = self.steps.pop(0)
            fase()
