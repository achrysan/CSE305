(* CSE305 Spring 2016
 * A possible solution to HW2, expressed in Standard ML
 * Author: Carl Alphonce
 * Modified: Lu Meng
 *)

(****************************************************************************
 TYPE DEFINITIONS 
 ****************************************************************************)

(* The type of expressions and special forms *)
datatype exp =
    Boolean of bool
  | Number of int
  | String of string
  | Name of string 
  | Error | Quit | Add | Sub | Mul | Div | Rem | Pop | Swap | Neg |
  And | Or | Not | Bind | Equals | LessThan | If | Let | End | Unit;

  
(****************************************************************************
 UTILITY FUNCTIONS 
 ****************************************************************************)

(* Utility function to build a textual form of an expression
   or special form, used for printing.
 *)
fun expression2string(Boolean(true)) = ":true:"
  | expression2string(Boolean(false)) = ":false:"
  | expression2string(String(s)) = s
  | expression2string(Number(X)) = if (X<0) then "-"^Int.toString(~X) else Int.toString(X)
  | expression2string(Error) = ":error:"
  | expression2string(Unit) = ":unit:"
  | expression2string(Name(x)) = x 
  | expression2string(Let) = "let"
  | expression2string(End) = "end"
  | expression2string(_) = "?? should not happen ??"
  ;


(* Computes quotient according to rules of the language *)
fun quotient(a2,a1) =
    if (a1<0)
    then if (a2 div a1) * a1 > a2 then (a2 div a1)+1 else (a2 div a1)
    else (a2 div a1);

(* Computes remainder according to rules of the language *)
fun remainder(a2,a1) = a2 - a1 * quotient(a2,a1);


(****************************************************************************
 MAIN EVALUATOR FUNCTIONS 
 ****************************************************************************)

(* Applies a primitive function to its two arguments *)

fun 
  (* 0-ARY OPERATORS *)
    apply(_,[])  = (Error,[])

  (* UNARY OPERATORS *)
  | apply(Neg,Number(a)::rest) = (Number(~a),rest)
  | apply(Not,Boolean(a) :: rest) = (Boolean(not a), rest)
  | apply(_,[x]) = (Error,[x])

  (* BINARY OPERATORS *)
  | apply(Add,Number(a1)::Number(a2)::rest) = (Number(a2+a1),rest)
  | apply(Sub,Number(a1)::Number(a2)::rest) = (Number(a2-a1),rest)
  | apply(Mul,Number(a1)::Number(a2)::rest) = (Number(a2*a1),rest)
  | apply(Div,Number(a1)::Number(a2)::rest) = (if a1 = 0 then (Error,Number(a1)::Number(a2)::rest) else (Number(quotient(a2,a1)),rest))
  | apply(Rem,Number(a1)::Number(a2)::rest) = (if a1 = 0 then (Error,Number(a1)::Number(a2)::rest) else (Number(remainder(a2,a1)),rest))
  | apply(Equals, Number(a1) :: Number(a2) :: rest) = (Boolean(a2 = a1), rest)
  | apply(LessThan, Number(a1) :: Number(a2) :: rest) =  (Boolean(a2 < a1), rest)
  | apply(And, Boolean(a1) :: Boolean(a2) :: rest) =  (Boolean(a2 andalso a1), rest)
  | apply(Or, Boolean(a1) :: Boolean(a2) :: rest) =  (Boolean(a2 orelse a1), rest)
  
  (*  TERNARY OPERATORS *)
  | apply(If, a1 :: a2 :: Boolean(true) :: rest) =  (a1, rest)
  | apply(If, a1 :: a2 :: Boolean(false) :: rest) =  (a2, rest)
  
  (*Anything else results in an error *)
  | apply(_,stack) = (Error,stack)
  ;

  
 (* Functions to look up name in the list of environments *)
fun lookup2(Name(x),[]) = NONE
  | lookup2(Name(x), (Name(y),value)::bindings) =
      if (x=y) then SOME(value)
               else lookup2(Name(x),bindings)
  | lookup2(_,_) = SOME(Error);  
 
  
fun lookup(Name(x),[]) = Name(x)
  | lookup(Name(x),e::es) = (
       case (lookup2(Name(x),e)) of
       	  NONE => lookup(Name(x),es)
       	| SOME(v) => v )
  | lookup(_,_) = Error;

 (* Function to check if a name is bound *)

fun isBound(Name(x),[]) = NONE
  | isBound(Name(x),e::es) = (
       case (lookup2(Name(x),e)) of
       	  NONE => isBound(Name(x),es)
       	| SOME(v) => SOME(v))
  | isBound(_,_) = SOME(Error);
  

