"""
Convert mnemonics into machine code

@author:shubham1172
"""

def dest(mnemonic):
    """
    :param mnemonic: in original command
    :return: code for it
    """
    data = ['', 'M', 'D', 'MD', 'A', 'AM', 'AD', 'AMD']
    return bin(data.index(mnemonic))[2:].zfill(3)


def comp(mnemonic):
    """
    :param mnemonic: in original command
    :return: code for it
    """
    data = {
        "": "0000000",
        "0": "0101010",
        "1": "0111111",
        "-1": "0111010",
        "D": "0001100",
        "A": "0110000",
        "!D": "0001101",
        "!A": "0110001",
        "-D": "001111",
        "-A": "0110011",
        "D+1": "0011111",
        "A+1": "0110111",
        "D-1": "0001110",
        "A-1": "0110010",
        "D+A": "0000010",
        "D-A": "0010011",
        "A-D": "0000111",
        "D&A": "0000000",
        "D|A": "0010101",
        "M": "1110000",
        "!M": "1110001",
        "-M": "1110011",
        "M+1": "1110111",
        "M-1": "1110010",
        "D+M": "1000010",
        "D-M": "1010011",
        "M-D": "1000111",
        "D&M": "1000000",
        "D|M": "1010101"
    }
    return data[mnemonic]


def jump(mnemonic):
    """
    :param mnemonic: in original command
    :return: code for it
    """
    data = ["", "JGT", "JEQ", "JGE", "JLT", "JNE", "JLE", "JMP"]
    return bin(data.index(mnemonic))[2:].zfill(3)
