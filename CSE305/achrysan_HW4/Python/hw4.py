import re
import copy
fInput = 0
def hw4(input, output):
    global myFuncNameArray
    myFuncNameArray = list()
    global myInOutFuncNameArray
    myInOutFuncNameArray = list()
    global retreHolder
    retreHolder = {}
    global fInput
    global hm_fun
    global hm_inOutFun
    hm_fun = {}
    hm_inOutFun = {}
    fInput = open(input,'r')
    f = open(output,'w')
    stack = []
    hm = {}
    for line in fileRead():
        if line.startswith('let'):
            stack.insert(0,parseLet(fInput,hm,f))
        elif line.startswith('inOutFun'):
            myClosure = ()
            funNameandArg = line[9:len(line)]
            counter = 0
            for x in funNameandArg:
                if x != ' ':
                    counter = counter + 1
                if x == ' ':
                    break
            funName = line[9:9+counter]
            myInOutFuncNameArray.insert(0,funName)
            print('funName:',funName)
            argName = line[10+counter:len(line)-1]
            print("Arg Name:",argName)
            parseinOutFun(fInput,hm,funName,argName,myClosure,stack)
        elif line.startswith('fun'):
            myClosure = ()
            funNameandArg = line[4:len(line)]
            counter = 0
            for x in funNameandArg:
                if x != ' ':
                    counter = counter + 1
                if x == ' ':
                    break
            funName = line[4:4+counter]
            myFuncNameArray.insert(0,funName)
            print('funName:',funName)
            argName = line[5+counter:len(line)-1]
            print("Arg Name:",argName)
            parseFun(fInput,hm,funName,argName,myClosure,stack)
        elif line.startswith('funEnd'):
            print("dog")
        elif line[0].isalpha():
            print("line:",line)
            parsePrimitive(line, stack, hm, f)
        elif line[0] == ':':
            parseBooleanOrError(line, stack, hm)
            
    fInput.close()

def fileRead():
    for line in fInput:
        yield line 

def parseFun(input, hm_parent,funcName,argumentName,myClosure,stack):
    global fInput
    global hm_fun
    statements = []
    #myList = copy.deepcopy(hm_parent)
    #hm_fun = myList
    for x in hm_parent:
        if not(x in hm_fun):
            hm_fun[x] = hm_parent[x]
    counter = 0
    for line in fileRead():
        if not(line.startswith('funEnd')) and counter < 1:
            statements.insert(len(statements), line)
        elif line.startswith('funEnd') :
            break
    myClosure = statements,argumentName,hm_fun
    print("Statements:",myClosure[0])
    print("ArgumentName:",myClosure[1])
    hm_fun[funcName] = myClosure
    print("Environment contains:",myClosure[2])
    print("Regular HM contains:",hm_parent)
    return stack.insert(0, ':unit:')
def parseinOutFun(input, hm_parent,funcName,argumentName,myClosure,stack):
    global fInput
    global hm_inOutFun
    statements = []
    for x in hm_parent:
        if not(x in hm_inOutFun):
            hm_inOutFun[x] = hm_parent[x]
    counter = 0
    for line in fileRead():
        if not(line.startswith('funEnd')) and counter < 1:
            if line.startswith('call'):
                line = '`call'
            statements.insert(len(statements), line)
        elif line.startswith('funEnd') :
            break
    myClosure = statements,argumentName,hm_inOutFun
    print("Statements:",myClosure[0])
    print("ArgumentName:",myClosure[1])
    print("statements:",statements)
    hm_inOutFun[funcName] = myClosure
    print("Environment (inOutFun) contains:",myClosure[2])
    print("Regular HM contains:",hm_parent)
    return stack.insert(0, ':unit:')