fun bind(Error::Name(n)::rest, e :: es) = (Error::Name(n)::rest, e :: es)
| bind(Unit::Name(n)::rest, e::es) = (Unit::rest,((Name(n),Unit)::e)::es)
| bind(String(s) :: Name(n) :: rest, e::es) =  (Unit::rest, ((Name(n),String(s))::e)::es)
| bind(Number(x) :: Name(n) :: rest, e::es) =  (Unit::rest, ((Name(n),Number(x))::e)::es)
| bind(Boolean(s) :: Name(n) :: rest, e::es) =  (Unit::rest, ((Name(n),Boolean(s))::e)::es)
(*
| bind(Name(value) ::Name(n)::rest, e::es) =  (
  case (isBound(Name(value),e::es)) of
  	  NONE => (Error:: Name(value) :: Name(n) ::rest, e::es) 
  	| SOME(c) => (Unit::rest, ((Name(n),c)::e)::es)
	 ) *)
| bind(value::Name(n)::rest, e::es) =  (
  case (isBound(value,e::es)) of
  	  NONE => (Unit::rest, ((Name(n),value)::e)::es)
  	| SOME(c) => (Unit::rest,((Name(n),c)::e)::es) )
| bind(stack,envs) = (Error::stack, envs);

(*
| bind(value ::Name(n)::rest, e::es) =  (
  case (isBound(Name(n),e::es)) of
  	  NONE => (Unit::rest, ((Name(n),value)::e)::es) 
  	| SOME(c) => (Unit::rest, ((Name(n),c)::e)::es)
	 )
  | bind(stack,envs) = (Error::stack, envs);
 *)
 
fun doPop(Let :: rest) = rest 
| doPop(a :: b) = doPop(b) 
| doPop([]) = [] ;


fun doLet(stack, envs) = ( Let :: stack,envs);

fun doEnd(a :: rest, envs) = ( a :: doPop(rest),envs) ;
  
(* stack operations *)

fun stackOps(Pop, x::stack) = stack
  | stackOps(Swap, x::y::stack) = y::x::stack
  | stackOps(_,stack) = Error::stack
  ;

(* Evaluates an expression *)

fun eval(Boolean(x), stack, env) = (Boolean(x)::stack , env)
  | eval(Number(x), stack , env)  = (Number(x)::stack , env)
  | eval(Name(x), stack, env)    = (lookup(Name(x),env)::stack, env)
  | eval(Bind, stack, env)       = bind(stack, env)
  | eval(Let,stack,env) = doLet(stack,env)
  | eval(End,stack,env) = doEnd(stack,env)
  | eval(Quit, stack, env)       = (Quit::stack , env)
  | eval(Pop, x::stack, env)     = (stack , env)
  | eval(String(x), stack, env)  = (String(x)::stack,env)
  | eval(Swap, x::y::stack , env)     = (y::x::stack, env)
  | eval(Error, stack , env)      = (Error::stack,env)
  | eval(Unit,stack , env) = (Unit::stack, env)
  | eval(expr, stack , env) = let
        val (v,s) = apply(expr, stack)
    in
        (v::s , env)
    end;

(* Functions to parse a number *)

