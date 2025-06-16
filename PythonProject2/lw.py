class LW:
        def __init__(self, rd, imm, rs1, proce):

            self.rd = rd
            self.imm = imm
            self.rs1 = rs1
            self.proce = proce

            self.steps = [self.step1, self.step2, self.step3, self.step4]

        def step1(self):
            self.proce.regRegFile.data = self.proce.regFile.reg[self.rs1]
            print("valor =",self.proce.regRegFile.data)

        def step2(self):
            self.proce.alu_reg.data = self.proce.alu.OP(self.proce.regRegFile.data, self.imm,0)
            print("dirección =", self.proce.alu_reg.data)

        def step3(self):
            addr = self.proce.alu_reg.data
            self.proce.reg_data.data = self.proce.dataMem.memory[addr]
            print("dato =", self.proce.reg_data.data)

        def step4(self):
            self.proce.regFile.reg[self.rd] = self.proce.reg_data.data
            print("resultado =", self.proce.regFile.reg[self.rd])

        def execute(self):
            if self.steps:
                fase = self.steps.pop(0)
                fase()
                if not self.steps:  # ya se ejecutó la última etapa
                    print("terminó")