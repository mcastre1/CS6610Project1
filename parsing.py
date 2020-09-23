import re

def hello():
    print("Hello")

"""
Split method, helper method to split instruction strings into an array.
Returns an array of tokens
"""
def split(line):
    line = line.replace(',', ' ')
    line = line.replace('\t', ' ')
    return line.split()

"""
translateInstruction Function translate a given instruction into its binary value
takes the instruction, data values which will be used for certain instructions, a program counter, and a list of labels.
returns a string combination of the binary representation of the given instruction.
"""
def translateInstruction(instruction, dataValues, PC, labelsOffset):
    out = ""

    #All these if/elif statements go through each instruction and check whether or not they can do something about it.
    if(instruction[0] == "addiu"):
        rs = format(int(instruction[2][1:]), '05b')
        rt = format(int(instruction[1][1:]), '05b')
        imm = format(int(instruction[3], 16), '016b')
        out += "001001{}{}{}".format(rs,rt,imm)
    elif(instruction[0]== "addu"):
        rs = format(int(instruction[2][1:]), '05b')
        rt = format(int(instruction[3][1:]), '05b')
        rd = format(int(instruction[1][1:]), '05b')
        out += "000000{}{}{}00000100001".format(rs, rt, rd)
    elif(instruction[0]== "and"):
        rd = format(int(instruction[1][1:]), '05b')
        rs = format(int(instruction[2][1:]), '05b')
        rt = format(int(instruction[3][1:]), '05b')
        out += "000000{}{}{}00000100100".format(rs, rt, rd)
    elif(instruction[0]== "andi"):
        rt = format(int(instruction[1][1:]), '05b')
        rs = format(int(instruction[2][1:]), '05b')
        imm = format(int(instruction[3], 16), '016b')
        out += "01100{}{}{}".format(rs, rt, imm)
    elif(instruction[0]== "beq"):
        rs = format(int(instruction[1][1:]), '05b')
        rt = format(int(instruction[2][1:]), '05b')
        offset = 0
        for value in labelsOffset:
            if(value.split(",")[0] == instruction[3]):
                #print("found label")
                labelPC = hex(int(value.split(",")[1]))
                instPC = hex(PC)

                offset = int((int(labelPC, 16) - (int(instPC, 16) + int("0x4", 16)))/4)
                offset = bin(offset & 0b1111111111111111)
        out += "000100{}{}{}".format(rs,rt,offset[2:].zfill(16))
    elif(instruction[0]== "bne"):
        rs = format(int(instruction[1][1:]), '05b')
        rt = format(int(instruction[2][1:]), '05b')
        offset = 0
        for value in labelsOffset:
            if(value.split(",")[0] == instruction[3]):
                labelPC = hex(int(value.split(",")[1]))
                instPC = hex(PC)

                offset = int((int(labelPC, 16) - (int(instPC, 16) + int("0x4", 16)))/4)
                offset = bin(offset & 0b1111111111111111)[2:]
        out += "000101{}{}{}".format(rs,rt,offset)
        #print("000101{}{}{}".format(rs,rt,offset))
    elif(instruction[0]== "j"):
        for value in labelsOffset:
            if(value.split(",")[0] == instruction[1]):
                labelPC = hex(int(value.split(",")[1]))
                instPC = hex(PC)
                textOffset = hex(int("0x400000", 16))

                off = (int(textOffset, 16) | int(labelPC, 16)) >> 2
                offset = format(off, '026b')
                out += "000010{}".format(offset)

    elif(instruction[0]== "jal"):
        print("")
    elif(instruction[0]== "jr"):
        rs = format(int(instruction[1][1:]), '05b')
        out += "000000{}000000000000000001000".format(rs)
    elif(instruction[0]== "lui"):
        rt = format(int(instruction[1][1:]), '05b')
        imm = format(int(instruction[2], 16), '016b')
        out += "00111100000{}{}".format(rt, imm)
    elif(instruction[0]== "lw"):
        rt = format(int(instruction[1][1:]), '05b')
        offset = int(instruction[2].split("(")[0])
        if(offset < 0):
            offset = bin(int(instruction[2].split("(")[0]) & 0b1111111111111111)
            offset = offset[2:]
        else:
            offset = format(int(instruction[2].split("(")[0]),'016b')

        base = instruction[2].split("(")[1]
        base = base[1:]
        base = base[:-1]
        base = format(int(base), '05b')
        out += "100011{}{}{}".format(base, rt, offset)
    elif(instruction[0]== "la"):
        h = 0
        for value in dataValues:
            if(instruction[2] == value.split(",")[0]):
                h = value.split(",")[1]

        rt = format(int(instruction[1][1:]), '05b')
        imm = "{0:016b}".format(int(h[0:6], 16))
        out += "00111100000{}{}".format(rt,imm)

        ori = checkLA(instruction, dataValues)
        if(ori):
            rs = format(int(instruction[1][1:]), '05b')
            rt = format(int(instruction[1][1:]), '05b')
            imm = "{0:016b}".format(int(h[6:12], 16))
            out += "001101{}{}{}".format(rs,rt,imm)
            
    elif(instruction[0]== "nor"):
        rd = format(int(instruction[1][1:]), '05b')
        rs = format(int(instruction[2][1:]), '05b')
        rt = format(int(instruction[3][1:]), '05b')
        out += "000000{}{}{}00000100111".format(rs,rt,rd)
    elif(instruction[0]== "or"):
        rd = format(int(instruction[1][1:]), '05b')
        rs = format(int(instruction[2][1:]), '05b')
        rt = format(int(instruction[3][1:]), '05b')
        out += "000000{}{}{}00000100101".format(rs,rt,rd)
    elif(instruction[0]== "ori"):
        rt = format(int(instruction[1][1:]), '05b')
        rs = format(int(instruction[2][1:]), '05b')
        imm = format(int(instruction[3], 16), '016b')
        out += "001101{}{}{}".format(rs,rt,imm)
    elif(instruction[0]== "sltiu"):
        rt = format(int(instruction[1][1:]), '05b')
        rs = format(int(instruction[2][1:]), '05b')
        imm = format(int(instruction[3], 16), '016b')
        out += "001011{}{}{}".format(rs,rt,imm)
    elif(instruction[0]== "sltu"):
        rd = format(int(instruction[1][1:]), '05b')
        rs = format(int(instruction[2][1:]), '05b')
        rt = format(int(instruction[3][1:]), '05b')
        out += "000000{}{}{}00000101011".format(rs,rt,rd)
    elif(instruction[0]== "sll"):
        rd = format(int(instruction[1][1:]), '05b')
        rt = format(int(instruction[2][1:]), '05b')
        sa = format(int(instruction[3]), '05b')
        out += "00000000000{}{}{}000000".format(rt,rd,sa)
    elif(instruction[0]== "srl"):
        rd = format(int(instruction[1][1:]), '05b')
        rt = format(int(instruction[2][1:]), '05b')
        sa = format(int(instruction[3]), '05b')
        out += "00000000000{}{}{}000010".format(rt,rd,sa)
    elif(instruction[0]== "sw"):
        rt = format(int(instruction[1][1:]), '05b')
        offset = int(instruction[2].split("(")[0])
        if(offset < 0):
            offset = bin(int(instruction[2].split("(")[0]) & 0b1111111111111111)
            offset = offset[2:]
        else:
            offset = format(int(instruction[2].split("(")[0]),'016b')

        base = instruction[2].split("(")[1]
        base = base[1:]
        base = base[:-1]
        base = format(int(base), '05b')
        out += "101011{}{}{}".format(base, rt, offset)
    elif(instruction[0]== "subu"):
        rd = format(int(instruction[1][1:]), '05b')
        rs = format(int(instruction[2][1:]), '05b')
        rt = format(int(instruction[3][1:]), '05b')
        out += "000000{}{}{}00000100011".format(rs,rt,rd)
    return out

"""
checkLA function is a helper function to check whether we use only lui when a la instruction is present or we use a lui and an ori instruction.
returns true if the lower 16 bits are not equal to 0
"""
def checkLA(instruction, dataValues):
    for value in dataValues:
        if(value.split(",")[0] == instruction[2]):
            lowerBits = value.split(",")[1][6:12]
            nonZeroCount = 0
            for i in lowerBits:
                if(not i == "0"):
                    nonZeroCount += 1
            
            if(nonZeroCount > 0):
                return True
            else:
                return False