class instrMemory:
    def __init__(self):
        self.memory = []
        self.active = False

    def read(self, address):
        self.active = True  # Se activa al leer
        return self.memory[address]

    def __getitem__(self, address):
        self.active = True  # Se activa al acceder
        return self.memory[address]

    def clear_active(self):
        self.active = False  # Se desactiva