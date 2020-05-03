# Hack-Assembler
Hack assembler for the 6th Nand2Tetris project, implemented in Python.
Main file is assembler, bincode and binparser are modules.

Assembler takes in an .asm file and outputs a .hack file.
Basically, it takes the machine language written in the input file and converts it into binary code for the computer.

Input file can contain:
  - Comments -> starting with //;
  - A-instructions -> @ sign, followed by a memory register address, variable or label;
  - C-instructions -> dest=comp;jmp, where dest is the destination, comp is the computation (addition, substraction, logical operations) and jmp is the jump condition, based on a logical operation relative to 0 (greater than, equal to, less than, etc.).
