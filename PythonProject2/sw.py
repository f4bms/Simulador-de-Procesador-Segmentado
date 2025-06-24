class SW:
    def __init__(self, rd, imm, rs1, proce):
        self.rd   = rd
        self.imm  = imm
        self.rs1  = rs1
        self.proce = proce
        self.steps = [self.step1, self.step2, self.step3]
        self.addr = None
        self.data = None

    def step1(self):
        print("empezando sw")
        self.base = self.proce.regFile.reg[self.rs1]
        self.data = self.proce.regFile.reg[self.rd]
        print(f"SW:[ID] base={self.base}, data={self.data}")

    def step2(self):
        self.addr = self.proce.alu.OP(self.base, self.imm, 0)
        print(f"SW:[EX] dirección={self.addr}")

    def step3(self):
        self.proce.dataMem.memory[self.addr] = self.data
        print(f"SW:[MEM] Mem[{self.addr}] <- {self.data}\nSW terminada")

    def execute(self):
        if self.steps:
            fase = self.steps.pop(0)
            fase()

    # Métodos para hazard unit
    def uses_rs(self):
        return True

    def uses_rt(self):
        return True  # rd es el registro fuente en SW

    def modifies_rd(self):
        return False

    def is_store(self):
        return True