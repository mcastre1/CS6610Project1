# Project 1. A Simple MIPS Assembler

- [Project 1. A Simple MIPS Assembler](#project-1-a-simple-mips-assembler)
  - [Team Info](#team-info)
  - [Purpose](#purpose)
    - [Instruction Set](#instruction-set)
  - [Directives](#directives)
  - [Memory Layout](#memory-layout)
  - [Execution command](#execution-command)
    - [Input format](#input-format)
    - [Output format](#output-format)
    - [Files to work on](#files-to-work-on)
      - [Compile Code project](#compile-code-project)
    - [Publish your code](#publish-your-code)
  
## Team Info

Team members:

- Member 1:
- Member 2:

Github Repository:

## Purpose

The objective of the first project is to implement a MIPS ISA assembler. The assembler is
the tool which converts assembly codes to a binary file. This project is intended to help you
understand the MIPS ISA instruction set.

The assembler you are going to design is a simplified assembler which do not support the
linking process, and thus you do not need to add the symbol and relocation tables for each
file. In this project, only one assemble fil will be the whole program.

You should implement the assembler which can convert a subset of the instruction set
shown in the following table. In addition, your assembler must handle labels for jump/branch
targets, and labels for the static data section.

### Instruction Set

The detailed information regarding instructions are in the **docs/** folder. This folder
contains two files:

- The official MIPS documentation.
- A book on MIPS assembly programming.

For this project you are need to support the following instructions:

| ADDIU | ADDU  | AND  | ANDI | BEQ | BNE | J    |
|-------|-------|------|------|-----|-----|------|
| JAL   | JR    | LUI  | LW   | LA* | NOR | OR   |
| ORI   | SLTIU | SLTU | SLL  | SRL | SW  | SUBU |

- Only instructions for **unsigned** operations need to be implemented. (`addu, addiu,
    subu, sltiu, sltu, sll, srl`)
- However, the immediate fields for certain instructions are sign extended to allow
    negative numbers (`addui, beq, bne, lw, sw, sltui`)
- Only loads and stores with `4B` word need to be implemented.
- The assembler must support decimal and hexadecimal numbers (`0x`) for the
    immediate field, and `.data` section.
- The register name is always `$n` where `n` is from `0 to 31`.

- `la` (load address) is a pseudo instruction; it should be converted to one or two
    assembly instructions.
  - For example: `la $2, VAR1` : `VAR1` is a label in the `data` section
  - It should be converted to `lui` and `ori` instructions.

For example:

```mips
la $register, VAR1
```

will be converted into:

```mips
lui $register, upper 16bit address
ori $register, lower 16bit address
```

If the lower 16 bits address is `0x0000`, the `ori` instruction is not required.

Case 1) load address is `0x1000 0000`

```mips
lui $2, 0x1000
```

This will be typically true for the first label you defined in the `.data` section.

Case 2) load address is `0x1000 0004`

```mips
lui $2, 0x1000
ori $2, $2, 0x0004
```

This will be typically true starting on the second label you defined in the `.data` section.

## Directives

`.text`

- indicates that following items are stored in the user text segment, typically
    instructions
- It always starts from `0x400000`
  
`.data`

- indicates that following data items are stored in the data segment
- It always starts from `0x10000000`
  
`.word`

- store n 32-bit quantities in successive memory words

You can assume that the `.data` and `.text` directives appear only once, and the `.data` must
appear before `.text` directive.

Assume that each word in the data section is initialized (Each word has an initial value).

## Memory Layout

![Memory](/images/memory.png)

---

## Execution command

```bash
> ./ca <assembly file>
```

Your program must produce a single output file (`.*o`) from the input assembly file (`*.s`).

### Input format

Your input files are located in the `sample_input/` folder.

### Output format

Your program output should be safe in the `sample_ouput/` folder.

The output of the assembler is an object file. We use a simplified custom format.

- The first word (32bits) is the size in bytes of `text` section
- The second word (32bits) is the size in bytes of the `data` section.
- The next bytes are the instructions in binary. The length must be equal to the
    specified text section length.
- After the text section, the rest of bytes are the initial values of the data section.

The following must be the final binary format:

<text section size>
<data section size>
<instruction 1>
...
<instruction n>

<value 1>
...
<value m>

I have included a sample output file `sample_output/example1.o` which corresponds
to the input file from `sample_input/example1.s`. A debug version of the output file
is also included.

### Files to work on

You can choose the programming language among C, C++, and Python. Since subsequent
project 2, 3, and 4 should be written in C/C++, I strongly recommend you use use C/C++
for the project to get familiar with the language, if you are not yet.

If you write it in C or C++, you may begin with the following file template:

- `README.md`: Update the student name an github account.
- All the functions you write, will be part of the library. The library consist of these files:
  - `src/rom.c` .  // for any functions related to the memory
  - `src/rom.h`
  - `src/parseline.c` .  // for any functions related to parsing strings
  - `src/parseline.h`
  - `src/vector.c` .  // Optional library to use vectors in C
  - `src/vector.h`
- Our "driver" will be `src/cs6610.c`.

You may modify the other CMakeLists.txt files as you add/remove files to your project.

---

#### Compile Code project

[How to compile and run the code with cmake.](faqs.md#how-to-compile-and-run-the-code-with-cmake)

### Publish your code

Make sure you [commit and push](https://code.visualstudio.com/docs/editor/versioncontrol) your code to your online repository