fun parseNumber(x,inStr) = 
    case (TextIO.input1(inStr)) of
	NONE => SOME(Error)
      | SOME(ch) => 
	    if (Char.isDigit(ch)) then parseNumber(x*10+(ord(ch)-ord(#"0")),inStr)
       else if (Char.isSpace(ch)) then SOME(Number(x))
       else SOME(Error)
      ;

fun parseNegativeNumber(inStr) = 
    case ( parseNumber(0,inStr) ) of
        NONE => SOME(Error)
      | SOME(Number(num)) =>  SOME(Number(~1 * num))
      | SOME(_) => SOME(Error) 
      ;

(* Function to parse a boolean  *)

fun parseBoolean(x, inStr) = 
    case (TextIO.input1(inStr)) of
	NONE => SOME(Error)
      | SOME(ch) => 
	    if (Char.isAlpha(ch) orelse ch = #":") then parseBoolean(x^Char.toString(ch),inStr)
       else if (Char.isSpace(ch))
	       then if (x = ":true:")  then SOME(Boolean(true))
	       else if (x = ":false:") then SOME(Boolean(false))
	       else SOME(Error)
       else SOME(Error);

(* Function to parse an error *)

fun parseError(x, inStr) = 
    case (TextIO.input1(inStr)) of
	NONE => SOME(Error)
      | SOME(ch) => 
	    if (Char.isAlpha(ch) orelse ch = #":") then parseError(x^Char.toString(ch),inStr)
       else if (Char.isSpace(ch))
	       then if (x = ":error:")  then SOME(Error)
	       else SOME(Error)
       else SOME(Error);

(***** EDITED TO HERE ********************************************************************)

(* Function to parse a boolean or error  *)

fun parseString(x, inStr) =
    case (TextIO.input1(inStr)) of
        NONE => SOME(Error)
      | SOME(ch) =>
			if (ch = #"\"") then SOME(String(x))
       else parseString(x^Char.toString(ch),inStr)
	  
      

fun parseBooleanOrError(x, inStr) = 
    case (TextIO.input1(inStr)) of
	NONE => SOME(Error)
      | SOME(ch) => 
	    if (ch = #"e")                  then parseError(x^Char.toString(ch),inStr)
       else if (ch = #"t" orelse ch = #"f") then parseBoolean(x^Char.toString(ch),inStr)
       else SOME(Error);

(* Function to parse a primitive  *)

fun parsePrimitive(x, inStr) = 
    case (TextIO.input1(inStr)) of
	NONE => SOME(Error)
      | SOME(ch) => 
	    if (Char.isAlpha(ch) orelse Char.isDigit(ch))  then parsePrimitive(x^Char.toString(ch),inStr)
       else if (ch = #"\n")
	       then if (x = "add") then SOME(Add)
	       else if (x = "sub") then SOME(Sub)
	       else if (x = "mul") then SOME(Mul)
	       else if (x = "div") then SOME(Div)
	       else if (x = "rem") then SOME(Rem)
	       else if (x = "pop") then SOME(Pop)
	       else if (x = "swap") then SOME(Swap)
	       else if (x = "neg") then SOME(Neg)
		   else if (x = "and") then SOME(And)
	       else if (x = "or") then SOME(Or)
	       else if (x = "not") then SOME(Not)
	       else if (x = "equal") then SOME(Equals)
	       else if (x = "lessThan") then SOME(LessThan)
	       else if (x = "if") then SOME(If)
	       else if (x = "bind") then SOME(Bind)
           else if (x = "quit") then SOME(Quit)
		   else if (x = "let") then SOME(Let)
		   else if(x = "end") then SOME(End)
		   else SOME(Name(x))
       else SOME(Error);

(* fun parsePush(inStr) = 
    case (TextIO.input1(inStr)) of
  NONE => SOME(Error)
      | SOME(ch) =>
      if (Char.isAlpha(ch)) then parsePush(inStr)
       else if (Char.isSpace(ch))
         then if (TextIO.input1(inStr) = SOME(c)) then
              (if c = #"-") then parseNegativeNumber(inStr)
              else parseNumber(ord(TextIO.input1(inStr))-ord(#"0"),inStr))
       else SOME(Error);
*)




(* A recursive helper function for the parse function, which reads
   a character from the input stream and determines what more
   specific parsing function to call.
 *)      
fun parseHelper(NONE, inStr) = NONE
  | parseHelper(SOME(ch), inStr) =

  let

    val line = Option.valOf (TextIO.inputLine inStr)
    val second = String.sub (line, 0)
    val inStr1 = TextIO.openString line

  in
      if (ch = #"p" andalso second = #"u") then parseHelper(TextIO.input1(TextIO.openString (String.extract(line,4,NONE))), TextIO.openString (String.extract(line, 5, NONE)))
 else if (Char.isDigit(ch)) then parseNumber(ord(ch)-ord(#"0"),inStr1)
 else if (ch = #"-")        then parseNegativeNumber(inStr1)
 else if (ch = #":")        then parseBooleanOrError(":", inStr1)
 else if (ch = #"\"")       then parseString("", inStr1)
 else if (Char.isAlpha(ch)) then parsePrimitive(Char.toString(ch), inStr1)
 else if (ch = #"\n")       then parseHelper(TextIO.input1(inStr1), inStr1)
 else NONE
 end;


(* Function to parse the next expression on the input stream. *)      
fun parse(inStr) = parseHelper(TextIO.input1(inStr), inStr);







fun hw4(inFile : string, outFile : string) =
  let
    val fileInp = TextIO.openIn inFile
    val fileOut = TextIO.openOut outFile
    fun printStack([]) = ()
    | printStack(x::xs) = ( TextIO.output (fileOut, (expression2string(x)^"\n")) ; printStack(xs) );

    fun replHelper(inStr, (stack,env)) =
    (
      
      case (parse(inStr)) of 
         NONE => replHelper(inStr, (stack,env))
        | SOME(Quit) => (printStack(stack); TextIO.closeIn fileInp; TextIO.closeOut fileOut) 
        | SOME(expression) => replHelper(inStr,eval(expression, stack,env)) 
    );

  in
    replHelper(fileInp, ([],[[]]))
  end

