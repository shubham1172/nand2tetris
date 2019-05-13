"""
Parse the VM code into Hack machine code

@author:shubham1172
"""
import convert
from enum import Enum

class CommandType(Enum):
    ARITHMETIC = 0,
    PUSH=1,
    POP=2,
    LABEL=3,
    GOTO=4,
    IF=5,
    FUNCTION=6,
    RETURN=7,
    CALL=8


class Parser:
    def __init__(self, data):
        """
        :param data: lines of VM program
        """
        self.current_idx = -1
        self.data = data
        self.preprocess()

    def preprocess(self):
        """
        clean the input data
        remove comments
        """
        data = []
        for line in self.data:
            line = line.strip().split('//')[0].strip()
            if line != "":
                data.append(line)
        self.data = data

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
        :return: type of command
        """
        tokens = command.split(" ")
        if tokens[0] == 'push':
            return CommandType.PUSH
        elif tokens[0] == 'pop':
            return CommandType.POP
        elif tokens[0] in ['add', 'sub', 'and', 'or', 'lt', 'gt', 'eq', 'neg', 'not']:
            return CommandType.ARITHMETIC
        elif tokens[0] == 'label':
            return CommandType.LABEL
        elif tokens[0] == 'goto':
            return CommandType.GOTO
        elif tokens[0] == 'if-goto':
            return CommandType.IF
        elif tokens[0] == 'function':
            return CommandType.FUNCTION
        elif tokens[0] == 'call':
            return CommandType.CALL
        elif tokens[0] == 'return':
            return CommandType.RETURN
        else:
            raise Exception('Command type is unknown')

    @staticmethod
    def arg1(command):
        """
        :return: first argument of command
        """
        if Parser.command_type(command) == CommandType.ARITHMETIC:
            return command
        elif Parser.command_type(command) != CommandType.RETURN:
            return command.split(" ")[1]
        else:
            raise Exception('Argument1 does not exist')

    @staticmethod
    def arg2(command):
        """
        :return: second argument of command
        """
        if Parser.command_type(command) in [
            CommandType.PUSH, CommandType.POP, CommandType.FUNCTION, CommandType.CALL]:
            return command.split(" ")[2]
        else:
            raise Exception('Argument2 does not exist')

    def parse(self):
        out = []
        while self.has_more_commands():
            command = self.next_command()
            c_type = Parser.command_type(command)
            if c_type == CommandType.PUSH:
                out += convert.push(Parser.arg1(command), Parser.arg2(command))
            elif c_type == CommandType.POP:
                out += convert.pop(Parser.arg1(command), Parser.arg2(command))
            elif c_type == CommandType.ARITHMETIC:
                out += convert.arithmetic(command)
        return [line + '\n' for line in out]


