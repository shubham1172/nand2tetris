# nand2tetris
This project is from the course [nand2tetris](https://www.nand2tetris.org/). From building logic gates to writing a high level language and an operating system in it, the resultant is a modern-day 16-bit computer which I have documented below. 

## Project Outcome
1. Bare bones hardware - The _Hack_ computer
2. Assembly language - The _Hack_ assembly
3. Virtual machine - The _Jack Virtual Machine_ (JVM)
4. High level language - The _Jack_ programming language
5. Operating System - The _Jack_ OS

## Table of Contents
1. [Hardware](#hardware) 
	- [Logic Gates](#logic-gates)
	- [ALU](#alu)
	- [Registers, RAM, and PC](#registers-ram-and-pc)
2. [Architecture](#architecture)
	- [Instruction Set](#instruction-set)
		- [The A-instruction](#the-a-instruction)
 		- [The C-instruction](#the-c-instruction)
	- [Memory](#memory)
	- [CPU](#cpu)
	- [Computer](#computer)
4. [Assembler](#assembler)
5. [Jack Virtual Machine](#jack-virtual-machine)
	- [The Stack](#the-stack)
	- [Program Control](#program-control)
	- [JVM and Hack](#jvm-and-hack)
6. [Compiler](#compiler)
	- [High Level Language](#high-level-language)
	- [Syntax Analysis](#syntax-analysis)
	- [Code Generation](#code-generation)
7. [Operating System](#operating-system)

# Hardware
This section aims at building the bare-bones of the computer. We first make simple logic gates and then leverage them to further make more sophisticated hardware. The logic is written in a custom Hardware Description Language (HDL) specified [here](https://docs.wixstatic.com/ugd/44046b_2cc5aac034ae49f4bf1650a3d31df32c.pdf).

## Logic Gates
All the logic gates are created from the primitive Nand gate. Here are a list of gates that were implemented.

- Nand, [Not](./projects/01/Not.hdl), [And](./projects/01/And.hdl), [Or](./projects/01/Or.hdl), [Xor](./projects/01/Xor.hdl)
- [Mux]((./projects/01/Mux.hdl)), [DMux](./projects/01/DMux.hdl)
- [Not16](./projects/01/Not16.hdl), [And16](./projects/01/And16.hdl), [Or16](./projects/01/Or16.hdl), [Mux16](./projects/01/Mux16.hdl) - 16-bit wide gates
- [Or8Way](./projects/01/Or8Way.hdl) - Or(x0,...,x7)
- [Mux4Way16](./projects/01/Mux4Way16.hdl), [Mux8Way16](./projects/01/Mux8Way16.hdl), [DMux4Way16](./projects/01/DMux4Way16.hdl), [DMux8Way16](./projects/01/DMux8Way16.hdl) - 16-bit wide with 4/8 inputs

## ALU
This ALU can compute eighteen functions using some minimal hardware design. It uses 6 control bits where each bit refers to a certain elementary operation.

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

## Registers, RAM and PC
Storage is realized using Data Flip-Flops (DFFs). Registers are 16-bit wide and are composed of DFFs. These registers are further stacked to create the random access memory (RAM). It allows reading/writing data from/to any address in constant time, irrespective of the physical location.

Finally, a program counter is also realized using a 16-bit register which has the following functions - reset to zero, load a particular value, and increment the current value.

List of chips implemented
* [Bit](./projects/03/a/Bit.hdl), [Register](./projects/03/a/Register.hdl)
* [RAM8](./projects/03/a/RAM8.hdl), [RAM64](./projects/03/a/RAM64.hdl), [RAM512](./projects/03/b/RAM512.hdl), [RAM4K](./projects/03/b/RAM4K.hdl), [RAM16K](./projects/03/b/16K.hdl)
* [PC](./projects/03/a/PC.hdl)

# Architecture
Bringing together all the circuitry, the computer is assembled in this section. The resultant device is a 16-bit von Neumann platform consisting of a CPU, two memory modules and two memory-mapped I/O devices - a screen and a keyboard.

There are two 16-bit registers A and D where D is the data register which intends at storing values, and A acts as a dual purpose register which can store both data and address. Depending on the instruction context, A's value can be interpreted as either data or a memory address. The A register allows direct memory access.

## Instruction Set
The complete instruction set reference is available at [this](https://docs.wixstatic.com/ugd/44046b_7ef1c00a714c46768f08c459a6cab45a.pdf).  There are two generic types of instructions available - *A-instruction* or *address instruction*, and *C-instruction* or *compute instruction*. Each instruction has a binary and symbolic representation.

### The A-instruction
This is used to set the A register to a 15-bit value. <br>
Instruction: ```@value``` <br>
Binary: ```0 v v v``` ```v v v v``` ```v v v v``` ```v v v v``` <br>

A-instruction allows setting a constant value at a memory address. It also allows the C-instruction to manipulate a certain memory location or make a jump to a particular location. The left-most bit ```0``` is the A-instruction opcode and the following bits are the 15-bit value.

### The C-instruction
C-instruction accounts for all the compute tasks on this computer. <br>
Instruction:```dest=comp;jump``` // Either dest/jump maybe empty and symbols are omitted accordingly. <br>
Binary:```1 x x a``` ```c1 c2 c3 c4``` ```c5 c6 d1 d2``` ```d3 j1 j2 j3```<br>

The left-most bit ```1``` is the C-instruction opcode and the next two bits are don't cares.  The ```comp``` field is specified by the a-bit and the six c-bits. The a-bit is responsible for selecting either A-register or Memory and the c-bits are the control bits for the ALU. The ```dest``` field is given by the d-bits which allow us to select a destination. Each bit is mapped to a particular location where data is written if the bit is set. 

|d-bit|location|
|---|---|
d1|A-register|
d2|D-register|
d3|Memory|

The last three bits are the jump bits which decide when to make the jump. Together with the two status bits from ALU, they guide the PC in deciding the next address.

j1|j2|j2|Mnemonic
---|---|---|---
0|0|0|null
0|0|1|JGT
0|1|0|JEQ
0|1|1|JGE
1|0|0|JLT
1|0|1|JNE
1|1|0|JLE
1|1|1|JMP

## Memory
This computer has two memory banks - instruction memory and data memory. The instruction memory is implemented using a ROM chip with 32K addressable 16-bit registers. The data memory is a RAM device consisting of 32K addressable 16-bit registers with provision for memory mapped IO.

The data memory is laid out with the RAM in the upper section, followed by IO memory buffers for the two peripheral devices - a 512 x 256 display and a keyboard. Data memory supports 15-bit addressing.
<table>
	<thead>
		<tr>
			<th> address </th>
			<th> component </th>
			<th> capacity </th>
		</tr>
	</thead>
	<tbody>
		<tr> 
			<td><center>0x0000 <br> - <br> 0x3FFF</center></td>
			<td>RAM </td>
			<td> 16K </td>
		</tr>
		<tr>
			<td><center>0x4000 <br> - <br> 0x5FFF </center></td>
			<td> Screen </td>
			<td> 8K </td>
		</tr>
		<tr>
			<td>0x6000</td>
			<td> Keyboard </td>
			<td> 1 </td>
		</tr>
	</tbody>
</table>

Implementation: [Memory Chip](./projects/05/Memory.hdl).

## CPU
The CPU consists on the ALU, two registers A and D, and a program counter PC. It fetches the instruction from the instruction memory and decodes it using internal circuitry of logic. It then executes the instruction and writes back the data.
![CPU](https://imgur.com/FR7RlI3.png)
<br><center>src: [nand2tetris computer architecture](https://docs.wixstatic.com/ugd/44046b_552ed0898d5d491aabafd8a768a87c6f.pdf) </center>

The control bits in the image above are labelled *c*. Different bits are routed to different parts of the CPU.

Implementation: [CPU Chip](./projects/05/CPU.hdl).

## Computer
Finally, the computer can be realized by connecting the instruction memory, CPU and the data memory. Final implementation - [Computer](./projects/05/Computer.hdl). This marks the complete hardware which powers everything on this device.
Finally, the computer can be realized by connecting the instruction memory, CPU and the data memory. Final implementation - [Computer](./projects/05/Computer.hdl). This marks the complete hardware which powers everything on this device.

# Assembler
An assembler is a piece of software that converts an assembly code into the device's machine code. This assembler is written in python and follows the instruction set as specified [above](#instruction-set). The assembler API is specified by [this](https://docs.wixstatic.com/ugd/44046b_b73759b866b249a0b3a715bf5a18f668.pdf). <br> <br>
To assemble a program: <br> 
```$ assembler.py /path/to/file.asm``` <br>

All mnemonic lookup hashtables are defined in [convert](./assembler/convert.py).<br>
All predefined symbols and symbol hashtable are defined in [symbol_table](./assembler/symbol_table.py). 

# Jack Virtual Machine
A virtual machine facilitates a two-tier compilation for our code. It handles intermediate logic and allows the high-level language to leverage its architecture than compile to raw assembly which is a really complex task. A VM translator is realized which translates program in the VM language to the Hack assembly. It is stack-based and supports four types of commands:

| | |
|---|---|
|Arithmetic|Perform arithmetic and logical operations on stack|
|Memory Access|Transfer data b/w stack and memory segments| 
|Program Flow|Conditional and unconditional braching ops|
|Function Calling|Call functions and return from them|

## Stack Arithmetic

### Arithmetic/Logical commands

There are nine commands out of which two are unary and seven are binary. The stack uses -1 (0xFFFF) for true and 0 (0x0000) for false.

|command|action|
|---|---|
|add|pop y, pop x, push x+y|
|sub|pop y, pop x, push x-y|
|and|pop y, pop x, push x&y|
|or|pop y, pop x, push x\|y|
|lt|pop y, pop x, push -1 if x<y, else 0|
|gt|pop y, pop x, push -1 if x>y, else 0|
|eq|pop y, pop x, push -1 if x=y, else 0|
|neg|pop x, push -x|
|not|pop x, push !x|

### Memory access commands

Memory commands can manipulate eight separate virtual memory segments. The command uses two variables which can select any memory location together. 

#### Pointer-based addressing

|segment|location|purpose|notes|
|---|---|---|---|
|argument|*(ARG+index)|store function's arguments|private to a function|
|local|*(LCL+index)|store function's local variables|private to a function|
|this|*(THIS+index)|store field variables of current object|can be used to manipulate certain heap areas|
|that|*(THAT+index)|store array entries|<center>"</center>|

#### Absolute addressing

|segment|location|purpose|notes|
|---|---|---|---|
|pointer|THIS(0) or THAT(1)|alter base ptrs for this/that segments|<center>-</center>|
|temp|R5-R12|global temporary variables|public access to everyone|
|static|filename.index|store static variables of a file|all functions in the file share it|
|constant|@index|store constants 0-(2^15-1) |emulated for consistency - pseudo segment|

These two commands can essentially realize any memory operation.

<pre>push <i>segment index</i></pre>
push the value at _index_ in _segment_ to the stack <br>
_segment_ can be - argument, local, static, constant, this, that, pointer or temp.<br>
_index_ is a non-negative integer.

<pre>pop <i>segment index</i></pre>
pop value off the stack and store at _index_ in _segment_<br>
_segment_ can be - argument, local, static, this, that, pointer or temp.<br>
_index_ is a non-negative integer.

### Data structures

There are two implicit data structures managed by the Virtual Machine without any explicit implementation in the software. Their state is managed with carefully written pseudo commands.

1. Stack - The working memory of the VM operations is a stack. All operations are facilitated using a stack.
2. Heap- An area in RAM dedicated for storing objects and data structures like arrays.

## Program Control

## JVM and Hack

Abstract notions of the VM defined above sounds good, but there should be a contract between the principles listed and the hardware it will run on, i.e. the Hack computer.

### RAM Usage

The Hack data memory consists of 32k 16-bit words - refer [memory](#Memory). The VM implementation uses the space as follows

|Address|Usage|
|---|---|
|0-15|16 virtual registers (described below)|
|16-255|Static variables|
|256-2047|Stack memory|
|2048-16383|Heap memory|
|16384-24575|Memory mapped I/O|

### Hack registers

The first 16 registers can be addressed using the assembly as R0-R15. However, VM introduces some conventions for easy readibility and accessibility. 

|Register(s)|Name|Usage|
|---|---|---|
|R0|SP|Stack Pointer|
|R1|LCL|Points to _local_ segment|
|R2|ARG|Points to _argument_ segment|
|R3|THIS|Points to _this_ segment (in heap)|
|R4|THAT|Points to _that_ segment (in heap)|
|R5-R12|-|Holds content of _temp_ segment|
|R13-R15|-|Can be used as general-purpose registers|

