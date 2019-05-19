#!/usr/bin/python3
"""
Jack Virtual Machine translator
https://www.nand2tetris.org

@author: shubham1172
"""
import sys
import argparse
from parser import Parser

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('path')
args = arg_parser.parse_args()

file, data = None, None
try:
    file = open(args.path)
    if args.path[-3:] != '.vm':
        raise NameError()
    data = file.readlines()
    file.close()
except FileNotFoundError:
    print("file not found at the requested path")
    sys.exit(-1)
except NameError:
    print("file must have a .vm extension")
    sys.exit(-1)

parser = Parser(data, ".".join(file.name.split("/")[-1].split(".")[:-1]))
out = parser.parse()
try:
    file = open(args.path[:-3] + '.asm', 'w')
    file.writelines(out)
    file.close()
except FileExistsError:
    print('error writing file - file already exists')
    sys.exit(-1)
