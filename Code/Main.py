"""from Imports import Branch
from Imports import LogConfig"""


class CPU:
    maxReg = 4
    maxMem = 256

    def __init__(self):
        self.registers = [0 for _ in range(self.maxReg)]
        self.memory = [0 for _ in range(self.maxMem)]
        self.pc = 0
        self.ir = 0
        self.state = True

    def fetch(self):
        self.ir = self.memory[self.pc]
        self.ir += 1

    def decode(self):
        pass

    def execute(self):
        pass

    def run(self):
        while self.state:
            self.fetch()
            self.decode()
            self.execute()


if __name__ == "__main__":
    instance = CPU()