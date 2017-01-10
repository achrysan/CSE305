#!/usr/bin/env python
import sys
import copy
myStack = list();
myMap = dict();
temp = list();
envHolder = list();
global counter
counter = 0
def hw3(inString, outString):
    file_read = open(inString, 'r')
    text_in_f = file_read.readlines()
    print(len(text_in_f))
    file_write = open(outString, 'w')
    for line in text_in_f:
        line = line[:-1]
        print("The line: \""+line+"\"")
        if line[:4] == "push":
            value = line[5:len(line)]
            try:
                if value[0] == "\"" and value[len(value)-1] == "\"":
                    value = value[1:len(value)-1]
                    value = value + '`'
                    push_val(value)
                elif value[0].isalpha():
                    push_val(value)
                elif '.' in line:
                    push_val(":error:")
                else:
                    push_val(int(value))
            except:
                push_val(":error:")

        elif line == "pop":
            pop_val()
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
        elif line == "and":
            comp_and()
        elif line == "or":
            comp_or()
        elif line == "not":
            comp_not()
        elif line == "equal":
            comp_equal()
        elif line == "lessThan":
            comp_lessThan()
        elif line == "bind":
            bind()
        elif line == "if":
            comp_if()
        if line == "let":
            push_val("xletx")
        elif line == "end":
            topval = top_val(myStack)
            pop_val()
            while myStack[0]!= "xletx":
                pop_val()
            pop_val()
            push_val(topval)
        elif line == "qui" or line == "quit":
            print("\nThis is what's being written to the file:")
            print(*myStack, sep="\n")
            for item in myStack:
                if isinstance(item, str):
                    if item[len(item)-1] == '`':
                        item = item[0:len(item)-1]
                    else:
                        pass
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
        push_val(":error:")
def top_val(myStack):
    if len(myStack) != 0:
        return myStack[0]
    else:
        pass
    
def add_vals():
    print("adding")
    if len(myStack)>1:
        myVal_1 = myStack[0]
        myVal_2 = myStack[1]
        for x in myMap:
            if x == myVal_1:
                myVal_1 = myMap[myVal_1]
        for x in myMap:
            if x == myVal_2:
                myVal_2 = myMap[myVal_2]
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
        for x in myMap:
            if x == myVal_1:
                myVal_1 = myMap[myVal_1]
        for x in myMap:
            if x == myVal_2:
                myVal_2 = myMap[myVal_2]
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
        for x in myMap:
            if x == myVal_1:
                myVal_1 = myMap[myVal_1]
        for x in myMap:
            if x == myVal_2:
                myVal_2 = myMap[myVal_2]
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
        for x in myMap:
            if x == myVal_1:
                myVal_1 = myMap[myVal_1]
        for x in myMap:
            if x == myVal_2:
                myVal_2 = myMap[myVal_2]
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
        for x in myMap:
            if x == myVal_1:
                myVal_1 = myMap[myVal_1]
        for x in myMap:
            if x == myVal_2:
                myVal_2 = myMap[myVal_2]
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
        for x in myMap:
            if x == myVal_1:
                myVal_1 = myMap[myVal_1]
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

def comp_and():
    print("checking -and-")
    if len(myStack)>1:
        myVal_1 = myStack[0]
        myVal_2 = myStack[1]
        for x in myMap:
            if x == myVal_1:
                myVal_1 = myMap[myVal_1]
        for x in myMap:
            if x == myVal_2:
                myVal_2 = myMap[myVal_2]
        if myVal_1 != ":true:" and myVal_1 != ":false:" or myVal_2 != ":true:" and myVal_2 != ":false:":
            push_val(":error:")
        else:
            if myVal_1 == myVal_2:
                temp = myVal_1
                pop_val()
                pop_val()
                push_val(temp)
            elif myVal_1 == ":false:" or myVal_2 == ":false:":
                pop_val()
                pop_val()
                push_val(":false:")
    else:
        push_val(":error:")