def parseLet(input,hm_parent,f):
    global fInput
    stack_let = []
    hm_let = {}
    removeThisFun = list()
    removeThisInOutFun = list()
    for line in fileRead():
        if line.startswith('end'):
            for x in hm_let:
                if x in myFuncNameArray:
                    myFuncNameArray.remove(x)
                if x in myInOutFuncNameArray:
                    myInOutFuncNameArray.remove(x)
                if x in hm_fun:
                    removeThisFun.insert(0,x)
                if x in hm_inOutFun:
                    removeThisInOutFun.insert(0,x)
            print("STACK_LET:",stack_let)
            for x in removeThisFun:
                if x in hm_fun:
                    del hm_fun[x]
            for x in removeThisInOutFun:
                if x in hm_inOutFun:
                    del hm_inOutFun[x]
            return stack_let[0]
        elif line[0] == 'let':
            stack.insert(0,parseLet(fInput,hm_let,f))
        elif line.startswith('fun'):
            myClosure = ()
            funNameandArg = line[4:len(line)]
            counter = 0
            for x in funNameandArg:
                if x != ' ':
                    counter = counter + 1
                if x == ' ':
                    break
            funName = line[4:4+counter]
            myFuncNameArray.insert(0,funName)
            print('funName:',funName)
            argName = line[5+counter:len(line)-1]
            print("Arg Name:",argName)
            parseFun(fInput,hm_let,funName,argName,myClosure,stack_let)
        elif line.startswith('inOutFun'):
            myClosure = ()
            funNameandArg = line[9:len(line)]
            counter = 0
            for x in funNameandArg:
                if x != ' ':
                    counter = counter + 1
                if x == ' ':
                    break
            funName = line[9:9+counter]
            myFuncNameArray.insert(0,funName)
            print('funName:',funName)
            argName = line[10+counter:len(line)-1]
            print("Arg Name:",argName)
            parseinOutFun(fInput,hm_let,funName,argName,myClosure,stack_let)
        elif line[0].isalpha() or line[0] == '`':
            parsePrimitive(line, stack_let, hm_let, f)
        elif line[0] == ':':
            parseBooleanOrError(line, stack_let, hm_let)

def parsePrimitive(line, stack, hm, f):
    if line.startswith('add'):
        doAdd(stack, hm)
    elif line.startswith('sub'):
        doSub(stack, hm)
    elif line.startswith('mul'):
        doMul(stack, hm)
    elif line.startswith('div'):
        doDiv(stack, hm)
    elif line.startswith('rem'):
        doRem(stack, hm)
    elif line.startswith('pop'):
        doPop(stack)
    elif line.startswith('push'):
        doPush(stack, line)
    elif line.startswith('swap'):
        doSwap(stack)
    elif line.startswith('neg'):
        doNeg(stack, hm)
    elif line.startswith('quit'):
        doQuit(stack, f)
    elif line.startswith('if'):
        doIf(stack, hm)
    elif line.startswith('not'):
        doNot(stack, hm)
    elif line.startswith('and'):
        doAnd(stack, hm)
    elif line.startswith('or'):
        doOr(stack, hm)
    elif line.startswith('equal'):
        doEqual(stack, hm)
    elif line.startswith('lessThan'):
        doLessThan(stack, hm)
    elif line.startswith('bind'):
        doBind(stack, hm)
    elif line.startswith('call'):
        print("\n")
        if(not(len(hm_fun) == 0)):
            doCall(stack,hm_fun,hm,f)
        elif(not(len(hm_inOutFun) == 0)):
            doinOutCall(stack,hm_inOutFun,hm,f)
        else:
            stack.insert(0,":error:")
    elif line.startswith('`call'):
        doinOutCall(stack,hm_inOutFun,hm,f)
    elif line.startswith('return'):
        if len(hm_fun) == 0:
            print('\n')
            print('ASDSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS')
            print('hm_parent:',hm)
            print('hm_inOutFun:',hm_inOutFun)
            for x in hm:
                if x in hm_inOutFun:
                    print('x:',x)
                    hm[x] = hm_inOutFun[x]
        return stack[0]
def doAdd(stack, hm):
    if len(stack) < 2:
        return stack.insert(0, ':error:')
    elif stack[0][0] == ':' or stack[1][0] == ':':
        return stack.insert(0, ':error:')
    else:
        s0 = str(stack[0])
        s1 = str(stack[1])
        if re.match('^[a-zA-Z].*',s0,0):
            s0 = str(hm.get(s0,s0))
        if re.match('^[a-zA-Z].*',s1,0):
            s1 = str(hm.get(s1,s1))
        if s0.isdigit and s1.isdigit:
            print("s1:",s1)
            print("s0:",s0)
            y = int(s0)
            x = int(s1)
            stack.pop(0)
            stack.pop(0)
            newTop = x+y
            return stack.insert(0, str(newTop))
        else:
            return stack.insert(0, ':error:')


