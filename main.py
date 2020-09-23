#!/usr/bin/env python
# -*- coding: utf-8 -*-
import parsing
#List used to keep track and check which instructions are acceptable.
instruction_list = ["addiu","addu","and","andi","beq","bne","j",
                    "jal","jr","lui","lw","la","nor","or",
                    "ori","sltiu","sltu","sll","srl","sw","subu"]

#list to keep track of which data types are acceptable.
dataTypes = [".word"]
#List to keep track of every label and its program counter.
labelsOffset = []
#List to keep track of all the used data values in the assembly file.
dataValues = []

def main():
    filePath = "sample_input/example1.s"
    dataCount = 0
    textCount = 0
    data = False
    text = False
    PC = 0
    
    #Data offset starts at 0x10000000
    dataPC = int("10000000", base=16)
    out = ""

    #In this first while loop we go through and keep track of labels, data values, number of instructions and number of data values.
    with open(filePath) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            instArray = parsing.split(line.strip())

            #These two if statements above just keep track of where in the file we are.
            if(instArray[0] == ".data"):
                data = True
                text = False
                
            elif(instArray[0] == ".text"):
                data = False
                text = True
                
            if(data):
                #Here we add to our datavalues list, depending on whether the data type is acceptable.
                if(len(instArray) == 3):
                    if(instArray[1] in dataTypes):
                        dataCount += 1
                        dataValues.append("{},{},{}".format(instArray[0][:-1],hex(dataPC),instArray[2]))
                        dataPC += 4
                        #print(hex(dataPC))
            if(text):
                #Check whether or not the line is a label.
                if(not ":" in instArray[0] and not "." in instArray[0]):
                    textCount += 1
                    #print("Counted this as text instruction")
                    if(instArray[0] in instruction_list):
                        PC += 4
                        if(instArray[0] == "la"):
                            ori = False
                            ori = parsing.checkLA(instArray, dataValues)
                            if(ori):
                                #print("Need ori instruction")
                                PC += 4
                                textCount += 1
                elif(":" in instArray[0] and not instArray[0] == "main:"):
                    labelsOffset.append("{},{}".format(instArray[0][:-1], PC))

            
            line = fp.readline()
            cnt += 1

    #for x in labelsOffset:
        #print(x)

    out += format(textCount*4, '032b')
    out += format(dataCount*4, '032b')
    
    PC = int("0", base=16)

    #In this second while loop is where we start using the above variables and we translate each instruction into its binary form.
    with open(filePath) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            instArray = parsing.split(line.strip())
            #print(instArray)
            
            if(instArray[0] in instruction_list):
                #print(hex(PC))
                out += parsing.translateInstruction(instArray, dataValues, PC, labelsOffset)
                #As a special case, la will be checked for and only if its lower 16 values are greater than 0 we will add another instruciton to our program.
                if(instArray[0] == "la"):
                    ori = parsing.checkLA(instArray, dataValues)
                    if(ori):
                        PC += 4
                PC += 4

            line = fp.readline()
            cnt += 1

    #Here we just printout every data value we currently have in our list.
    for data in dataValues:
        if("0x" in data.split(",")[2]):
            number = int(data.split(",")[2], 16)
            number = format(number, '032b')
            out += number
            #print(number)
        else:
            number = int(data.split(",")[2])
            number = format(number, '032b')
            out += number
            #print(number)

    print(out)
    #print("text {}".format(textCount))
    return 0

if __name__ == "__main__":
    main()