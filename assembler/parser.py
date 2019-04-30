"""
Parse the assembly into machine code

@author:shubham1172
"""
import code
from enum import Enum
from symbol_table import SymbolTable


class CommandType(Enum):
    A_COMMAND = 1  # a-type @value
    C_COMMAND = 2  # c-type dest=comp;jmp
    L_COMMAND = 3  # labels (LABEL)


class Parser:
    def __init__(self, data):
        """
        :param data: lines of assembly program
        """
        self.current_idx = -1
        self.symbol_table = SymbolTable()
        self.data = self.preprocess(data)

    def preprocess(self, raw):
        data = []
        curr_address = 0
        for i in range(len(raw)):
            raw[i] = raw[i].strip().split("//")[0].strip()
            if raw[i] != "":
                if Parser.command_type(raw[i]) == CommandType.L_COMMAND:
                    symbol = self.symbol(raw[i])
                    self.symbol_table.put_label(symbol, curr_address)
                else:
                    curr_address += 1
                data.append(raw[i])
        return data

    def has_more_commands(self):
        """
        :return: if more commands are available
        """
        return self.current_idx < (len(self.data) - 1)

    def next_command(self):
        """
        read next command
        make it the current command
        """
        self.current_idx += 1
        return self.data[self.current_idx]

    @staticmethod
    def command_type(command):
        """
        :return: command type of the command
        """
        if command[0] == '@':
            return CommandType.A_COMMAND
        elif command[0] == '(' and command[-1] == ')':
            return CommandType.L_COMMAND
        else:
            return CommandType.C_COMMAND

    def symbol(self, command):
        """
        :return: symbol or decimal @Xxx or (Xxx)
        """
        if command[0] == '@':
            # @Xxx
            symbol = command[1:]
            if symbol.isnumeric():
                return symbol
            if self.symbol_table.contains(symbol):
                return self.symbol_table.get(symbol)
            else:
                return self.symbol_table.put_variable(symbol)
        else:
            # (Xxx)
            return command[1:-1]

    @staticmethod
    def dest(command):
        """
        :return: dest mnemonic in current C-command
        """
        if "=" in command:
            return command.split('=')[0]
        else:
            return ""

    @staticmethod
    def comp(command):
        """
        :return: comp mnemonic in current C-command
        """
        if "=" in command:
            return command.split('=')[1]
        elif ";" in command:
            return command.split(";")[0]
        else:
            return ""

    @staticmethod
    def jump(command):
        """
        :return: jump mnemonic in current C-command
        """
        if ";" in command:
            return command.split(';')[1]
        else:
            return ""

    def parse(self):
        out = []
        while self.has_more_commands():
            command = self.next_command()
            c_type = Parser.command_type(command)
            if c_type == CommandType.A_COMMAND:
                # a-instruction
                address = self.symbol(command)
                out.append(bin(int(address))[2:].zfill(16))
            elif c_type == CommandType.C_COMMAND:
                # c-instruction
                dest = Parser.dest(command)
                comp = Parser.comp(command)
                jump = Parser.jump(command)
                out.append("111"+code.comp(comp)+code.dest(dest)+code.jump(jump))
        return [line + '\n' for line in out]