def doSub(stack, hm):
    if len(stack) < 2:
        return stack.insert(0, ':error:')
    elif stack[0][0] == ':' or stack[1][0] == ':':
        return stack.insert(0, ':error:')
    else:
        s0 = str(stack[0])
        s1 = str(stack[1])
        if re.match('^[a-zA-Z].*',s0,0):
            s0 = str(hm.get(s0,s0))
        if re.match('^[a-zA-Z].*',s1,0):
            s1 = str(hm.get(s1,s1))
        if s0.isdigit and s1.isdigit:
            y = int(s0)
            x = int(s1)
            stack.pop(0)
            stack.pop(0)
            newTop = x-y
            return stack.insert(0, str(newTop))
        else:
            return stack.insert(0, ':error:')



def doMul(stack, hm):
    if len(stack) < 2:
        return stack.insert(0, ':error:')
    elif stack[0][0] == ':' or stack[1][0] == ':':
        return stack.insert(0, ':error:')
    else:
        s0 = str(stack[0])
        s1 = str(stack[1])
        if re.match('^[a-zA-Z].*',s0,0):
            s0 = str(hm.get(s0,s0))
        if re.match('^[a-zA-Z].*',s1,0):
            s1 = str(hm.get(s1,s1))
        if s0.isdigit and s1.isdigit:
            y = int(s0)
            x = int(s1)
            stack.pop(0)
            stack.pop(0)
            newTop = x*y
            return stack.insert(0, str(newTop))
        else:
            return stack.insert(0, ':error:')



def doDiv(stack, hm):
    if len(stack) < 2:
        return stack.insert(0, ':error:')
    elif stack[0][0] == ':' or stack[1][0] == ':':
        return stack.insert(0, ':error:')
    else:
        s0 = str(stack[0])
        s1 = str(stack[1])
        if re.match('^[a-zA-Z].*',s0,0):
            s0 = str(hm.get(s0,s0))
        if re.match('^[a-zA-Z].*',s1,0):
            s1 = str(hm.get(s1,s1))
        if s0.isdigit and s1.isdigit:
            y = int(s0)
            x = int(s1)
            if y == 0:
                return stack.insert(0, ':error:')
            stack.pop(0)
            stack.pop(0)
            newTop = x*y
            return stack.insert(0, str(newTop))
        else:
            return stack.insert(0, ':error:')



def doRem(stack, hm):
    if len(stack) < 2:
        return stack.insert(0, ':error:')
    elif stack[0][0] == ':' or stack[1][0] == ':':
        return stack.insert(0, ':error:')
    else:
        s0 = str(stack[0])
        s1 = str(stack[1])
        if re.match('^[a-zA-Z].*',s0,0):
            s0 = str(hm.get(s0,s0))
        if re.match('^[a-zA-Z].*',s1,0):
            s1 = str(hm.get(s1,s1))
        if s0.isdigit and s1.isdigit:
            y = int(s0)
            x = int(s1)
            if y == 0:
                return stack.insert(0, ':error:')
            stack.pop(0)
            stack.pop(0)
            newTop = x%y
            return stack.insert(0, str(newTop))
        else:
            return stack.insert(0, ':error:')


def doPop(stack):
    if len(stack) < 1:
        return stack.insert(0, ':error:')
    else:
        return stack.pop(0)


def doPush(stack, line):
    getList = line.split(' ',1)
    getList[1] = getList[1].strip('\n')
    if getList[1][0] == '-':
        if getList[1][1:] == '0':
            return stack.insert(0,'0')
        elif getList[1][1:].isdigit():
            return stack.insert(0, getList[1])
        else:
            return stack.insert(0, ':error:')
    elif getList[1].isdigit():
        return stack.insert(0, getList[1])
    elif re.match('^[a-zA-Z].*',getList[1],0):
        if getList[1]in hm_fun:
            if hm_fun[getList[1]] in myFuncNameArray:
                getList[1] = hm_fun[getList[1]]
        if getList[1] in hm_inOutFun:
            if hm_inOutFun[getList[1]] in myInOutFuncNameArray:
                getList[1] = hm_inOutFun[getList[1]]
        return stack.insert(0, getList[1])
    elif re.match('^".+"$',getList[1],0):
        return stack.insert(0, getList[1])
    else:
        return stack.insert(0, ':error:')


