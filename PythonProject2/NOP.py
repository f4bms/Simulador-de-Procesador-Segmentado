class NOP:
    def __init__(self, proce=None):
        self.proce = proce
        self.steps = [self.step]  # solo un paso

    def step(self):
        print("NOP ejecutado (burbuja)")

    def execute(self):
        if self.steps:
            fase = self.steps.pop(0)
            fase()

    # Métodos para hazard unit
    def uses_rs(self):
        return False

    def uses_rt(self):
        return False

    def modifies_rd(self):
        return False