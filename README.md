
# nand2tetris
This project is from the course [nand2tetris](https://www.nand2tetris.org/). From building logic gates to writing a high level language and an operating system in it, the outcome of this project is a modern-day computer which I have documented below.

## Table of contents
1. [Hardware](#hardware) 
	- [Boolean Logic](#booleanlogic)
	- [Boolean Arithmetic](#booleanarithmetic)
	- [Sequential Logic](#sequentiallogic)
2. [Architecture](#architecture)
	- [Machine Language](#machinelanguage)
	- [Computer Architecture](#computerarchitecture) 
3. [Assembler](#assembler)
4. [Virtual Machine](#virtualmachine)
	- [Stack Arithmetic](#stackarithmetic)
	- [Program Control](#programcontrol) 
5. [Compiler](#compiler)
	- [High Level Language](#highlevellanguage)
	- [Syntax Analysis](#syntaxanalysis)
	- [Code Generation](#codegeneration)
6. [Operating System](#operatingsystem)

# Hardware
This section aims at building the bare-bones of the computer. We first make simple logic gates and then leverage them to further make more sophisticated hardware. The logic is written in a custom Hardware Description Language (HDL) specified [here](https://docs.wixstatic.com/ugd/44046b_2cc5aac034ae49f4bf1650a3d31df32c.pdf).

## Boolean Logic
All the logic gates are created from the primitive Nand gate. Here are a list of gates that were implemented.

- Nand, [Not](./projects/01/Not.hdl), [And](./projects/01/And.hdl), [Or](./projects/01/Or.hdl), [Xor](./projects/01/Xor.hdl)
- [Mux]((./projects/01/Mux.hdl)), [DMux](./projects/01/DMux.hdl)
- [Not16](./projects/01/Not16.hdl), [And16](./projects/01/And16.hdl), [Or16](./projects/01/Or16.hdl), [Mux16](./projects/01/Mux16.hdl) - 16-bit wide gates
- [Or8Way](./projects/01/Or8Way.hdl) - Or(x0,...,x7)
- [Mux4Way16](./projects/01/Mux4Way16.hdl), [Mux8Way16](./projects/01/Mux8Way16.hdl), [DMux4Way16](./projects/01/DMux4Way16.hdl), [DMux8Way16](./projects/01/DMux8Way16.hdl) - 16-bit wide with 4/8 inputs

## Boolean Arithmetic
We implement our ALU in this section. Using minimal hardware, our ALU can compute eighteen functions. It uses 6 control bits where each bit refers to a certain elementary operation.

|control-bit|description|
|---|---|
|zx|zero the x input?|
|nx|negate the x input?|
|zy|zero the y input?|
|ny|negate the y input?|
|f|compute x+y (if 1) or x&y (if 0)|
|no|negate the output?|

The following functions can be computed with the control bits as follows:

#|zx|nx|zy|ny|f|no|f(x,y)
---|---|---|---|---|---|---|---
1|1|0|1|0|1|0|0
2|1|1|1|1|1|1|1
3|1|1|1|0|1|0|-1
4|0|0|1|1|0|0|x
5|1|1|0|0|0|0|y
6|0|0|1|1|0|1|!x
7|1|1|0|0|0|1|!y
8|0|0|1|1|1|1|-x
9|1|1|0|0|1|1|-y
10|0|1|1|1|1|1|x+1
11|1|1|0|1|1|1|y+1
12|0|0|1|1|1|0|x-1
13|1|1|0|0|1|0|y-1
14|0|0|0|0|1|0|x+y
15|0|1|0|0|1|1|x-y
16|0|0|0|1|1|1|y-x
17|0|0|0|0|0|0|x&y
18|0|1|0|1|0|1|x\|y

The ALU also produces two status bits with the output.

|status-bit|description|
|---|---|
|zr|is the output zero?|
|ng|is the output negative?|

The following chips were implemented in this section
* [HalfAdder](./projects/02/HalfAdder.hdl), [FullAdder](./projects/02/FullAdder.hdl)
* [Add16](./projects/02/Add16.hdl), [Inc16](./projects/02/Inc16.hdl)
* [ALU](./projects/02/ALU.hdl)

**Future work**: It will be better to replace the naive ripple carry adder in Add16 with a more efficient one like a carry-lookahead adder.
