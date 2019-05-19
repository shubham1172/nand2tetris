"""
Symbol table for the assembler

@author: shubham1172
"""


class SymbolTable:
    def __init__(self):
        # predefined data
        self.data = {
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4,
            "SCREEN": 16384,
            "KBD": 24576
        }
        for i in range(0, 16):
            self.data["R%d" % i] = i
        # counter for variables
        self.next_address = 16

    def contains(self, symbol):
        return symbol in self.data

    def put_variable(self, symbol):
        self.data[symbol] = self.next_address
        self.next_address += 1
        return self.next_address - 1

    def put_label(self, symbol, address):
        self.data[symbol] = address

    def get(self, symbol):
        return self.data[symbol]
