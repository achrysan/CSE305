#!/usr/bin/env python
import sys
myStack = list();

def hw2(inString, outString):
    file_read = open(inString, 'r')
    text_in_f = file_read.readlines()
    print(text_in_f)
    file_write = open(outString, 'w')
    for line in text_in_f:
        line = line[:-1]
        print("The line: \""+line+"\"")
        if line[:4] == "push":
            value = line[5:len(line)]
            try:
                if '.' in line:
                    push_val(":error:")
                else:
                    push_val(int(value))
            except:
                push_val(":error:")

        elif line == "pop":
            pop_val()#line[4:len(line)])
        elif line == ":true:" or line == ":false:" or line == ":error:":
            push_val(line)
        elif line == "add":
            add_vals()
        elif line == "sub":
            sub_vals()
        elif line == "mul":
            mul_vals()
        elif line == "div":
            div_vals()
        elif line == "rem":
            rem_vals()
        elif line == "neg":
            neg_val()
        elif line == "swap":
            swap_vals()
        elif line == "qui" or line == "quit":
            print("\nThis is what's being written to the file:")
            print(*myStack, sep="\n")
            for item in myStack:
                file_write.write("%s\n" % item)
            sys.exit()
            
def push_val(myVal):
    """if((not(isinstance(myVal,int))) and myVal!= ":true:" or myVal!= ":false:" or myVal != ":error:"):
        myStack.insert(0, ":error:")
        return myStack
    if(isinstance(myVal,int):
       myStack.insert("""
    myStack.insert(0,myVal)
    print(myVal,"is being pushed onto the stack")
    print(*myStack, sep="\n")
    print("")
    return myStack

def pop_val():
    if len(myStack) != 0:
        print(myStack[0],"is being pop'd off the stack")
        myStack.remove(myStack[0])
        return myStack
    else:
        pass

def add_vals():
    print("adding")
    if len(myStack)>1:
        myVal_1 = myStack[0]
        myVal_2 = myStack[1]
        if isinstance(myVal_1,int) and isinstance(myVal_2,int):
            result = myVal_2 + myVal_1
            print("result: ",result)
            pop_val()
            pop_val()
            push_val(result)
        else:
            push_val(":error:")
    else:
        push_val(":error:")


def sub_vals():
    print("subtracting")
    if len(myStack)>1:
        myVal_1 = myStack[0]
        myVal_2 = myStack[1]
        if isinstance(myVal_1,int) and isinstance(myVal_2,int):
            result = myVal_2 - myVal_1
            print("result: ",result)
            pop_val()
            pop_val()
            push_val(result)
        else:
            push_val(":error:")
    else:
        push_val(":error:")

def mul_vals():
    print("multiplying")
    if len(myStack)>1:
        myVal_1 = myStack[0]
        myVal_2 = myStack[1]
        if isinstance(myVal_1,int) and isinstance(myVal_2,int):
            result = myVal_2 * myVal_1
            print("result: ",result)
            pop_val()
            pop_val()
            push_val(result)
        else:
            push_val(":error:")
    else:
        push_val(":error:")

def div_vals():
    print("dividing")
    if len(myStack)>1:
        myVal_1 = myStack[0]
        myVal_2 = myStack[1]
        if isinstance(myVal_1,int) and isinstance(myVal_2,int) and myVal_2 != 0:
            result = myVal_2 // myVal_1
            print("result: ",result)
            pop_val()
            pop_val()
            push_val(result)
        else:
            push_val(":error:")
    else:
        push_val(":error:")

def rem_vals():
    print("modulating")
    if len(myStack)>1:
        myVal_1 = myStack[0]
        myVal_2 = myStack[1]
        if isinstance(myVal_1,int) and isinstance(myVal_2,int) and myVal_2 != 0:
            result = myVal_2 % myVal_1
            print("result: ",result)
            pop_val()
            pop_val()
            push_val(result)
        else:
            push_val(":error:")
    else:
        push_val(":error:")

def neg_val():
    print("negating")
    if len(myStack)>0:
        myVal_1 = myStack[0]
        if isinstance(myVal_1,int):
            result = 0 - myVal_1
            pop_val()
            push_val(result)
            print("result: ",result)
        else:
            push_val(":error:")
    else:
        push_val(":error:")

def swap_vals():
    print("swapping")
    if len(myStack)>1:
        temp = myStack[0]
        myStack[0] = myStack[1]
        myStack[1] = temp
        print(*myStack, sep="\n")
    else:
        push_val(":error:")
        print(*myStack, sep="\n")
