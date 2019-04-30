// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

//  R10 stores what to write on the screen
//  R11 stores the last address to write on
//  Algorithm:
//  read keypress and store FFFF or 0000 in R10
//  loop from screen's start address to end address (R11)
//      populate each word with R10

@24576
D=A
@R11
M=D         // R11 = screen end address
(INF)
    @24576
    D=M     // D = key press value
    @WHITE
    D;JEQ   // if D == 0, paint white
    @BLACK
    0;JMP   // else paint black
    @INF
    0;JEQ
(BLACK)     // blacken the screen
    @0
    D=!A
    @R10
    M=D     // R10 = !0
    @LOOPSTART
    0;JMP
(WHITE)     // whiten the screen
    @R10
    M=0     // R10 = 0  
(LOOPSTART) // put R10 in all pixels
    @SCREEN
    D=A
    @i
    M=D     // i = SCREEN
(LOOP)
    @R10
    D=M
    @i
    A=M
    M=D     // @i = R10
    @i
    M=M+1   // i = i + 1
    D=M
    @R11
    D=M-D   // i = R11 - i
    @LOOP
    D;JGT
    @INF
    0;JMP