def doSwap(stack):
    if len(stack) < 2:
        return stack.insert(0, ':error:')
    else:
        x = stack[1]
        y = stack[0]
        stack.pop(0)
        stack.pop(0)
        stack.insert(0, y)
        return stack.insert(0, x)



def doNeg(stack, hm):
    if len(stack) < 1:
        return stack.insert(0, ':error:')
    elif stack[0][0] == ':' or stack[1][0] == ':':
        return stack.insert(0, ':error:')
    else:
        s0 = str(stack[0])
        if re.match('^[a-zA-Z].*',s0,0):
            s0 = str(hm.get(s0,s0))
        if s0.isdigit:
            x = int(s0)
            stack.pop(0)
            newTop = -1*x
            return stack.insert(0, str(newTop))
        else:
            return stack.insert(0, ':error:')


def doQuit(stack, f):
    print("stack:",stack)
    for ele in stack:
        f.write(ele.strip('"') + '\n')
    f.close()

def parseBooleanOrError(line, stack, hm):
    if line[1] == 'e':
        return stack.insert(0,':error:')
    elif line[1] == 't':
        return stack.insert(0,':true:')
    else:
        return stack.insert(0,':false:')

def doIf(stack, hm):
    if len(stack) < 3:
        return stack.insert(0, ':error:')
    else:
        s2 = str(stack[2])
        if s2 != ':true:' and s2 != ':false:':
            s2 = str(hm.get(s2,s2))
        if s2 == ':true:':
            stack.pop(2)
            stack.pop(1)
            return stack
        elif s2 == ':false:':
            stack.pop(2)
            stack.pop(0)
				
            return stack
        else:
            return stack.insert(0,':error:')

def doNot(stack, hm):
    if len(stack) < 1:
        return stack.insert(0, ':error:')
    else:
        s0 = str(stack[0])
        if s0 != ':true:' and s0 != ':false:':
            s0 = str(hm.get(s0,s0))
        if s0 == ':true:':
            stack.pop(0)
            stack.insert(0,':false:')
            return stack
        elif s0 == ':false:':
            stack.pop(0)
            stack.insert(0,':true:')
            return stack
        else:
            return stack.insert(0,':error:')
        
def doAnd(stack, hm):
    if len(stack) < 2:
        return stack.insert(0, ':error:')
    else:
        s0 = str(stack[0])
        s1 = str(stack[1])
        if s0 != ':true:' and s0 != ':false:':
            s0 = str(hm.get(s0,s0))
        if s1 != ':true:' and s1 != ':false:':
            s1 = str(hm.get(s1,s1))
        if s0 == ':false:' and s1 == ':false:':
            stack.pop(0)
            stack.pop(0)
            stack.insert(0,':false:')
            return stack
        elif s0 == ':false:' and s1 == ':true:':
            stack.pop(0)
            stack.pop(0)
            stack.insert(0,':false:')
            return stack
        elif s0 == ':true:' and s1 == ':false:':
            stack.pop(0)
            stack.pop(0)
            stack.insert(0,':false:')
            return stack
        elif s0 == ':true:' and s1 == ':true:':
            stack.pop(0)
            stack.pop(0)
            stack.insert(0,':true:')
            return stack
        else:
            return stack.insert(0,':error:')
        
def doOr(stack, hm):
    if len(stack) < 2:
        return stack.insert(0, ':error:')
    else:
        s0 = str(stack[0])
        s1 = str(stack[1])
        if s0 != ':true:' and s0 != ':false:':
            s0 = str(hm.get(s0,s0))
        if s1 != ':true:' and s1 != ':false:':
            s1 = str(hm.get(s1,s1))
        if s0 == ':false:' and s1 == ':false:':
            stack.pop(0)
            stack.pop(0)
            stack.insert(0,':false:')
            return stack
        elif s0 == ':false:' and s1 == ':true:':
            stack.pop(0)
            stack.pop(0)
            stack.insert(0,':true:')
            return stack
        elif s0 == ':true:' and s1 == ':false:':
            stack.pop(0)
            stack.pop(0)
            stack.insert(0,':true:')
            return stack
        elif s0 == ':true:' and s1 == ':true:':
            stack.pop(0)
            stack.pop(0)
            stack.insert(0,':true:')
            return stack
        else:
            return stack.insert(0,':error:')
        
