class dataMemory:
    def __init__(self):
        self.memory = [None] * 32
        self.active = False
        self.last_accessed = None
        self.was_write = False

    def read(self, address):
        self.active = True  # Se activa al leer
        self.last_accessed = address
        self.was_write = False
        return self.memory[address]

    def write(self, address, value):
        self.active = True  # Se activa al escribir
        self.last_accessed = address
        self.was_write = True
        self.memory[address] = value

    def clear_active(self):
        self.active = False  # Se desactiva