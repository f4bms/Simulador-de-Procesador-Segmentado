class ALU:
    def __init__(self):
        self.active = False

    def OP(self, A, B, op):
        self.active = True  # Se activa al operar
        if op == 0:
            return A + B
        elif op == 1:
            return A - B
        elif op == 2:
            return A & B
        elif op == 3:
            return A | B
        elif op == 4:
            return A ^ B
        else:
            raise ValueError("No se reconoce la operacion")

    def clear_active(self):
        self.active = False  # Se desactiva