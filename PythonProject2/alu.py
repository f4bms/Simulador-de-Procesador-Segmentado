class ALU:
    def __init__(self):
        pass

    def OP(self, A, B, op):
        if op == 0:
            return A + B
        elif op == 1:
            return A - B
        elif op == 2:
            return A & B
        elif op == 3:
            return A | B
        else:
            raise ValueError("No se reconoce la operacion")