def comp_or():
    print("checking -or-")
    if len(myStack)>1:
        myVal_1 = myStack[0]
        myVal_2 = myStack[1]
        for x in myMap:
            if x == myVal_1:
                myVal_1 = myMap[myVal_1]
        for x in myMap:
            if x == myVal_2:
                myVal_2 = myMap[myVal_2]
        if myVal_1 != ":true:" and myVal_1 != ":false:" or myVal_2 != ":true:" and myVal_2 != ":false:":
            push_val(":error:")
        else:
            if myVal_1 == myVal_2:
                temp = myVal_1
                pop_val()
                pop_val()
                push_val(temp)
            elif myVal_1 == ":true:" or myVal_2 == ":true:":
                pop_val()
                pop_val()
                push_val(":true:")
    else:
        push_val(":error:")

def comp_not():
    print("computing not")
    if len(myStack)>0:
        myVal_1 = myStack[0]
        for x in myMap:
            if x == myVal_1:
                myVal_1 = myMap[myVal_1]
        if myVal_1 != ":true:" and myVal_1 != ":false:":
            push_val(":error:")
        else:
            if myVal_1 == ":true:":
                pop_val()
                push_val(":false:")
            elif myVal_1 == ":false:":
                pop_val()
                push_val(":true:")
    else:
        push_val(":error:")

def comp_equal():
    print("computing equal")
    if len(myStack) > 1:
        myVal_1 = myStack[0]
        myVal_2 = myStack[1]
        for x in myMap:
            if x == myVal_1:
                myVal_1 = myMap[myVal_1]
        for x in myMap:
            if x == myVal_2:
                myVal_2 = myMap[myVal_2]
        if isinstance(myVal_1,int) and isinstance(myVal_2,int):
            if myVal_1 == myVal_2:
                pop_val()
                pop_val()
                push_val(":true:")
            else:
                pop_val()
                pop_val()
                push_val(":false:")
        else:
            push_val(":error:")
    else:
        push_val(":error:")

def comp_lessThan():
    print("computing lessThan")
    if len(myStack) > 1:
        myVal_1 = myStack[0]
        myVal_2 = myStack[1]
        for x in myMap:
            if x == myVal_1:
                myVal_1 = myMap[myVal_1]
        for x in myMap:
            if x == myVal_2:
                myVal_2 = myMap[myVal_2]
        if isinstance(myVal_1,int) and isinstance(myVal_2,int):
            if myVal_2 < myVal_1:
                pop_val()
                pop_val()
                push_val(":true:")
            else:
                pop_val()
                pop_val()
                push_val(":false:")
        else:
            push_val(":error:")
    else:
        push_val(":error:")

def bind():
    print("binding")
    if len(myStack) > 1:
        if isinstance(myStack[1], str):
            x = myStack[1]
            if x[len(x)-1] == "`" or x == ":error:" or x == "xletx" or x == ":true:" or x == ":false:" or x == ":unit:" or myStack[0] == ":error:":
                push_val(":error:")
            
            else:
                myMap[myStack[1]] = myStack[0]
                if x in myMap:
                    print("key: "+x)
                    if myMap[x] in myMap:
                        print("value: "+myMap[x])
                        print("value of value: "+str(myMap[myMap[x]]))
                        myMap[x] = myMap[myMap[x]]
                print (str(myStack[1])+" :" , str(myMap[myStack[1]]))
                pop_val()
                pop_val()
                push_val(":unit:")
        else:
            push_val(":error:")
    else:
        push_val(":error:")

def comp_if():
    if len(myStack) > 2:
        temp0 = myStack[0]
        temp1 = myStack[1]
        myVal_1 = myStack[0]
        myVal_2 = myStack[1]
        myVal_3 = myStack[2]
        for x in myMap:
            if x == myVal_1:
                myVal_1 = myMap[myVal_1]
        for x in myMap:
            if x == myVal_2:
                myVal_2 = myMap[myVal_2]
        for x in myMap:
            if x == myVal_3:
                myVal_3 = myMap[myVal_3]
        if myVal_3 == ":true:" or myVal_3 == ":false:":
            if myVal_3 == ":true:":
                pop_val()
                pop_val()
                pop_val()
                push_val(temp0)
            elif myVal_3 == ":false:":
                pop_val()
                pop_val()
                pop_val()
                push_val(temp1)
        else:
            push_val(":error:")
    else:
        push_val(":error:")