def doEqual(stack, hm):
    if len(stack) < 2:
        return stack.insert(0, ':error:')
    elif stack[0][0] == ':' or stack[1][0] == ':':
        return stack.insert(0, ':error:')
    else:
        s0 = str(stack[0])
        s1 = str(stack[1])
        if re.match('^[a-zA-Z].*',s0,0):
            s0 = str(hm.get(s0,s0))
        if re.match('^[a-zA-Z].*',s1,0):
            s1 = str(hm.get(s1,s1))
        if s0.isdigit and s1.isdigit:
            y = int(s0)
            x = int(s1)
            stack.pop(0)
            stack.pop(0)
            if x==y:
                return stack.insert(0, ':true:')
            else:
                return stack.insert(0, ':false:')
        else:
            return stack.insert(0, ':error:')
        
def doLessThan(stack, hm):
    if len(stack) < 2:
        return stack.insert(0, ':error:')
    elif stack[0][0] == ':' or stack[1][0] == ':':
        return stack.insert(0, ':error:')
    else:
        s0 = str(stack[0])
        s1 = str(stack[1])
        if re.match('^[a-zA-Z].*',s0,0):
            s0 = str(hm.get(s0,s0))
        if re.match('^[a-zA-Z].*',s1,0):
            s1 = str(hm.get(s1,s1))
        if s0.isdigit and s1.isdigit:
            y = int(s0)
            x = int(s1)
            stack.pop(0)
            stack.pop(0)
            if x<y:
                return stack.insert(0, ':true:')
            else:
                return stack.insert(0, ':false:')
        else:
            return stack.insert(0, ':error:')
        
def doBind(stack, hm):
    if len(stack) < 2:
        return stack.insert(0,':error:')
    else:
        s0 = stack[0]
        s1 = stack[1]
        if re.match('^[a-zA-Z].*',stack[1],0) and stack[0] != ':error:':
            stack.pop(0)
            stack.pop(0)
            s0 = str(hm.get(s0,s0))
            hm[s1] = s0
            print("Regular HM is now:",hm)
            print("HM_fun is now:",hm_fun)
            print("HM_inOutFun is now:",hm_inOutFun)
            print('\n')
            return stack.insert(0,':unit:')
        else:
            return stack.insert(0,':error:')

def doCall(stack,hm,hm_parent,f):
    print("MADE IT TO CALL")
    global fInput
    funcName = stack[0]
    fun_stack = []
    if funcName in hm:
        print("True")
        if stack[1] == ":error:":
            return stack.insert(0,':error:')
        else:
            print("STACK[0]:",stack[0])
            print("STACK[1]:",stack[1])
            myTup = hm[funcName]
            myStatements = myTup[0]
            argName = myTup[1]
            print("HM_FUN CONTAINS:",hm)
            print("HM_PARENT CONTAINS:",hm_parent)
            if stack[1] in hm_parent:
                print("hi")
                if stack[0] in myFuncNameArray or hm_fun[stack[0]] in myFuncNameArray: #r stack[1] in myFuncNameArray:
                    print("stack[0] == funcname")
                    print('STACK[1]:',stack[1])
                    if stack[1] in myFuncNameArray: #and stack[0] in myFuncNameArray:
                        print("STACK[1] == FUNCNAME")
                        pass
                    else:
                        try:
                            print("stack[1]:",stack[1])
                            stack[1] = hm_parent[stack[1]]
                            print("New stack[1]:",stack[1])
                        except:
                            pass
            hm[argName] = stack[1]
            print("\nThis is the current environment:\n",hm)
            print("This is the current stack:",stack)
            print('\n')
            
            for x in myStatements:
                
                if x.startswith('let'):
                    fun_stack.insert(0,parseLet(fInput,hm,f))
                elif x[0].isalpha():
                    print("This is next line within statements:",x)
                    parsePrimitive(x, fun_stack, hm, f)
                    print("HM_FUN:",hm)
                    print("Fun_stack:",fun_stack)
                elif x[0] == ':':
                    parseBooleanOrError(x, fun_stack, hm)
            print("this is the fun_stack:",fun_stack)
            print("hm_fun ==:",hm)
            print("hm_parent ==:",hm_parent)
            try:
                for x in fun_stack:
                    if x in hm:
                        print("Changing var -> val")
                        index = fun_stack.index(x)
                        fun_stack.pop(index)
                        tformd = hm[x]
                        fun_stack.insert(index,tformd)
                        print('fun_stack:',fun_stack)
            except:
                pass
            retVal = fun_stack.pop(0)
            print("retVal:",retVal)
            print("STACK[0]        :",stack[0])
            stack.pop(0)
            print("STACK[0]        :",stack[0])
            stack.pop(0)
            print("STACK IS NOW:",stack)
            return stack.insert(0,retVal)
    else:
        return stack.insert(0, ':error:')

