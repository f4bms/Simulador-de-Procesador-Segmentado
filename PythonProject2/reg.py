#temporary register between etapas
class Registr:
    def __init__(self):
        self.instr = None
        self.data = None

#para vaciar lo que tengo en el reg
    def clear(self):
        self.instr = None
        self.data = None