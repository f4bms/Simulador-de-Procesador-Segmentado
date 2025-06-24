class SW:
    def __init__(self, rd, imm, rs1, proce):
        self.base = None
        self.rd   = rd
        self.imm  = imm
        self.rs1  = rs1
        self.proce = proce
        self.steps = [self.step1, self.step2, self.step3]
        self.addr = None
        self.data = None

    def __str__(self):
        return f"SW x{self.rd}, {self.imm}(x{self.rs1})"

    def __repr__(self):
        return str(self)

    def step1(self):
        print("empezando sw")
        self.base = self.proce.regFile.read(self.rs1)
        self.data = self.proce.regFile.read(self.rd)
        print("valor base =", self.base, "dato =", self.data)

    def step2(self):
        self.addr = self.proce.alu.OP(self.base, self.imm, 0)
        print(f"SW:[EX] dirección={self.addr}")

    def step3(self):
        self.proce.dataMem.write(self.addr, self.data)
        print(f"dato escrito: Mem[{self.addr}] <- {self.data}\nSW terminada")

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