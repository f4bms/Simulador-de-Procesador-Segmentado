class BEQ:
    def __init__(self, rs1, rs2, imm, proce):
        self.rs1, self.rs2, self.imm = rs1, rs2, imm
        self.proce = proce
        self.steps = [self.id, self.ex]

    def id(self):
        print("empezando beq")

        self.op1 = self.proce.regFile.reg[self.rs1]
        self.op2 = self.proce.regFile.reg[self.rs2]
        print(f"[ID] op1={self.op1} op2={self.op2}")

    def ex(self):
        if self.op1 == self.op2:
            # PC ya avanzó en IF; vuelve a ajustar:
            self.proce.pc += (self.imm // 4) - 1
            print(f"[EX] BEQ tomado → PC salta a {self.proce.pc}")
        else:
            print("[EX] BEQ no tomado")
        print("BEQ terminada")

    def execute(self):
        if self.steps:
            self.steps.pop(0)()