def doinOutCall(stack,hm,hm_parent,f):
    print("MADE IT TO CALL")
    global fInput
    funcName = stack[0]
    inOutfun_stack = []
    if funcName in hm:
        print("True")
        if stack[1] == ":error:":
            return stack.insert(0,':error:')
        else:
            print("STACK[0]:",stack[0])
            print("STACK[1]:",stack[1])
            myTup = hm[funcName]
            myStatements = myTup[0]
            argName = myTup[1]
            print("HM_InOutFUN CONTAINS:",hm)
            print("HM_PARENT CONTAINS:",hm_parent)
            if stack[1] in hm_parent:
                print("hi")
                print('myInOutFuncNameArray:',myInOutFuncNameArray)
                if stack[0] in myInOutFuncNameArray or hm_inOutFun[stack[0]] in myInOutFuncNameArray: #r stack[1] in myFuncNameArray:
                    print("stack[0] == funcname")
                    print('STACK[1]:',stack[1])
                    if stack[1] in myInOutFuncNameArray: #and stack[0] in myFuncNameArray:
                        print("STACK[1] == FUNCNAME")
                        pass
                    else:
                        try:
                            capture = stack[1]
                            print("stack[1]:",stack[1])
                            stack[1] = hm_parent[stack[1]]
                            print("New stack[1]:",stack[1])
                        except:
                            pass
            retreHolder[capture] = argName
            print("RETREHOLDER:",retreHolder)
            hm[argName] = stack[1]
            print("\nThis is the current environment:\n",hm)
            print("This is the current stack:",stack)
            print('\n')
            
            for x in myStatements:
                
                if x.startswith('let'):
                    inOutfun_stack.insert(0,parseLet(fInput,hm,f))
                elif x.startswith('end'):
                    print("The next line is end")
                elif x[0].isalpha() or x[0] == '`':
                    print("This is next line within statements:",x)
                    parsePrimitive(x, inOutfun_stack, hm, f)
                    print("HM_inOutFUN:",hm)
                    print("inOutFun_stack:",inOutfun_stack)
                elif x[0] == ':':
                    parseBooleanOrError(x, inOutfun_stack, hm)
            print("this is the inOutfun_stack:",inOutfun_stack)
            print("hm_inOutfun ==:",hm)
            print("hm_parent ==:",hm_parent)
            try:
                for x in inOutfun_stack:
                    if x in hm:
                        print("Changing var -> val")
                        index = inOutfun_stack.index(x)
                        inOutfun_stack.pop(index)
                        tformd = hm[x]
                        inOutfun_stack.insert(index,tformd)
            except:
                pass
            retVal = inOutfun_stack.pop(0)
            print("retVal:",retVal)
            print("STACK[0]        :",stack[0])
            stack.pop(0)
            print("STACK[0]        :",stack[0])
            stack.pop(0)
            print("STACK IS NOW:",stack)
            print('\n\n')
            print('retreHolder:',retreHolder)
            print('hm_parent:',hm_parent)
            print('hm_inOutFun:',hm_inOutFun)
            for x in retreHolder:
                if retreHolder[x] in hm_inOutFun and x in hm_parent:
                    print('x:',x)
                    print('retreHolder[x]:',retreHolder[x])
                    print('hm_parent[x]',hm_parent[x])
                    print('hm_inOutFun[x]:',hm_inOutFun[retreHolder[x]])
                    hm_parent[x] = hm_inOutFun[retreHolder[x]]        
            return stack.insert(0,retVal)
    else:
        return stack.insert(0, ':error:')
