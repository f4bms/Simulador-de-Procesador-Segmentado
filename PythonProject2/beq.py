class BEQ:
    def __init__(self, rs1, rs2, imm, proce):
        self.rs1, self.rs2, self.imm = rs1, rs2, imm
        self.proce = proce
        self.steps = [self.id, self.ex]
        self.op1 = None
        self.op2 = None
        self.taken = False

        #Predicción de saltos
        self.predicted_taken = False
        self.original_pc = proce.pc

    def __str__(self):
        return f"BEQ x{self.rs1}, x{self.rs2}, {self.imm}"

    def __repr__(self):
        return str(self)

    def id(self):
        print("empezando beq")

        self.op1 = self.proce.regFile.read(self.rs1)
        self.op2 = self.proce.regFile.read(self.rs2)
        print(f"[ID] op1={self.op1} op2={self.op2}")

        if self.proce.branch_prediction:
            if self.proce.branch_prediction_mode == "always_taken":
                self.predicted_taken = True
                self.proce.pc += (self.imm // 4) - 1
                print(f"[Predict] Predicción: salto tomado (always taken)")
            elif self.proce.branch_prediction_mode == "always_not_taken":
                self.predicted_taken = False
                print("[Predict] Predicción: salto no tomado (always_not_taken)")

    def ex(self):
        actual_taken = (self.op1 == self.op2)
        if actual_taken:
            if not self.predicted_taken:
                self.proce.mispredictions += 1
                self.proce.pc = self.original_pc + (self.imm // 4)
                print(f"[EX] BEQ tomado (mispredicted) → PC corregido a {self.proce.pc}")
            else:
                print(f"[EX] BEQ tomado (correctly predicted)")
        else:
            if self.predicted_taken:
                self.proce.mispredictions += 1
                self.proce.pc = self.original_pc + 1
                print(f"[EX] BEQ no tomado (mispredicted) → PC corregido a {self.proce.pc}")
            else:
                print("[EX] BEQ no tomado (correctly predicted)")

        print("BEQ terminada")

    def execute(self):
        if self.steps:
            self.steps.pop(0)()

    # Métodos para hazard unit
    def uses_rs(self):
        return True

    def uses_rt(self):
        return True

    def modifies_rd(self):
        return False

    def is_branch(self):
        return True