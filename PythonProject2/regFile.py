class regFile:
    def __init__(self):
        self.reg = [0] * 32
        self.active = False

    def read(self, reg_num):
        self.active = True  # Se activa al leer
        return self.reg[reg_num]

    def write(self, reg_num, value):
        self.active = True  # Se activa al escribir
        if reg_num != 0:  # x0 es siempre cero
            self.reg[reg_num] = value

    def clear_active(self):
        self.active = False  # Se desactiva