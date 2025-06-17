class SW:
    def __init__(self, rd, imm, rs1, proce):
        """
        rd   ➜ rs2 en RISCV (dato a escribir)
        imm  ➜ desplazamiento
        rs1  ➜ registro base (dirección)
        """
        self.rd   = rd      # registro con el DATO (rs2)
        self.imm  = imm     # desplazamiento
        self.rs1  = rs1     # registro base (rs1)
        self.proce = proce
        self.steps = [self.step1, self.step2, self.step3]

    # ────────────────── ID ──────────────────
    def step1(self):
        print("empezando sw")
        # base = x[rs1]; dato = x[rd]  (rd funciona como rs2)
        self.base = self.proce.regFile.reg[self.rs1]
        self.data = self.proce.regFile.reg[self.rd]
        print("valor base =", self.base, "dato =", self.data)

    # ────────────────── EX ──────────────────
    def step2(self):
        # dirección = base + imm
        self.addr = self.proce.alu.OP(self.base, self.imm, 0)   # 0 = suma
        print("dirección =", self.addr)

    # ───────────────── MEM ──────────────────
    def step3(self):
        self.proce.dataMem.memory[self.addr] = self.data
        print(f"dato escrito: Mem[{self.addr}] <- {self.data}\nSW terminada")

    # Avanza una fase por ciclo
    def execute(self):
        if self.steps:
            fase = self.steps.pop(0)
            fase()
